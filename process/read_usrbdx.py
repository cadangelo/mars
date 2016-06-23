#!/usr/env/python
import math

def tokenize(string,token):
    tokens = string.split( )
    return tokens[token]

def delimit(item):
    string = ' '.join(item.split())
    return string

class UsrbdxFile:
    def __init__(self):
        self.num_primaries = 0
        self.total_weight = 0
        self.scorers = {}

    def read_file(self,file_name):
        # open the file 
        self.file_name = file_name
        self.f = open(self.file_name,'r')

        # read line by line
        for i in range(4):
            line = self.f.readline()
        line = self.f.readline()
        self.num_primaries = int(tokenize(delimit(line),3))
        line = self.f.readline()
        self.total_weight = float(tokenize(delimit(line),6))

        # read two blank llnes
        for i in range(2):
            line = self.f.readline()

        ok = True
        while ok:
            try:
                data = Usrbdx(self.f)
                data.read_usrbdx()
                self.scorers[data.detector_name] = data
            except:
                ok = False

class AveAdd:
    def __init__(self, usrbdxfile1,usrbdxfile2,wgt1,wgt2):
        self.num_hist1 = usrbdxfile1.num_primaries
        self.num_hist2 = usrbdxfile2.num_primaries
        self.file1 = usrbdxfile1
        self.file2 = usrbdxfile2

        self.wgt1 = wgt1
        self.wgt2 = wgt2

        self.data = UsrbdxFile()
        self.data.num_histories = self.num_hist1 + self.num_hist2

    def average(self, value1,value1_err,value2,value2_err):
        n  = self.num_hist1 +  self.num_hist2
        s1 = self.num_hist1 * value1
        s2 = self.num_hist2 * value2
        t1 = self.num_hist1 * value1**2
        t1 = t1 * (self.num_hist1 * value1_err**2 + 100)
        t2 = self.num_hist2 * value2**2
        t2 = t2 * (self.num_hist2 * value2_err**2 + 100)
        mean = (s1+s2)/n
        stddev2 = ((t1+t2)/n - mean*mean)/n
        
        if mean == 0:
            stddev = 0
        else:
            stddev = math.sqrt(stddev2)/mean

        return mean,stddev

    def sum(self, value1,value1_err,value2,value2_err):
        n  = self.num_hist1 +  self.num_hist2

        s1 = value1*self.wgt1
        s2 = value2*self.wgt2
        e1 = value1_err
        e2 = value2_err
 
        SUM = (s1*self.wgt1)+(s2*self.wgt2)
        if SUM == 0:
            stddev = 0.0
        else:
            stddev = math.sqrt((s1*e1)**2 + (s2*e2)**2)/(SUM)
        return SUM,stddev


    def calculate_sum(self,particle_name):
        data1 = self.file1.scorers[particle_name]
        data2 = self.file2.scorers[particle_name]
        
        val,stddev = self.sum(data1.total_response,data1.total_response_error,
                                  data2.total_response,data2.total_response_error)
        new_total_response = val
        new_total_response_error = stddev

        new_total_flux = []
        new_total_flux_error = []
        for value in range(len(data1.total_flux)):
            val,stddev = self.sum(data1.total_flux[value],data1.total_flux_error[value],
                                  data2.total_flux[value],data2.total_flux_error[value])
            new_total_flux.append(val)
            new_total_flux_error.append(stddev)

        new_cumul_flux = []
        new_cumul_flux_error = []
        for value in range(len(data1.cumul_flux)):
            val,stddev = self.sum(data1.cumul_flux[value],data1.cumul_flux_error[value],
                                  data2.cumul_flux[value],data2.cumul_flux_error[value])
            new_cumul_flux.append(val)
            new_cumul_flux_error.append(stddev)

        new_angle_flux = []
        new_angle_flux_error = []
        for value in range(len(data1.angle_flux)):
            new_angle_flux_bin = []
            new_angle_flux_error_bin = []
            for item in range(len(data1.angle_flux[value])):
                val,stddev = self.sum(data1.angle_flux[value][item],data1.angle_flux_error[value][item],
                                      data2.angle_flux[value][item],data2.angle_flux_error[value][item])
                new_angle_flux_bin.append(val)
                new_angle_flux_error_bin.append(stddev)
            new_angle_flux.append(new_angle_flux_bin)
            new_angle_flux_error.append(new_angle_flux_error_bin)

        new_solid_angle_flux = []
        new_solid_angle_flux_error = []
        for value in range(len(data1.solid_angle_flux)):
            new_solid_angle_flux_bin = []
            new_solid_angle_flux_error_bin = []
            for item in range(len(data1.solid_angle_flux[value])):
                val,stddev = self.sum(data1.solid_angle_flux[value][item],data1.solid_angle_flux_error[value][item],
                                      data2.solid_angle_flux[value][item],data2.solid_angle_flux_error[value][item])
                new_solid_angle_flux_bin.append(val)
                new_solid_angle_flux_error_bin.append(stddev)
            new_solid_angle_flux.append(new_solid_angle_flux_bin)
            new_solid_angle_flux_error.append(new_solid_angle_flux_error_bin)

        new_bdx = Usrbdx("")
        new_bdx.detector_name = data1.detector_name
        new_bdx.detector_number = data1.detector_number
        new_bdx.area = data1.area
        new_bdx.distribution = data1.distribution
        new_bdx.from_reg = data1.from_reg
        new_bdx.to_reg = data1.to_reg
        new_bdx.two_way = data1.two_way
        new_bdx.total_response = new_total_response
        new_bdx.total_response_error = new_total_response_error
        new_bdx.e_bounds = data1.e_bounds
        new_bdx.total_flux = new_total_flux
        new_bdx.total_flux_error = new_total_flux_error
        new_bdx.cumul_flux = new_cumul_flux
        new_bdx.cumul_flux_error = new_cumul_flux_error 
        new_bdx.solid_angle_boundaries  = data1.solid_angle_boundaries
        new_bdx.angle_boundaries = data1.angle_boundaries
        new_bdx.angle_flux = new_angle_flux
        new_bdx.angle_flux_error = new_angle_flux_error
        new_bdx.solid_angle_flux = new_solid_angle_flux
        new_bdx.solid_angle_flux_error = new_solid_angle_flux_error

        return new_bdx

      
    def calculate_average(self,particle_name):
        data1 = self.file1.scorers[particle_name]
        data2 = self.file2.scorers[particle_name]
        
        mean,stddev = self.average(data1.total_response,data1.total_response_error,
                                  data2.total_response,data2.total_response_error)
        new_total_response = mean
        new_total_response_error = stddev

        new_total_flux = []
        new_total_flux_error = []
        for value in range(len(data1.total_flux)):
            mean,stddev = self.average(data1.total_flux[value],data1.total_flux_error[value],
                                  data2.total_flux[value],data2.total_flux_error[value])
            new_total_flux.append(mean)
            new_total_flux_error.append(stddev)

        new_cumul_flux = []
        new_cumul_flux_error = []
        for value in range(len(data1.cumul_flux)):
            mean,stddev = self.average(data1.cumul_flux[value],data1.cumul_flux_error[value],
                                  data2.cumul_flux[value],data2.cumul_flux_error[value])
            new_cumul_flux.append(mean)
            new_cumul_flux_error.append(stddev)

        new_angle_flux = []
        new_angle_flux_error = []
        for value in range(len(data1.angle_flux)):
            new_angle_flux_bin = []
            new_angle_flux_error_bin = []
            for item in range(len(data1.angle_flux[value])):
                mean,stddev = self.average(data1.angle_flux[value][item],data1.angle_flux_error[value][item],
                                      data2.angle_flux[value][item],data2.angle_flux_error[value][item])
                new_angle_flux_bin.append(mean)
                new_angle_flux_error_bin.append(stddev)
            new_angle_flux.append(new_angle_flux_bin)
            new_angle_flux_error.append(new_angle_flux_error_bin)

        new_solid_angle_flux = []
        new_solid_angle_flux_error = []
        for value in range(len(data1.solid_angle_flux)):
            new_solid_angle_flux_bin = []
            new_solid_angle_flux_error_bin = []
            for item in range(len(data1.solid_angle_flux[value])):
                mean,stddev = self.average(data1.solid_angle_flux[value][item],data1.solid_angle_flux_error[value][item],
                                      data2.solid_angle_flux[value][item],data2.solid_angle_flux_error[value][item])
                new_solid_angle_flux_bin.append(mean)
                new_solid_angle_flux_error_bin.append(stddev)
            new_solid_angle_flux.append(new_solid_angle_flux_bin)
            new_solid_angle_flux_error.append(new_solid_angle_flux_error_bin)

        new_bdx = Usrbdx("")
        new_bdx.detector_name = data1.detector_name
        new_bdx.detector_number = data1.detector_number
        new_bdx.area = data1.area
        new_bdx.distribution = data1.distribution
        new_bdx.from_reg = data1.from_reg
        new_bdx.to_reg = data1.to_reg
        new_bdx.two_way = data1.two_way
        new_bdx.total_response = new_total_response
        new_bdx.total_response_error = new_total_response_error
        new_bdx.e_bounds = data1.e_bounds
        new_bdx.total_flux = new_total_flux
        new_bdx.total_flux_error = new_total_flux_error
        new_bdx.cumul_flux = new_cumul_flux
        new_bdx.cumul_flux_error = new_cumul_flux_error 
        new_bdx.solid_angle_boundaries  = data1.solid_angle_boundaries
        new_bdx.angle_boundaries = data1.angle_boundaries
        new_bdx.angle_flux = new_angle_flux
        new_bdx.angle_flux_error = new_angle_flux_error
        new_bdx.solid_angle_flux = new_solid_angle_flux
        new_bdx.solid_angle_flux_error = new_solid_angle_flux_error

        return new_bdx
        
    def get_ave(self):
        for item in self.file1.scorers.keys():
            usrbdx = self.calculate_average(item)
            self.data.scorers[item] = usrbdx
        return self.data      

    def get_sum(self):
        for item in self.file1.scorers.keys():
            usrbdx = self.calculate_sum(item)
            self.data.scorers[item] = usrbdx
        return self.data      

        

class Usrbdx:
    def __init__(self, file_unit):
        self.detector_name = ""
        self.detector_number = 0
        self.area = 0.0
        self.distribution = 0
        self.from_reg = 0
        self.to_reg = 0
        self.two_way = False
        self.total_response = 0.0
        self.total_response_error = 0.0
        self.e_bounds = []
        self.total_flux = []
        self.total_flux_error = []
        self.cumul_flux = []       
        self.cumul_flux_error = []       
        self.solid_angle_boundaries = []
        self.angle_boundaries = []
        self.angle_flux = []
        self.angle_flux_error = []
        self.solid_angle_flux = []
        self.solid_angle_flux_error = []      
        self.f = file_unit

    def _read_different_flux(self):

        # reading energy limits
        line = self.f.readline()
        e_bounds = []
        while line.find("Lowest boundary") < 0: 
            e_bounds.extend(delimit(line).split( ))
            line = self.f.readline()
        # now add the lowest boundary
        e_bounds.append(float(tokenize(delimit(line),3)))

        # read three blank llnes
        for i in range(3):
            line = self.f.readline()
            
        # loop over the energy groups
        for i in range((len(e_bounds)-1)/2):
            line = self.f.readline()
            self.total_flux.append(float(tokenize(delimit(line),0)))
            self.total_flux_error.append(float(tokenize(delimit(line),2)))
            self.total_flux.append(float(tokenize(delimit(line),4)))
            self.total_flux_error.append(float(tokenize(delimit(line),6)))
        # there may be one more value to read
        if((len(e_bounds)-1)%2 == 1):
            line = self.f.readline()
            self.total_flux.append(float(tokenize(delimit(line),0)))
            self.total_flux_error.append(float(tokenize(delimit(line),2)))
        self.e_bounds.extend(e_bounds)

        line = self.f.readline()
        line = self.f.readline()

        if line.find("Energy boundaries") > 0: 
            line = self.f.readline()
            e_bounds = []
            while line.find("Lowest boundary") < 0: 
                e_bounds.extend(delimit(line).split( ))
                line = self.f.readline()
            # now add the lowest boundary
            e_bounds.append(float(tokenize(delimit(line),3)))
            # read three blank llnes
            for i in range(3):
                line = self.f.readline()
            
            # loop over the energy groups
            for i in range((len(e_bounds)-1)/2):
                line = self.f.readline()
                self.total_flux.append(float(tokenize(delimit(line),0)))
                self.total_flux_error.append(float(tokenize(delimit(line),2)))
                self.total_flux.append(float(tokenize(delimit(line),4)))
                self.total_flux_error.append(float(tokenize(delimit(line),6)))
                # there may be one more value to read
            if((len(e_bounds)-1)%2 == 1):
                line = self.f.readline()
                self.total_flux.append(float(tokenize(delimit(line),0)))
                self.total_flux_error.append(float(tokenize(delimit(line),2)))
            self.e_bounds.extend(e_bounds)                  

        else:
            self.f.seek(-1*len(line),1)

        return

    def _read_cumul_flux(self):
        for i in range(6):
            line = self.f.readline()

        e_bounds = []
        while line.find("Lowest boundary") < 0: 
            e_bounds.extend(delimit(line).split( ))
            line = self.f.readline()
        # now add the lowest boundary
        e_bounds.append(float(tokenize(delimit(line),3)))

        # read three blank llnes
        for i in range(3):
            line = self.f.readline()

        # loop over the energy groups
        for i in range((len(e_bounds)-1)/2):
            line = self.f.readline()
            self.cumul_flux.append(float(tokenize(delimit(line),0)))
            self.cumul_flux_error.append(float(tokenize(delimit(line),2)))
            self.cumul_flux.append(float(tokenize(delimit(line),4)))
            self.cumul_flux_error.append(float(tokenize(delimit(line),6)))
        # there may be one more value to read
        if((len(e_bounds)-1)%2 == 1):
            line = self.f.readline()
            self.cumul_flux.append(float(tokenize(delimit(line),0)))
            self.cumul_flux_error.append(float(tokenize(delimit(line),2)))


        line = self.f.readline()
        line = self.f.readline()

        if line.find("Energy boundaries") > 0: 
            # if we have low energy neutrons
            # need to loose the last group of self.ebounds
            self.e_bounds = self.e_bounds[:-1]
            line = self.f.readline()
            e_bounds = []
            while line.find("Lowest boundary") < 0: 
                e_bounds.extend(delimit(line).split( ))
                line = self.f.readline()

            # now add the lowest boundary
            e_bounds.append(float(tokenize(delimit(line),3)))

            # read three blank llnes
            for i in range(3):
                line = self.f.readline()
            
            # loop over the energy groups
            for i in range((len(e_bounds)-1)/2):
                line = self.f.readline()
                self.cumul_flux.append(float(tokenize(delimit(line),0)))
                self.cumul_flux_error.append(float(tokenize(delimit(line),2)))
                self.cumul_flux.append(float(tokenize(delimit(line),4)))
                self.cumul_flux_error.append(float(tokenize(delimit(line),6)))
                # there may be one more value to read
            if((len(e_bounds)-1)%2 == 1):
                line = self.f.readline()
                self.cumul_flux.append(float(tokenize(delimit(line),0)))
                self.cumul_flux_error.append(float(tokenize(delimit(line),2)))

        else:
            # rewind until 
            self.f.seek(-(len(line)),1)

        return



        return

    def read_total_fluxes(self):
        # read tot resp
        # read two blank llnes
        for i in range(2):
            line = self.f.readline()
        line = self.f.readline()
        self.total_response = float(tokenize(delimit(line),3))
        self.total_response_error = float(tokenize(delimit(line),5))

        # read seven blank llnes
        for i in range(7):
            line = self.f.readline()

        self._read_different_flux()
        # it might be the case that for low energy neutrons we have more data to read      
        line = self.f.readline()

        # it might be the case that for low energy neutrons we have more data to read      
        self._read_cumul_flux()
       
        return


    def read_angle_flux(self,e_group):
        # line is now on "Energy Interval"
        line = self.f.readline()

        for i in range(3):
            line = self.f.readline()

        # we already know the size of the angle arrays
        num_angles = len(self.angle_boundaries)-1
        for i in range(num_angles/2):
           line = self.f.readline()
           self.solid_angle_flux[e_group].append(float(tokenize(delimit(line),0)))
           self.solid_angle_flux_error[e_group].append(float(tokenize(delimit(line),2)))
           self.solid_angle_flux[e_group].append(float(tokenize(delimit(line),4)))
           self.solid_angle_flux_error[e_group].append(float(tokenize(delimit(line),6)))
        if num_angles%2 == 1:
           line = self.f.readline()
           self.solid_angle_flux[e_group].append(float(tokenize(delimit(line),0)))
           self.solid_angle_flux_error[e_group].append(float(tokenize(delimit(line),2)))

        # now read 3 blanks
        for i in range(3):
            line = self.f.readline()
        # we already know the size of the angle arrays
        num_angles = len(self.angle_boundaries)-1
        for i in range(num_angles/2):
           line = self.f.readline()
           self.angle_flux[e_group].append(float(tokenize(delimit(line),0)))
           self.angle_flux_error[e_group].append(float(tokenize(delimit(line),2)))
           self.angle_flux[e_group].append(float(tokenize(delimit(line),4)))
           self.angle_flux_error[e_group].append(float(tokenize(delimit(line),6)))
        if num_angles%2 == 1:
           line = self.f.readline()
           self.angle_flux[e_group].append(float(tokenize(delimit(line),0)))
           self.angle_flux_error[e_group].append(float(tokenize(delimit(line),2)))

        # read one blank
        line = self.f.readline()

    def read_usrbdx(self):
        line = self.f.readline()

        # detector 
        self.detector_number = int(tokenize(delimit(line),2))
        self.detector_name = tokenize(delimit(line),6)

        line = self.f.readline()

        # area
        self.area = float(tokenize(delimit(line),1))
        line = self.f.readline()

        # dist scored
        self.distribution = int(tokenize(delimit(line),2))
        line = self.f.readline()

        # read from and to reg
        self.from_reg = int(tokenize(delimit(line),2))
        self.to_reg = int(tokenize(delimit(line),4))
        line = self.f.readline()

        # one way scoring?
        if delimit(line) == "one way scoring":
            self.two_way = False

        # read the total fluxes
        self.read_total_fluxes()           

        line = self.f.readline()
        # now read until "Double diff."
        # advance file until double diff found

        while line.find("Double diff.") < 0:
            line = self.f.readline()

        for i in range(2):
            line = self.f.readline()
        # on line solid angle minium
        line = self.f.readline()
        self.solid_angle_boundaries.append(float(tokenize(delimit(line),5)))
        for i in range(3):
            line = self.f.readline()
        # now on first line of data
        line = self.f.readline()
        while len(delimit(line).split( )) >  0: 
            self.solid_angle_boundaries.extend(delimit(line).split( ))
            line = self.f.readline()
        line = self.f.readline()
        self.angle_boundaries.append(float(tokenize(delimit(line),4)))
        # read 3 blanks
        for i in range(3):
            line = self.f.readline()
        # now on first line of data
        line = self.f.readline()
        while len(delimit(line).split( )) >  0: 
            self.angle_boundaries.extend(delimit(line).split( ))
            line = self.f.readline()

        line = self.f.readline()
        for i in range(len(self.e_bounds)-1):
            # size arrays appropriately
            self.angle_flux.append([])
            self.angle_flux_error.append([])
            self.solid_angle_flux.append([])
            self.solid_angle_flux_error.append([])
            self.read_angle_flux(i)



#data1 = UsrbdxFile()
#data1.read_file("mars_stable_28_sum.lis")
#data2 = UsrbdxFile()
#data2.read_file("mars_stable_28_sum.lis")
            
#data = Ave(data1,data2)
#data3 = data.get_ave()
#for item in data3.scorers.keys():
#    print item, data3.scorers[item].total_response, data3.scorers[item].total_response_error



    

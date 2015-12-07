import numpy as np
import string
from math import exp,log
#
mars_radius = 3.4895E8 # in cm 
total_atmos_radius = 3.4895E8 + 1.5E7 # in cm  

# this function returns density given some height
def density (height):
    scale_height = 10.1*1000*100 # scale height in cm
    atmos_dens = 0.00002
    density = atmos_dens * exp ( -height/scale_height)
    return density

# this function returns the height given a starting height and a farctional density
def fractional_change(fraction,start_height):
    atmos_dens = 0.00002
    scale_height = 10.1*1000*100
    old_density = density(start_height)
    new_density = fraction * old_density 
    radius = -1 * scale_height * log(new_density/atmos_dens)
#    radius = -1. * scale_height * log( fraction * exp(-1.0*start_height/scale_height))
    # radius = -1.*scale_height * log(fraction * density(start_height)/atmos_dens)
    return radius

# this function split the atmosphere layers 
def split_layers(): 
   radius = 0
   radii = []
   while ( radius < 1.6E7 and density(radius) > 9.9e-9 ):
	radii.append(radius)
	radius = fractional_change(0.99,radius)
   return radii


# this funtion gives the average density of a layer
def avg_density():
   radii = split_layers()
   density_avg = []
   for i in radii:
      mean_density= (-20.2*exp(-(i+1)/(10.1*1000*100)) + 20.2*exp(-(i)/(10.1*1000*100)))/((i+1)-i)
      density_avg.append(mean_density)

   return density_avg

# this function return the radius of each atmosphere as input geometry for flair
def atmosphere_radius():
   layer = split_layers()
   radius = [x + mars_radius for x in layer]
   a = 1
   for i in radius[1:]:
      line = ""
      line += "SPH "
      name = "ATMOS"+str(a) 
      line += width10(name,"left")
      line += " 0.0 0.0 -3.4895E8 "
      line += str(i) 
      print line
      a = a+1
   
# this function prints the input to form the reagions of each atmophere assuming
# the first atmosphere is already defined
def region():
   a = 2
   b = 1
   layer = split_layers()
   print "ATMOS1       5 -AT_CUT +ATMOS1 -MARS"
   for i in layer[2:]:
      line =""
      name = "ATMOS"+str(a)
      line += width10(name,"left")
      line += "   5 -AT_CUT +ATMOS"+str(a)
      line += " -ATMOS"+str(b)
      print line 

      a = a+1
      b = b+1
 
   line1 = ""
   name1 = "ATMOS"+str(a)
   line1 += width10(name1,"left")
   line1 += "   5 -AT_CUT +TOPATMOS"
   line1 += " -ATMOS"+str(b)
   print line1


# this function density card for each layer
def density_input():
   a = 41
   b = 1
   density = avg_density()
   for i in density[:-1]:
      line1 = ""
      line2 = ""
      line3 = ""
      line4 = ""
      line5 = ""

      line1 += width10("MATERIAL","left")
      line1 += width10("","right")
      line1 += width10("","right")
      line1 += width10('%.4E'%i,"right")
      name = str(a)+'.'
      line1 += width10(name,"right")
      line1 += width10("","right")
      line1 += width10("","right")
      line1 += "ATMOS"+str(b)

      line2 += width10("COMPOUND","left")
      line2 += width10("-.01017","right")
      line2 += width10("HYDROGEN","right")
      line2 += width10("-.004817","right")
      line2 += width10("HYDROG-1","right")
      line2 += width10("-.009626","right")
      line2 += width10("DEUTERIU","right")
      line2 += "ATMOS"+str(b)

      line3 += width10("COMPOUND","left") 
      line3 += width10("-.06379","right")  
      line3 += width10("CARBON","right")
      line3 += width10("-.1333","right")
      line3 += width10("NEON","right")  
      line3 += width10("-.4146","right")  
      line3 += width10("OXYGEN","right")
      line3 += "ATMOS"+str(b)

      line4 += width10("COMPOUND","left")
      line4 += width10("-.09091","right")  
      line4 += width10("NEON","right")
      line4 += width10("-.09091","right")
      line4 += width10("ARGON","right")      
      line4 += width10("-.09091","right")    
      line4 += width10("KRYPTON","right")
      line4 += "ATMOS"+str(b)

      line5 += width10("COMPOUND","left")
      line5 += width10("-.09091","right")
      line5 += width10("XENON","right")
      line5 += width10("","right")
      line5 += width10("","right")
      line5 += width10("","right")
      line5 += width10("","right")
      line5 += "ATMOS"+str(b)

      print line1
      print line2
      print line3
      print line4
      print line5

      a = a + 1
      b = b + 1


# line formatter
def width10(input,side):
    if side == "left":
     return str(input)[0:10].ljust(10)
    if side == "right":
     return str(input)[0:10].rjust(10)

# This function
def assign_density():
   density = avg_density()
   a = 1
   for i in density[:-1]:
       line = ""
       line += width10("ASSIGNMA","left")
       name = "ATMOS"+str(a)
       line += width10(name,"right")
       line += width10(name,"right")
       # increment a
       a+=1
       print line
   line2 = ""
   line2 += width10("ASSIGNMA","left")
   name2 = "ATMOS"+str(a)
   line2 += width10("VACUUM","right")
   line2 += width10(name2,"right")
   print line2

# this function creates a proton  USRBDX for each layer
def proton_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("PROTON","right")
   line += width10("-25.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_pro"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("PROTON","right")
   line2 += width10("-25.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_pro"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("PROTON","right")
      line3 += width10("-25.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_pro"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1
     
# this function creates a neutron  USRBDX for each layer
def neutron_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("NEUTRON","right")
   line += width10("-26.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_neu"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("NEUTRON","right")
   line2 += width10("-26.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_neu"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("NEUTRON","right")
      line3 += width10("-26.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_neu"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

# this function creates a electron USRBDX for each layer
def electron_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("ELECTRON","right")
   line += width10("-27.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_e"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("ELECTRON","right")
   line2 += width10("-27.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_e"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("ELECTRON","right")
      line3 += width10("-27.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_e"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

# this function creates a muon  USRBDX for each layer
def muons_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("MUONS","right")
   line += width10("-28.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_mu"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("MUONS","right")
   line2 += width10("-28.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_mu"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("MUONS","right")
      line3 += width10("-28.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_mu"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

# this function creates a photon  USRBDX for each layer
def photon_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("PHOTON","right")
   line += width10("-29.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_pho"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("PHOTON","right")
   line2 += width10("-29.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_pho"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("PHOTON","right")
      line3 += width10("-29.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_pho"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

# this function creates a helium3 USRBDX for each layer
def helium3_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("3-HELIUM","right")
   line += width10("-30.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_he3"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("3-HELIUM","right")
   line2 += width10("-30.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_he3"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("3-HELIUM","right")
      line3 += width10("-30.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_he3"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

# this function creates a helium4 USRBDX for each layer
def helium4_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("4-HELIUM","right")
   line += width10("-31.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_he4"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("4-HELIUM","right")
   line2 += width10("-31.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_he4"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("4-HELIUM","right")
      line3 += width10("-31.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_he4"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

# this function creates a triton USRBDX for each layer
def triton_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("TRITON","right")
   line += width10("-32.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_tri"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("TRITON","right")
   line2 += width10("-32.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_tri"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("TRITON","right")
      line3 += width10("-32.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_tri"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

# this function creates a deuteron USRBDX for each layer
def deuteron_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("DEUTERON","right")
   line += width10("-33.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_deu"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("DEUTERON","right")
   line2 += width10("-33.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_deu"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("DEUTERON","right")
      line3 += width10("-33.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_deu"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

# this function creates a heavyion USRBDX for each layer
def heavyion_usrbdx():
   density = avg_density()
   line = ""
   line1 = ""
   line2 = ""
   line += width10("USRBDX","left")
   line += width10("109.","right")
   line += width10("HEAVYION","right")
   line += width10("-34.","right")
   line += width10("GROUND","right")
   line += width10("ATMOS1","right")
   line += width10("1.","right")
   line += "GtoAT1_h"

   line1 += width10("USRBDX","left")
   line1 += width10("1.","right")
   line1 += width10("1E-6","right")
   line1 += width10("1000.","right")
   line1 += width10("6.28318531","right")
   line1 += width10("0.0","right")
   line1 += width10("1.","right")
   line1 += " &"

   line2 += width10("USRBDX","left")
   line2 += width10("109.","right")
   line2 += width10("HEAVYION","right")
   line2 += width10("-34.","right")
   line2 += width10("ATMOS1","right")
   line2 += width10("GROUND","right")
   line2 += width10("1.","right")
   line2 += "AT1toG_h"

   print line
   print line1
   print line2
   print line1

   a = 1
   for i in density[:-1]:
      line3 = ""
      line4 = ""
      line3 += width10("USRBDX","left")
      line3 += width10("109.","right")
      line3 += width10("HEAVYION","right")
      line3 += width10("-34.","right")
      name = "ATMOS"+str(a+1)
      line3 += width10(name,"right")
      name1 = "ATMOS"+str(a)
      line3 += width10(name1,"right")
      line3 += width10("1.","right")
      name2 = "A"+str(a+1)+ "t"+str(a)+"_h"
      line3 += width10(name2,"left")

      line4 += width10("USRBDX","left")
      line4 += width10("1.","right")
      line4 += width10("1E-6","right")
      line4 += width10("1000.","right")
      line4 += width10("6.28318531","right")
      line4 += width10("0.0","right")
      line4 += width10("1.","right")
      line4 += " &"

      print line3
      print line4

      a += 1

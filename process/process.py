from read_usrbdx import *

data1 = UsrbdxFile()
data1.read_file("1/mars_stable_28_sum.lis")
data2 = UsrbdxFile()
data2.read_file("2/mars_stable_28_sum.lis")
data3 = UsrbdxFile()
data3.read_file("3/mars_stable_28_sum.lis")

data = AveAdd(data1,data2,0.84156,0.144872)
data5 = data.get_sum()

data = AveAdd(data3,data5,1,0.000625099)
data = data.get_sum()

for item in data.scorers.keys():
    print item, data.scorers[item].total_response, data.scorers[item].total_response_error, data5.scorers[item].total_response,data5.scorers[item].total_response_error






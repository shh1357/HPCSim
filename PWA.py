'''
Created on 2015/08/01

@author: smallcat
'''

import os
import pandas as pd

# print os.getcwd()

#archive = "CEA-Curie-2011-2.1-cln.swf"
#archive = "workloads/LLNL-Thunder-2007-1.1-cln.swf"
# archive = "LLNL-Atlas-2006-2.1-cln.swf"
# archive = "LPC-EGEE-2004-1.2-cln.swf"
# archive = "SDSC-DS-2004-2.1-cln.swf"
# archive = "KTH-SP2-1996-2.1-cln.swf"
# archive = "Sandia-Ross-2001-1.1-cln.swf"
# archive = "SDSC-Par-1996-3.1-cln.swf"
# archive = "SDSC-Par-1995-3.1-cln.swf"
# archive = "LANL-CM5-1994-4.1-cln.swf"
archive = "workloads/UniLu-Gaia-2014-2.swf"

names = ["Job Number",
         "Submit Time",
         "Wait Time",
         "Run Time",
         "Number of Allocated Processors",
         "Average CPU Time Used",
         "Used Memory",
         "Requested Number of Processors",
         "Requested Time",
         "Requested Memory",
         "Status",
         "User ID",
         "Group ID",
         "Executable (Application) Number",
         "Queue Number",
         "Partition Number",
         "Preceding Job Number",
         "Think Time from Preceding Job"]

# data = pd.read_csv(archive, comment=";", sep="\s+", header=None)

data = pd.read_csv(archive, comment=";", sep="\s+", names=names)

# print len(data)
# print max(data["Requested Number of Processors"])
# print max(data["Requested Time"])
# print max(data["Run Time"])
# print max(data["Number of Allocated Processors"])
# print data["Number of Allocated Processors"][48]
# print data["Number of Allocated Processors"][10000]
# t = len(data)
# t=1000
# c1 = 0
# c2 = 0
# c4 = 0
# c8 = 0
# c16 = 0
# c32 = 0
# c64 = 0
# c128 = 0
# c256 = 0
# c512 = 0
# c516 = 0 
# for i in range(t):
#     if (data["Number of Allocated Processors"][i]<2):
#         c1 = c1+1
#     if (data["Number of Allocated Processors"][i]<3):
#         c2 = c2+1
#     if (data["Number of Allocated Processors"][i]<5):
#         c4 = c4+1  
#     if (data["Number of Allocated Processors"][i]<9):
#         c8 = c8+1 
#     if (data["Number of Allocated Processors"][i]<17):
#         c16 = c16+1  
#     if (data["Number of Allocated Processors"][i]<33):
#         c32 = c32+1  
#     if (data["Number of Allocated Processors"][i]<65):
#         c64 = c64+1  
#     if (data["Number of Allocated Processors"][i]<129):
#         c128 = c128+1
#     if (data["Number of Allocated Processors"][i]<257):
#         c256 = c256+1  
#     if (data["Number of Allocated Processors"][i]<513):
#         c512 = c512+1    
#     if (data["Number of Allocated Processors"][i]<517):
#         c516 = c516+1                                                               
# print c1, " : 1 : ", float(c1)/t
# print c2, " : 2 : ", float(c2)/t
# print c4, " : 4 : ", float(c4)/t
# print c8, " : 8 : ", float(c8)/t
# print c16, " : 16 : ", float(c16)/t
# print c32, " : 32 : ", float(c32)/t
# print c64, " : 64 : ", float(c64)/t
# print c128, " : 128 : ", float(c128)/t
# print c256, " : 256 : ", float(c256)/t
# print c512, " : 512 : ", float(c512)/t
# print c516, " : 516 : ", float(c516)/t

# columns = []
# for col in range(len(data.columns)):
#     columns.append(col)
# print columns
# print data[columns].mean(axis=0)

'''
Created on 2016/05/22

@author: smallcat
'''

import os
import pandas as pd

#print os.getcwd()

# archive = "workloads/CEA-Curie-2011-2.1-cln.swf"
# archive = "workloads/LLNL-Thunder-2007-1.1-cln.swf"
# archive = "workloads/LLNL-Atlas-2006-2.1-cln.swf"
# archive = "workloads/LPC-EGEE-2004-1.2-cln.swf"
# archive = "workloads/SDSC-DS-2004-2.1-cln.swf"
# archive = "workloads/KTH-SP2-1996-2.1-cln.swf"
# archive = "workloads/Sandia-Ross-2001-1.1-cln.swf"
# archive = "workloads/SDSC-Par-1996-3.1-cln.swf"
# archive = "workloads/SDSC-Par-1995-3.1-cln.swf"
# archive = "workloads/LANL-CM5-1994-4.1-cln.swf"

# archive = "workloads/NASA-iPSC-1993-3.1-cln.swf"
# archive = "workloads/CTC-SP2-1996-3.1-cln.swf"
# archive = "workloads/SDSC-SP2-1998-4.2-cln.swf"
# archive = "workloads/OSC-Clust-2000-3.1-cln.swf"
# archive = "workloads/HPC2N-2002-2.2-cln.swf"
# archive = "workloads/METACENTRUM-2009-2.swf"

# archive = "workloads/wagap1-10-2013.swf" #cerit13 CERIT-SC_2013
# archive = "workloads/meta1-6-2013.swf" #meta13 MetaCentrum_2013
# archive = "workloads/RICC-2010-2.swf"
# archive = "workloads/CEA-Curie-2011-2.1-clncln.swf"
# archive = "workloads/ANL-Intrepid-2009-1.swf" 
archive = "workloads/METACENTRUM-2013-3.swf" 

#archive = "workloads/2016-05-22-21-53-28-336000_200_jobs"
#archive = "workloads/2016-05-22-21-53-28-422000_2000_jobs"
#archive = "workloads/2016-05-25-14-50-16-446000_2000_jobs"
#archive = "workloads/2016-05-25-14-50-16-479000_4000_jobs"
#archive = "workloads/2016-05-25-14-50-16-516000_6000_jobs"
#archive = "workloads/2016-05-25-14-50-16-556000_8000_jobs"
#archive = "workloads/2016-05-25-14-50-16-601000_10000_jobs"
#archive = "workloads/2016-05-25-14-50-16-899000_20000_jobs"
#archive = "workloads/2016-06-08-16-34-13-159000_1000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-177000_2000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-216000_3000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-262000_4000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-322000_5000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-398000_6000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-490000_7000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-588000_8000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-709000_9000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-13-835000_10000_jobs_poisson"
#archive = "workloads/2016-06-08-16-34-14-143000_12000_jobs_poisson"

#archive = "workloads/2016-09-20-15-42-15-032000_10000_npb_jobs"
#archive = "workloads/2016-09-20-15-42-14-174000_2000_npb_jobs"

#archive = "workloads/2019-07-04-22-51-02-148359_100_npb_jobs"
#archive = "workloads/2019-07-04-22-51-02-150542_200_npb_jobs"
#archive = "workloads/2019-07-04-22-51-02-152864_300_npb_jobs"
#archive = "workloads/2019-07-04-22-51-02-155851_400_npb_jobs"
#archive = "workloads/2019-07-04-22-51-02-159931_500_npb_jobs"
#archive = "workloads/2019-07-04-22-51-02-165898_600_npb_jobs"
#archive = "workloads/2019-07-04-22-51-02-173288_700_npb_jobs"
#archive = "workloads/2019-07-04-22-51-02-181238_800_npb_jobs"
#archive = "workloads/2019-07-04-22-51-02-189737_900_npb_jobs"
#archive = "workloads/2019-07-03-16-05-54-369066_1000_npb_jobs"
#archive = "workloads/2019-07-03-16-05-54-380715_2000_npb_jobs"

edgelist = ""
#edgelist = "edges/Torus1024_conventional"
#edgelist = "edges/Torus1024_disaggregateA"
#edgelist = "edges/Torus1024_disaggregateB"
#edgelist = "edges/Torus1024_disaggregateC"

#edgelist = "edges/Torus1024_conventional_1s1h"
#edgelist = "edges/Torus1024_disaggregateB_1s1h"
#edgelist = "edges/Torus1024_disaggregateC_1s1h"

# names = ["job_number", 
#          "cpu#", 
#          "ssd#", 
#          "gpu#", 
#          "submit", 
#          "runtime"]

names = ["job_number", 
         "cpu#", 
         "ssd#", 
         "gpu#", 
         "submit", 
         "runtime",
         "npb"]

pwa_names = ["Job Number", 
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
         "Think Time from Preceding Job",
         "plus0",
         "plus1",
         "plus2"]
 
# data = pd.read_csv(archive, comment=";", sep="\s+", header=None)

data = pd.read_csv(archive, comment=";", sep="\s+", names=names) 
pwa_data = pd.read_csv(archive, comment=";", sep="\s+", names=pwa_names) 
num = len(pwa_data)

# print len(data)
# print max(data["Requested Number of Processors"])
# print max(data["Requested Time"])
# print max(data["Run Time"])
# print max(data["Number of Allocated Processors"])
# print data["Number of Allocated Processors"][48]
# print data["Number of Allocated Processors"][10000]
# t = len(data)

def cdf_nodes(t):
    #t = 1000
    c = 0
    c1 = 0
    c2 = 0
    c4 = 0
    c8 = 0
    c16 = 0
    c32 = 0
    c64 = 0
    c128 = 0
    c256 = 0
    c512 = 0
    c1024 = 0 
    c2048 = 0 
    c4096 = 0 
    c8192 = 0 
    for i in range(t):
        if pwa_data["Number of Allocated Processors"][i] > 0:
            c = c + 1
            if (pwa_data["Number of Allocated Processors"][i] < 2):
                c1 = c1 + 1
            if (pwa_data["Number of Allocated Processors"][i] < 3):
                c2 = c2 + 1
            if (pwa_data["Number of Allocated Processors"][i] < 5):
                c4 = c4 + 1  
            if (pwa_data["Number of Allocated Processors"][i] < 9):
                c8 = c8 + 1 
            if (pwa_data["Number of Allocated Processors"][i] < 17):
                c16 = c16 + 1  
            if (pwa_data["Number of Allocated Processors"][i] < 33):
                c32 = c32 + 1  
            if (pwa_data["Number of Allocated Processors"][i] < 65):
                c64 = c64 + 1  
            if (pwa_data["Number of Allocated Processors"][i] < 129):
                c128 = c128 + 1
            if (pwa_data["Number of Allocated Processors"][i] < 257):
                c256 = c256 + 1  
            if (pwa_data["Number of Allocated Processors"][i] < 513):
                c512 = c512 + 1    
            if (pwa_data["Number of Allocated Processors"][i] < 1025):
                c1024 = c1024 + 1           
            if (pwa_data["Number of Allocated Processors"][i] < 2049):
                c2048 = c2048 + 1      
            if (pwa_data["Number of Allocated Processors"][i] < 4097):
                c4096 = c4096 + 1      
            if (pwa_data["Number of Allocated Processors"][i] < 8193):
                c8192 = c8192 + 1                                                                                 
    print c1, " : 1 : ", float(c1)/c
    print c2, " : 2 : ", float(c2)/c
    print c4, " : 4 : ", float(c4)/c
    print c8, " : 8 : ", float(c8)/c
    print c16, " : 16 : ", float(c16)/c
    print c32, " : 32 : ", float(c32)/c
    print c64, " : 64 : ", float(c64)/c
    print c128, " : 128 : ", float(c128)/c
    print c256, " : 256 : ", float(c256)/c
    print c512, " : 512 : ", float(c512)/c
    print c1024, " : 1024 : ", float(c1024)/c
    print c2048, " : 2048 : ", float(c2048)/c
    print c4096, " : 4096 : ", float(c4096)/c
    print c8192, " : 8192 : ", float(c8192)/c

# columns = []
# for col in range(len(data.columns)):
#     columns.append(col)
# print columns
#print data[columns].mean(axis=0)

print num
cdf_nodes(num)

'''
Created on 2016/09/12

@author: smallcat
'''

import datetime
import random

# makespan = 1000
    
def generate_n_jobs(n, makespan):
    dt = str(datetime.datetime.now())
    dt = dt.replace(" ", "-")
    dt = dt.replace(".", "-")
    dt = dt.replace(":", "-")
    fn = dt + "_" + str(n) + "_jobs"
    f = open(fn, "w")  
    f.write(";job_number  cpu#  ssd#  gpu#  submit  runtime\n")   
    submits = []
    for i in range(n):
        submits.append(random.uniform(0,makespan))
    submits.sort()
    for i in range(n):
        cpu_unit = random.randint(1,25)
        ssd_unit = random.randint(0,cpu_unit)
        gpu_unit = random.randint(0,cpu_unit)
        runtime = random.randint(1,10)
        s = str(i+1) + "    " + str(cpu_unit) + "    " + str(ssd_unit) + "    " + str(gpu_unit) + "    " + str(submits[i]) + "    " + str(runtime) + "\n"
        f.write(s)
    f.close()
    
#generate_n_jobs(2000, 1000)
#generate_n_jobs(1200, 1000)
#generate_n_jobs(1400, 1000)
#generate_n_jobs(1600, 1000)
#generate_n_jobs(1800, 1000)

def generate_jobs(makespan):
    n = 2000
    submits = []
    jobs = {}
    while n < 20001:   
        dt = str(datetime.datetime.now())
        dt = dt.replace(" ", "-")
        dt = dt.replace(".", "-")
        dt = dt.replace(":", "-")
        fn = dt + "_" + str(n) + "_jobs"
        f = open(fn, "w")  
        f.write(";job_number  cpu#  ssd#  gpu#  submit  runtime\n")    
        for i in range(2000):
            time = random.uniform(0,makespan)
            submits.append(time)
        submits.sort()
        for i in range(n):
            s = ""
            time = submits[i]
            if time in jobs:
                s = jobs[time] 
                s = str(i+1) + "    " + s.split("    ", 1)[1]
            else:
                cpu_unit = random.randint(1,25)
                ssd_unit = random.randint(0,cpu_unit)
                gpu_unit = random.randint(0,cpu_unit)
                runtime = random.randint(1,10)
                s = str(i+1) + "    " + str(cpu_unit) + "    " + str(ssd_unit) + "    " + str(gpu_unit) + "    " + str(time) + "    " + str(runtime) + "\n"
                jobs[time] = s
            f.write(s)
        f.close()
        n = n + 2000
        
#generate_jobs(1000)

def generate_jobs_poisson(makespan):
    n = 1000
    while n < 20001:   
        dt = str(datetime.datetime.now())
        dt = dt.replace(" ", "-")
        dt = dt.replace(".", "-")
        dt = dt.replace(":", "-")
        fn = dt + "_" + str(n) + "_jobs_poisson"
        f = open(fn, "w")  
        f.write(";job_number  cpu#  ssd#  gpu#  submit  runtime\n") 
        time = 0.0   
        for i in range(n):
            time += random.expovariate(n/float(makespan))
            cpu_unit = random.randint(1,25)
            ssd_unit = random.randint(0,cpu_unit)
            gpu_unit = random.randint(0,cpu_unit)
            runtime = random.randint(1,10)/10.0
            s = str(i+1) + "    " + str(cpu_unit) + "    " + str(ssd_unit) + "    " + str(gpu_unit) + "    " + str(time) + "    " + str(runtime) + "\n"
            f.write(s)
        f.close()
        n = n + 1000

#generate_jobs_poisson(100)

def generate_npb_jobs(makespan):
    n = 1000
    while n < 20001:      
        dt = str(datetime.datetime.now())
        dt = dt.replace(" ", "-")
        dt = dt.replace(".", "-")
        dt = dt.replace(":", "-")
        fn = dt + "_" + str(n) + "_npb_jobs"
        f = open(fn, "w")  
        f.write(";job_number  cpu#  ssd#  gpu#  submit  runtime  npb\n") 
        time = 0.0   
        for i in range(n):
            time += random.expovariate(n/float(makespan))
            cpu_unit = random.sample([4, 16, 64, 256], 1)[0]
            ssd_unit = random.randint(0, cpu_unit)
            gpu_unit = random.randint(0, cpu_unit)
            runtime = ""
            npb = random.sample(["FT", "IS", "CG", "BT", "SP", "MG", "MM"], 1)[0]
            if cpu_unit == 256 and npb == "IS":
                cpu_unit = random.sample([4, 16, 64], 1)[0]
                ssd_unit = random.randint(0, cpu_unit)
                gpu_unit = random.randint(0, cpu_unit)
            if cpu_unit == 4:
                if npb == "FT":
                    runtime = "2mesh:0.1010:0.1011:0.1013:0.1014:2torus:0.1010:0.1011:0.1013:0.1014:random:0.0832:0.0834:0.0836:0.0838"
                if npb == "IS":
                    runtime = "2mesh:0.0302:0.0302:0.0303:0.0303:2torus:0.0302:0.0302:0.0303:0.0303:random:0.0284:0.0284:0.0284:0.0284"  
                if npb == "CG":
                    runtime = "2mesh:0.6207:0.6243:0.6279:0.6315:2torus:0.6207:0.6243:0.6279:0.6315:random:0.5956:0.5984:0.6011:0.6039"  
                if npb == "BT":
                    runtime = "2mesh:0.9252:0.9286:0.9314:0.9341:2torus:0.9252:0.9287:0.9314:0.9341:random:0.6452:0.6477:0.6501:0.6526"
                if npb == "SP":
                    runtime = "2mesh:1.6023:1.6049:1.6074:1.6100:2torus:1.6023:1.6049:1.6074:1.6100:random:1.1283:1.1322:1.1357:1.1396"
                if npb == "MG":
                    runtime = "2mesh:0.0701:0.0704:0.0707:0.0710:2torus:0.0701:0.0704:0.0707:0.0710:random:0.0522:0.0526:0.0529:0.0533"
                if npb == "MM":
                    runtime = "2mesh:0.0059:0.0059:0.0059:0.0059:2torus:0.0059:0.0059:0.0059:0.0059:random:0.0059:0.0059:0.0059:0.0060"      
            if cpu_unit == 16:
                if npb == "FT":
                    runtime = "2mesh:0.0534:0.0535:0.0537:0.0539:3mesh:0.0435:0.0436:0.0438:0.0441:3torus:0.0539:0.0539:0.0541:0.0541:random:0.0297:0.0299:0.0300:0.0302"
                if npb == "IS":
                    runtime = "2mesh:0.0173:0.0173:0.0173:0.0173:3mesh:0.0132:0.0132:0.0132:0.0133:3torus:0.0166:0.0167:0.0167:0.0167:random:0.0098:0.0099:0.0099:0.0099"  
                if npb == "CG":
                    runtime = "2mesh:0.9127:0.9210:0.9294:0.9377:3mesh:0.9185:0.9263:0.9347:0.9431:3torus:0.9779:0.9857:0.9936:1.0015:random:0.8805:0.8836:0.8867:0.8895"  
                if npb == "BT":
                    runtime = "2mesh:1.0200:1.0201:1.0211:1.0231:3mesh:0.5332:0.5342:0.5366:0.5360:3torus:0.5363:0.5378:0.5394:0.5408:random:0.4243:0.4253:0.4263:0.4284"
                if npb == "SP":
                    runtime = "2mesh:1.8337:1.8339:1.8361:1.8354:3mesh:0.9748:0.9757:0.9775:0.9801:3torus:0.9644:0.9670:0.9694:0.9718:random:0.7616:0.7662:0.7709:0.7753"
                if npb == "MG":
                    runtime = "2mesh:0.0275:0.0281:0.0287:0.0293:3mesh:0.0322:0.0327:0.0332:0.0338:3torus:0.0320:0.0325:0.0329:0.0333:random:0.0285:0.0290:0.0296:0.0301"
                if npb == "MM":
                    runtime = "2mesh:0.0487:0.0488:0.0489:0.0490:3mesh:0.0432:0.0433:0.0433:0.0434:3torus:0.0435:0.0437:0.0438:0.0436:random:0.0429:0.0431:0.0432:0.0434"     
            if cpu_unit == 64:
                if npb == "FT":
                    runtime = "2mesh:0.0298:0.0303:0.0307:0.0311:3mesh:0.0200:0.0236:0.0238:0.0240:3torus:0.0296:0.0298:0.0230:0.0302:random:0.0125:0.0128:0.0131:0.0135"
                if npb == "IS":
                    runtime = "2mesh:0.0123:0.0123:0.0124:0.0124:3mesh:0.0105:0.0105:0.0106:0.0106:3torus:0.0120:0.0120:0.0120:0.0121:random:0.0055:0.0055:0.0056:0.0056"  
                if npb == "CG":
                    runtime = "2mesh:1.1700:1.1766:1.1833:1.1899:3mesh:1.0875:1.0941:1.1006:1.1072:3torus:1.2793:1.2850:1.2908:1.2965:random:0.9446:0.9510:0.9575:0.9639"  
                if npb == "BT":
                    runtime = "2mesh:1.2038:1.2054:1.2070:1.2082:3mesh:0.3817:0.3875:0.3926:0.4015:3torus:0.2741:0.2801:0.2853:0.2903:random:0.4167:0.4201:0.4242:0.4299"
                if npb == "SP":
                    runtime = "2mesh:1.9574:1.9607:1.9646:1.9695:3mesh:0.6189:0.6357:0.6474:0.6609:3torus:0.4629:0.4709:0.4794:0.4871:random:0.6779:0.6832:0.6889:0.6958"
                if npb == "MG":
                    runtime = "2mesh:0.0179:0.0191:0.0203:0.0216:3mesh:0.0285:0.0293:0.0301:0.0309:3torus:0.0275:0.0282:0.0288:0.0294:random:0.0234:0.0241:0.0247:0.0254"
                if npb == "MM":
                    runtime = "2mesh:0.4266:0.4276:0.4266:0.4266:3mesh:0.2932:0.2935:0.2929:0.2950:3torus:0.2713:0.2712:0.2713:0.2717:random:0.1855:0.1881:0.1865:0.1872"  
            if cpu_unit == 256:
                if npb == "FT":
                    runtime = "2mesh:0.0140:0.0141:0.0141:0.0142:3mesh:0.0072:0.0073:0.0073:0.0074:3torus:0.0120:0.0121:0.0121:0.0122:random:0.0057:0.0057:0.0057:0.0058"
    #             if npb == "IS":
    #                 runtime = ""  
                if npb == "CG":
                    runtime = "2mesh:1.3573:1.3700:1.3825:1.3951:3mesh:0.8811:0.8939:0.9019:0.9103:3torus:0.7643:0.7729:0.7810:0.7887:random:0.7528:0.7683:0.7774:0.7890"  
                if npb == "BT":
                    runtime = "2mesh:1.5466:1.5680:1.5915:1.6179:3mesh:0.5555:0.5797:0.6066:0.6329:3torus:0.3371:0.3465:0.3557:0.3652:random:0.4221:0.4344:0.4475:0.4594"
                if npb == "SP":
                    runtime = "2mesh:2.1815:2.1587:2.2090:2.2553:3mesh:0.7435:0.8147:0.8833:0.9604:3torus:0.5051:0.5297:0.5560:0.5830:random:0.6189:0.6486:0.6811:0.7162"
                if npb == "MG":
                    runtime = "2mesh:0.0163:0.0196:0.0222:0.0244:3mesh:0.0250:0.0263:0.0276:0.0289:3torus:0.0257:0.0267:0.0276:0.0287:random:0.0177:0.0187:0.0198:0.0209"
                if npb == "MM":
                    runtime = "2mesh:4.0320:4.0311:4.0317:4.0357:3mesh:1.8990:1.9062:1.9090:1.9104:3torus:1.8457:1.8438:1.8419:1.8476:random:0.8000:0.8078:0.8087:0.8114"                                                                                                                               
            s = str(i+1) + "    " + str(cpu_unit) + "    " + str(ssd_unit) + "    " + str(gpu_unit) + "    " + str(time) + "    " + str(runtime) + "    " + str(npb) + "\n"
            f.write(s)
        f.close()
        n = n + 1000

generate_npb_jobs(100)
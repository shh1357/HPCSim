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
    fn = "workloads/" + dt + "_" + str(n) + "_jobs"
    f = open(fn, "w")
    f.write(";job_number  cpu#  ssd#  gpu#  submit  runtime\n")
    submits = []
    for i in range(n):
        submits.append(random.uniform(0, makespan))
    submits.sort()
    for i in range(n):
        cpu_unit = random.randint(1, 25)
        ssd_unit = random.randint(0, cpu_unit)
        gpu_unit = random.randint(0, cpu_unit)
        runtime = random.randint(1, 10)
        s = str(i + 1) + "    " + str(cpu_unit) + "    " + str(ssd_unit) + "    " + str(gpu_unit) + "    " + str(
            submits[i]) + "    " + str(runtime) + "\n"
        f.write(s)
    f.close()


# generate_n_jobs(2000, 1000)
# generate_n_jobs(1200, 1000)
# generate_n_jobs(1400, 1000)
# generate_n_jobs(1600, 1000)
# generate_n_jobs(1800, 1000)

def generate_jobs(makespan):
    n = 2000
    submits = []
    jobs = {}
    while n < 20001:
        dt = str(datetime.datetime.now())
        dt = dt.replace(" ", "-")
        dt = dt.replace(".", "-")
        dt = dt.replace(":", "-")
        fn = "workloads/" + dt + "_" + str(n) + "_jobs"
        f = open(fn, "w")
        f.write(";job_number  cpu#  ssd#  gpu#  submit  runtime\n")
        for i in range(2000):
            time = random.uniform(0, makespan)
            submits.append(time)
        submits.sort()
        for i in range(n):
            s = ""
            time = submits[i]
            if time in jobs:
                s = jobs[time]
                s = str(i + 1) + "    " + s.split("    ", 1)[1]
            else:
                cpu_unit = random.randint(1, 25)
                ssd_unit = random.randint(0, cpu_unit)
                gpu_unit = random.randint(0, cpu_unit)
                runtime = random.randint(1, 10)
                s = str(i + 1) + "    " + str(cpu_unit) + "    " + str(ssd_unit) + "    " + str(
                    gpu_unit) + "    " + str(time) + "    " + str(runtime) + "\n"
                jobs[time] = s
            f.write(s)
        f.close()
        n = n + 2000


# generate_jobs(1000)

def generate_jobs_poisson(makespan):
    n = 1000
    while n < 20001:
        dt = str(datetime.datetime.now())
        dt = dt.replace(" ", "-")
        dt = dt.replace(".", "-")
        dt = dt.replace(":", "-")
        fn = "workloads/" + dt + "_" + str(n) + "_jobs_poisson"
        f = open(fn, "w")
        f.write(";job_number  cpu#  ssd#  gpu#  submit  runtime\n")
        time = 0.0
        for i in range(n):
            time += random.expovariate(n / float(makespan))
            cpu_unit = random.randint(1, 25)
            ssd_unit = random.randint(0, cpu_unit)
            gpu_unit = random.randint(0, cpu_unit)
            runtime = random.randint(1, 10) / 10.0
            s = str(i + 1) + "    " + str(cpu_unit) + "    " + str(ssd_unit) + "    " + str(gpu_unit) + "    " + str(
                time) + "    " + str(runtime) + "\n"
            f.write(s)
        f.close()
        n = n + 1000


# generate_jobs_poisson(100)

def generate_npb_jobs(makespan):
    n = 100
    while n < 1000:
        dt = str(datetime.datetime.now())
        dt = dt.replace(" ", "-")
        dt = dt.replace(".", "-")
        dt = dt.replace(":", "-")
        fn = "workloads/" + dt + "_" + str(n) + "_npb_jobs"
        f = open(fn, "w")
        f.write(";job_number  cpu#  ssd#  gpu#  submit  runtime  npb\n")
        time = 0.0
        for i in range(n):
            time += random.expovariate(n / float(makespan))
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
                    runtime = "2mesh:0.1010:0.1011:0.1013:0.1014:2torus:0.1010:0.1011:0.1013:0.1014:random-4:0.0832:0.0834:0.0836:0.0838"
                if npb == "IS":
                    runtime = "2mesh:0.0302:0.0302:0.0303:0.0303:2torus:0.0302:0.0302:0.0303:0.0303:random-4:0.0284:0.0284:0.0284:0.0284"
                if npb == "CG":
                    runtime = "2mesh:0.6207:0.6243:0.6279:0.6315:2torus:0.6207:0.6243:0.6279:0.6315:random-4:0.5956:0.5984:0.6011:0.6039"
                if npb == "BT":
                    runtime = "2mesh:0.9252:0.9286:0.9314:0.9341:2torus:0.9252:0.9287:0.9314:0.9341:random-4:0.6452:0.6477:0.6501:0.6526"
                if npb == "SP":
                    runtime = "2mesh:1.6023:1.6049:1.6074:1.6100:2torus:1.6023:1.6049:1.6074:1.6100:random-4:1.1283:1.1322:1.1357:1.1396"
                if npb == "MG":
                    runtime = "2mesh:0.0701:0.0704:0.0707:0.0710:2torus:0.0701:0.0704:0.0707:0.0710:random-4:0.0522:0.0526:0.0529:0.0533"
                if npb == "MM":
                    runtime = "2mesh:0.0059:0.0059:0.0059:0.0059:2torus:0.0059:0.0059:0.0059:0.0059:random-4:0.0059:0.0059:0.0059:0.0060"
            if cpu_unit == 16:
                if npb == "FT":
                    runtime = "2mesh:0.0534:0.0535:0.0537:0.0539:2torus:0.0537:0.0538:0.0540:0.0540:3mesh:0.0435:0.0436:0.0438:0.0441:3torus:0.0539:0.0539:0.0541:0.0541:random-6:0.0297:0.0299:0.0300:0.0302:random-4:0.0336:0.0336:0.0338:0.0339"
                if npb == "IS":
                    runtime = "2mesh:0.0173:0.0173:0.0173:0.0173:2torus:0.0166:0.0166:0.0167:0.0167:3mesh:0.0132:0.0132:0.0132:0.0133:3torus:0.0166:0.0167:0.0167:0.0167:random-6:0.0098:0.0099:0.0099:0.0099:random-4:0.0100:0.0100:0.0101:0.0101"
                if npb == "CG":
                    runtime = "2mesh:0.9127:0.9210:0.9294:0.9377:2torus:0.7999:0.8078:0.8158:0.8238:3mesh:0.9185:0.9263:0.9347:0.9431:3torus:0.9779:0.9857:0.9936:1.0015:random-6:0.8805:0.8836:0.8867:0.8895:random-4:0.9461:0.9534:0.9609:0.9684"
                if npb == "BT":
                    runtime = "2mesh:1.0200:1.0201:1.0211:1.0231:2torus:0.9205:0.9216:0.9235:0.9257:3mesh:0.5332:0.5342:0.5366:0.5360:3torus:0.5363:0.5378:0.5394:0.5408:random-6:0.4243:0.4253:0.4263:0.4284:random-4:0.5163:0.5170:0.5180:0.5198"
                if npb == "SP":
                    runtime = "2mesh:1.8337:1.8339:1.8361:1.8354:2torus:1.6460:1.6482:1.6502:1.6520:3mesh:0.9748:0.9757:0.9775:0.9801:3torus:0.9644:0.9670:0.9694:0.9718:random-6:0.7616:0.7662:0.7709:0.7753:random-4:0.9244:0.9271:0.9297:0.9335"
                if npb == "MG":
                    runtime = "2mesh:0.0275:0.0281:0.0287:0.0293:2torus:0.0272:0.0276:0.0280:0.0284:3mesh:0.0322:0.0327:0.0332:0.0338:3torus:0.0320:0.0325:0.0329:0.0333:random-6:0.0285:0.0290:0.0296:0.0301:random-4:0.0321:0.0327:0.0332:0.0338"
                if npb == "MM":
                    runtime = "2mesh:0.0487:0.0488:0.0489:0.0490:2torus:0.0445:0.0447:0.0446:0.0447:3mesh:0.0432:0.0433:0.0433:0.0434:3torus:0.0435:0.0437:0.0438:0.0436:random-6:0.0429:0.0431:0.0432:0.0434:random-4:0.0430:0.0431:0.0431:0.0432"
            if cpu_unit == 64:
                if npb == "FT":
                    runtime = "2mesh:0.0298:0.0303:0.0307:0.0311:2torus:0.0243:0.0246:0.0247:0.0250:3mesh:0.0200:0.0236:0.0238:0.0240:3torus:0.0296:0.0298:0.0230:0.0302:random-6:0.0125:0.0128:0.0131:0.0135:random-4:0.0150:0.0151:0.0154:0.0158"
                if npb == "IS":
                    runtime = "2mesh:0.0123:0.0123:0.0124:0.0124:2torus:0.0103:0.0104:0.0104:0.0104:3mesh:0.0105:0.0105:0.0106:0.0106:3torus:0.0120:0.0120:0.0120:0.0121:random-6:0.0055:0.0055:0.0056:0.0056:random-4:0.0063:0.0063:0.0064:0.0064"
                if npb == "CG":
                    runtime = "2mesh:1.1700:1.1766:1.1833:1.1899:2torus:0.8939:0.8996:0.9054:0.9111:3mesh:1.0875:1.0941:1.1006:1.1072:3torus:1.2793:1.2850:1.2908:1.2965:random-6:0.9446:0.9510:0.9575:0.9639:random-4:1.0155:1.0234:1.0299:1.0361"
                if npb == "BT":
                    runtime = "2mesh:1.2038:1.2054:1.2070:1.2082:2torus:1.0940:1.0964:1.0988:1.1009:3mesh:0.3817:0.3875:0.3926:0.4015:3torus:0.2741:0.2801:0.2853:0.2903:random-6:0.4167:0.4201:0.4242:0.4299:random-4:0.5326:0.5344:0.5367:0.5405"
                if npb == "SP":
                    runtime = "2mesh:1.9574:1.9607:1.9646:1.9695:2torus:1.7729:1.7768:1.7808:1.7860:3mesh:0.6189:0.6357:0.6474:0.6609:3torus:0.4629:0.4709:0.4794:0.4871:random-6:0.6779:0.6832:0.6889:0.6958:random-4:0.8597:0.8651:0.8708:0.8769"
                if npb == "MG":
                    runtime = "2mesh:0.0179:0.0191:0.0203:0.0216:2torus:0.0170:0.0176:0.0182:0.0188:3mesh:0.0285:0.0293:0.0301:0.0309:3torus:0.0275:0.0282:0.0288:0.0294:random-6:0.0234:0.0241:0.0247:0.0254:random-4:0.0266:0.0270:0.0278:0.0287"
                if npb == "MM":
                    runtime = "2mesh:0.4266:0.4276:0.4266:0.4266:2torus:0.3295:0.3300:0.3291:0.3304:3mesh:0.2932:0.2935:0.2929:0.2950:3torus:0.2713:0.2712:0.2713:0.2717:random-6:0.1855:0.1881:0.1865:0.1872:random-4:0.2063:0.2051:0.2059:0.2059"
            if cpu_unit == 256:
                if npb == "FT":
                    runtime = "2mesh:0.0140:0.0141:0.0141:0.0142:2torus:0.0146:0.0149:0.0157:0.0158:3mesh:0.0072:0.0073:0.0073:0.0074:3torus:0.0120:0.0121:0.0121:0.0122:random-6:0.0057:0.0057:0.0057:0.0058:random-4:0.0076:0.0076:0.0076:0.0076"
                #             if npb == "IS":
                #                 runtime = ""
                if npb == "CG":
                    runtime = "2mesh:1.3573:1.3700:1.3825:1.3951:2torus:1.1242:1.1367:1.1501:1.1639:3mesh:0.8811:0.8939:0.9019:0.9103:3torus:0.7643:0.7729:0.7810:0.7887:random-6:0.7528:0.7683:0.7774:0.7890:random-4:0.9109:0.9226:0.9349:0.9481"
                if npb == "BT":
                    runtime = "2mesh:1.5466:1.5680:1.5915:1.6179:2torus:1.3876:1.3982:1.4077:1.4233:3mesh:0.5555:0.5797:0.6066:0.6329:3torus:0.3371:0.3465:0.3557:0.3652:random-6:0.4221:0.4344:0.4475:0.4594:random-4:0.5352:0.5523:0.5640:0.5817"
                if npb == "SP":
                    runtime = "2mesh:2.1815:2.1587:2.2090:2.2553:2torus:1.8784:1.8919:1.9053:1.9222:3mesh:0.7435:0.8147:0.8833:0.9604:3torus:0.5051:0.5297:0.5560:0.5830:random-6:0.6189:0.6486:0.6811:0.7162:random-4:0.7648:0.7953:0.8301:0.8676"
                if npb == "MG":
                    runtime = "2mesh:0.0163:0.0196:0.0222:0.0244:2torus:0.0124:0.0135:0.0147:0.0158:3mesh:0.0250:0.0263:0.0276:0.0289:3torus:0.0257:0.0267:0.0276:0.0287:random-6:0.0177:0.0187:0.0198:0.0209:random-4:0.0221:0.0235:0.0248:0.0262"
                if npb == "MM":
                    runtime = "2mesh:4.0320:4.0311:4.0317:4.0357:2torus:3.4392:3.4326:3.4358:3.4356:3mesh:1.8990:1.9062:1.9090:1.9104:3torus:1.8457:1.8438:1.8419:1.8476:random-6:0.8000:0.8078:0.8087:0.8114:random-4:0.9650:0.9673:0.9711:0.9715"
            s = str(i + 1) + "    " + str(cpu_unit) + "    " + str(ssd_unit) + "    " + str(gpu_unit) + "    " + str(
                time) + "    " + str(runtime) + "    " + str(npb) + "\n"
            f.write(s)
        f.close()
        n = n + 100


generate_npb_jobs(100)

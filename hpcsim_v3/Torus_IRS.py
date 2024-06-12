'''
Created on 2016/05/20

@author: smallcat
'''

# from __future__ import division
import networkx as nx
# import matplotlib.pyplot as plt
# import itertools
import threading
from . import GUI
from . import MyPWA
import time
import datetime
from networkx.algorithms.components.connected import is_connected
# import Torus
# import random
import copy

app = GUI.MyApp(0)  # Create an instance of the application class
app.MainLoop()  # Tell it to start processing events

RG = nx.Graph()

torus_d = int(GUI.topo[0])
# pos = {}

# 8*8*4*4*4 for 5-d torus, 8*8*8*8 for 4-d torus, 16*16*16 for 3-d torus, 64*64 for 2-d torus (4096)
# 16*8*4*2*2 for 5-d torus, 16*8*4*4 for 4-d torus, 16*16*8 for 3-d torus, 64*32 for 2-d torus (2048)
# 16*8*2*2*2 for 5-d torus, 16*8*4*2 for 4-d torus, 16*8*8 for 3-d torus, 32*32 for 2-d torus (1024)

# 16 nodes in a cabinet, 4*4*2*2*2 for 5-d torus, 4*4*4*2 for 4-d torus, 8*4*4 for 3-d torus, 16*8 for 2-d torus (2048)
# 32 nodes in a cabinet, 4*2*2*2*2 for 5-d torus, 4*4*2*2 for 4-d torus, 4*4*4 for 3-d torus, 8*8 for 2-d torus (2048)
# 64 nodes in a cabinet, 2*2*2*2*2 for 5-d torus, 4*2*2*2 for 4-d torus, 4*4*2 for 3-d torus, 8*4 for 2-d torus (2048)

# 1296 racks = 432*3 = 18*24*3 = 54*24
cpu_in_one_unit = 4
ssd_in_one_unit = 64
gpu_in_one_unit = 64
racks = 1296
# rackscale
rs_cpu_unit_in_one_rack = 1
rs_ssd_unit_in_one_rack = 1
rs_gpu_unit_in_one_rack = 1
rs_cpu_in_one_rack = rs_cpu_unit_in_one_rack * cpu_in_one_unit  # 4
rs_ssd_in_one_rack = rs_ssd_unit_in_one_rack * ssd_in_one_unit  # 64
rs_gpu_in_one_rack = rs_gpu_unit_in_one_rack * gpu_in_one_unit  # 64
rs_cpu_racks = rs_cpu_in_one_rack * racks  # 4*1296=5184
rs_ssd_racks = rs_ssd_in_one_rack * racks  # 16*1296=20736
rs_gpu_racks = rs_gpu_in_one_rack * racks  # 64*1296=82944
# interrackscale
irs_cpu_unit_in_one_rack = 3
irs_ssd_unit_in_one_rack = 3
irs_gpu_unit_in_one_rack = 3
irs_cpu_in_one_rack = irs_cpu_unit_in_one_rack * cpu_in_one_unit  # 12
irs_ssd_in_one_rack = irs_ssd_unit_in_one_rack * ssd_in_one_unit  # 192
irs_gpu_in_one_rack = irs_gpu_unit_in_one_rack * gpu_in_one_unit  # 192
irs_cpu_racks = irs_cpu_in_one_rack * racks / 3  # 12*1296/3=5184
irs_ssd_racks = irs_ssd_in_one_rack * racks / 3  # 192*1296/3=82944
irs_gpu_racks = irs_gpu_in_one_rack * racks / 3  # 192*1296/3=82944

# cpu network
torus_two_x = 24
torus_two_y = 54

# arch = "RS"
# arch = "IRS-REPEAT"
# arch = "IRS-LOOP"
arch = GUI.arch

# print arch

if arch == "IRS-REPEAT" or "IRS-LOOP":
    torus_two_y = 18

nodes_in_cabinet = 32

# aa = 4
# bb = 2
# cc = 2
# dd = 2
# ee = 2

tn = racks  # total nodes

# degree = dimension*2
# links = nodes*degree/2 = nodes*dimension (nodes>4)
if (torus_d == 2):  # 2-d torus
    #     tn = torus_two_x*torus_two_y
    #     if GUI.speedup == "tor":
    #         tn = tn*nodes_in_cabinet
    #     RG = nx.grid_graph(dim=[torus_two_x,torus_two_y], periodic=True)
    #         pos = dict(zip(RG,RG))
    #     pos = nx.spring_layout(RG)
    if arch == "RS":
        RG = nx.grid_graph(dim=[24, 54], periodic=True)
        for node in RG.nodes():
            RG.node[node]["cpu"] = 1
            RG.node[node]["ssd"] = 1
            RG.node[node]["gpu"] = 1
            RG.node[node]["jobs"] = []
    if arch == "IRS-REPEAT":
        RG = nx.grid_graph(dim=[24, 54], periodic=True)
        for node in RG.nodes():
            if node[1] < torus_two_y:
                RG.node[node]["cpu"] = 3
                RG.node[node]["ssd"] = 0
                RG.node[node]["gpu"] = 0
                RG.node[node]["jobs"] = []
            elif node[1] < torus_two_y * 2:
                RG.node[node]["cpu"] = 0
                RG.node[node]["ssd"] = 3
                RG.node[node]["gpu"] = 0
                RG.node[node]["jobs"] = []
            elif node[1] < torus_two_y * 3:
                RG.node[node]["cpu"] = 0
                RG.node[node]["ssd"] = 0
                RG.node[node]["gpu"] = 3
                RG.node[node]["jobs"] = []
    if arch == "IRS-LOOP":
        RG = nx.grid_graph(dim=[24, 18], periodic=True)
        for node in RG.nodes():
            RG.node[node]["cpu"] = 3
            RG.node[node]["ssd"] = 3
            RG.node[node]["gpu"] = 3
            RG.node[node]["cpu_jobs"] = []
            RG.node[node]["ssd_jobs"] = []
            RG.node[node]["gpu_jobs"] = []

        # cpus_one = {}
# cpus_two = {}
# cpus_three = {}  

fso_cpu_ssdgpu = GUI.fso_cpu_ssdgpu
cpu_ssdgpu_improved_by_fso = 0
for node in RG.nodes():
    RG.node[node]["fso_cpu_ssdgpu"] = fso_cpu_ssdgpu

if (GUI.mode == "FSO_random"):
    for node in RG.nodes():
        RG.node[node]["fso"] = int(GUI.fso_r * 100)
elif (GUI.mode == "FSO"):
    for node in RG.nodes():
        RG.node[node]["fso"] = 2 * torus_d
elif (GUI.mode == "normal"):
    for node in RG.nodes():
        RG.node[node]["fso"] = 0

    # k = 10000.0
k = 1.0

fso_config_time = 0.0 / k

# nx.write_adjlist(RG,"test.adjlist")

jobs = {}

# jobs[0] = (4,1,0)   #job number, required cpus, required time (in seconds), submit time
# jobs[1] = (4,4,1)
# jobs[2] = (6,8,2)
# jobs[3] = (2,1,3)
# jobs[4] = (4,4,4)
# jobs[5] = (2,3,5)
# jobs[6] = (4,8,6)
# jobs[7] = (6,5,7)
# jobs[8] = (1,7,8)
# jobs[9] = (5,2,9)
# jobs[10] = (5,6,10)
# jobs[11] = (-1,2,11)

# huyao 151001
jobs_submit = {}
jobs_dispatch = {}

# huyao 151202
jobs_cpus = {}
jobs_runtime = {}

jobs_ssds = {}
jobs_gpus = {}

jobs_cpus_nodes = {}
jobs_cpus_aspl = {}
jobs_cpus_diameter = {}

job_x = []
job_y = []

data = MyPWA.data
num_jobs = len(data)
for i in range(num_jobs):
    #     jobs[i] = (data["Requested Number of Processors"][i], data["Requested Time"][i]/k)
    jobs[i] = (data["cpu#"][i], data["ssd#"][i], data["gpu#"][i], data["submit"][i] / k, data["runtime"][i] / k)
    jobs_submit[i] = 0.0
    jobs_dispatch[i] = 0.0
    jobs_cpus[i] = 0
    jobs_runtime[i] = 0.0
    jobs_ssds[i] = 0
    jobs_gpus[i] = 0

    jobs_cpus_nodes[i] = []
    jobs_cpus_aspl[i] = 0.0
    jobs_cpus_diameter[i] = 0

#     cpus_one[i] = 0
#     cpus_two[i] = 0
#     cpus_three[i] = 0 

# jobs_ = zip(jobs.keys(), jobs.values())

job_samples = list(jobs.items())
queue = [job_samples[0]]

jobs_submit[0] = time.time()

# current = job_samples[0][1][2]
num = len(job_samples)
all_submitted = False


# lock = False
def submit_jobs():
    current = job_samples[0][1][3]
    global queue, all_submitted, jobs_submit
    for i in range(1, num):
        wait = job_samples[i][1][3] - current
        if (wait >= 0):
            time.sleep(wait)
            current = job_samples[i][1][3]
            queue.append(job_samples[i])

            # 150824 huyao sorting according to job size (cpu#)
            #             global lock
            #             lock = True
            if (GUI.schedule == "BF"):
                # 150824 huyao first unchanged during insertion
                one = queue.pop(0)
                queue = sorted(queue, key=lambda abc: abc[1], reverse=True)
                queue.insert(0, one)
            if (GUI.schedule == "SF"):
                one = queue.pop(0)
                queue = sorted(queue, key=lambda abc: abc[1])
                queue.insert(0, one)
            #             if(GUI.schedule == "LIFO"):
            #                 queue.insert(1, queue.pop(-1))
            #             lock = False

            # 151129 huyao sorting according to runtime
            if (GUI.schedule == "RSF"):
                one = queue.pop(0)
                queue = sorted(queue, key=lambda abc: abc[1][1])
                queue.insert(0, one)
            if (GUI.schedule == "RLF"):
                one = queue.pop(0)
                queue = sorted(queue, key=lambda abc: abc[1][1], reverse=True)
                queue.insert(0, one)

            print(datetime.datetime.now(), "job: ", job_samples[i], " is submitted")

            jobs_submit[i] = time.time()
        else:
            print(datetime.datetime.now(), "job: ", job_samples[i], " can not be submitted")
            i = i + 1
        if (i == num - 1):
            all_submitted = True


# jobs_ = jobs.items()    #dic -> tuple
# if(GUI.schedule == "BF"):
#     jobs_ = sorted(jobs.items(), key=lambda abc:abc[1], reverse=True)
# if(GUI.schedule == "SF"):
#     jobs_ = sorted(jobs.items(), key=lambda abc:abc[1])   

# print jobs_ 

# print RG.nodes(data = True)
# print RG.edges()

# nodelist = []


# print jobs_[0][1][0]

# get all sub-graphs with x nodes
# target = nx.complete_graph(jobs_[0][1][0])
# for sub_nodes in itertools.combinations(RG.nodes(),len(target.nodes())):
#     subg = RG.subgraph(sub_nodes)
#     if nx.is_connected(subg):
#         #print subg.edges()
#         print subg.nodes()

# jobs_.pop(0)
# print jobs_

# jobs.pop(jobs_[0][0])
# print jobs

# def printt(str):
#     print datetime.datetime.now(), str


# def divi(n, start = 2):
#     if(n==1):
#         return 1, 1
#     for i in range(start,n+1):
#         if(n%i == 0):
#             return i, n/i   #i width; n/i length

def divi_torus(n):
    di = []
    # huyao 160111 host is 4d or 5d while sub is 3d
    if GUI.speedup == "tor-sub3d" and torus_d > 3:
        while (n != 1):
            for i in range(2, n + 1):
                if (n % i) == 0:
                    n /= i
                    di.append(i)
                    break
        dim = len(di)
        dis = dim - 3
        dis_abs = abs(dis)
        if (dis < 0):
            for i in range(dis_abs):
                di.append(1)
        if (dis > 0):
            for i in range(dis_abs):
                i_mod = i % torus_d
                di[i_mod] = di[i_mod] * di.pop(-1)
        dist = torus_d - 3
        for i in range(dist):
            di.append(1)
    else:
        while (n != 1):
            for i in range(2, n + 1):
                if (n % i) == 0:
                    n /= i
                    di.append(i)
                    break
        dim = len(di)
        dis = dim - torus_d
        dis_abs = abs(dis)
        if (dis < 0):
            for i in range(dis_abs):
                di.append(1)
        if (dis > 0):
            for i in range(dis_abs):
                i_mod = i % torus_d
                di[i_mod] = di[i_mod] * di.pop(-1)
    return di


# def unlock(node, endx, endy, endxx, endyy, job): 
#     node["ava"] = "yes"
#     nodelist.remove((endx,endy))
#     if(endx==endxx and endy==endyy):
#         print datetime.datetime.now(), "job: ", job, "is finished"

mylock = threading.RLock()


def unlock_unava(nl, job):
    job_number = job[0]
    if arch == "RS":
        while (len(nl) > 0):
            mylock.acquire()
            RG.node[nl[0]]["cpu"] = 1
            RG.node[nl[0]]["ssd"] = 1
            RG.node[nl[0]]["gpu"] = 1
            #             nodelist.remove(nl[0])
            mylock.release()
            nl.pop(0)
    if arch == "IRS-REPEAT":
        while (len(nl) > 0):
            mylock.acquire()
            RG.node[nl[0]]["cpu"] += 1
            x = nl[0][0]
            ssd_y = nl[0][1] + torus_two_y
            gpu_y = nl[0][1] + (2 * torus_two_y)
            if job_number in RG.node[x, ssd_y]["jobs"]:
                RG.node[x, ssd_y]["ssd"] += 1
            if job_number in RG.node[x, gpu_y]["jobs"]:
                RG.node[x, gpu_y]["gpu"] += 1
            #             nodelist.remove(nl[0])
            #             print RG.node[x, ssd_y]["ssd"], RG.node[x, gpu_y]["gpu"]
            if job_number in RG.node[nl[0]]:
                RG.node[nl[0]]["fso_cpu_ssdgpu"] += RG.node[nl[0]][job_number]
            mylock.release()
            nl.pop(0)
    if arch == "IRS-LOOP":
        while (len(nl) > 0):
            mylock.acquire()
            RG.node[nl[0]]["cpu"] += 1
            if job_number in RG.node[nl[0]]["ssd_jobs"]:
                RG.node[nl[0]]["ssd"] += 1
            if job_number in RG.node[nl[0]]["gpu_jobs"]:
                RG.node[nl[0]]["gpu"] += 1
            mylock.release()
            nl.pop(0)
    print(datetime.datetime.now(), "job: ", job, "is finished")


#     checkover()

# def unlock0(node, x, y, i, job): 
#     node["ava"] = "yes"
#     nodelist.remove((x,y))
#     if(i==0):
#         print datetime.datetime.now(), "job: ", job, "is finished"
# 150825 huyao
fso_not_found = False


def fso():
    count = 0
    ava_nodes = []
    global fso_not_found, jobs_dispatch, first_num, jobs_cpus, jobs_runtime, jobs_ssds, jobs_gpus, cpu_ssdgpu_improved_by_fso

    if (torus_d == 2):  # 2-d torus 8*8
        for b in range(torus_two_y):
            for a in range(torus_two_x):
                if (RG.node[(a, b)]["cpu"] > 0):
                    count = count + 1
                    ava_nodes.append((a, b))
                    if (count == first_cpu):
                        print(datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso):")

                        time.sleep(fso_config_time)

                        jobs_dispatch[first_num] = time.time()
                        jobs_cpus[first_num] = first_cpu
                        jobs_runtime[first_num] = first_time

                        jobs_ssds[first_num] = first_ssd
                        jobs_gpus[first_num] = first_gpu

                        n = 0
                        if arch == "RS":
                            for node in ava_nodes:
                                mylock.acquire()
                                RG.node[node]["cpu"] = 0
                                RG.node[node]["jobs"].append(first_num)
                                #                         print "(", ava_nodes[i][0], ", ", ava_nodes[i][1], ") "
                                #                                 nodelist.append(ava_nodes[i])
                                #                         t = threading.Timer(jobs_[0][1][1], unlock0, (RG.node[ava_nodes[i]], ava_nodes[i][0], ava_nodes[i][1], i, jobs_[0],)) #required processing time
                                #                         t.start()
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[node]["ssd"] = 0
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[node]["gpu"] = 0
                                mylock.release()
                                n = n + 1
                        if arch == "IRS-REPEAT":
                            cpu_ssdgpu = first_ssd + first_gpu
                            for node in ava_nodes:
                                if RG.node[node]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                    RG.node[node]["fso_cpu_ssdgpu"] -= 1
                                    cpu_ssdgpu -= 1
                                    RG.node[node][first_num] = 1
                                    cpu_ssdgpu_improved_by_fso += 1
                                    if RG.node[node]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                        RG.node[node]["fso_cpu_ssdgpu"] -= 1
                                        cpu_ssdgpu -= 1
                                        RG.node[node][first_num] = 2
                                        cpu_ssdgpu_improved_by_fso += 1
                                #                                 if RG.node[node]["cpu"] == 1:
                                #                                     cpus_one[first_num] += 1
                                #                                 elif RG.node[node]["cpu"] == 2:
                                #                                     cpus_two[first_num] += 1
                                #                                 elif RG.node[node]["cpu"] == 3:
                                #                                     cpus_three[first_num] += 1
                                mylock.acquire()
                                RG.node[node]["cpu"] -= 1
                                RG.node[node]["jobs"].append(first_num)
                                #                         print "(", ava_nodes[i][0], ", ", ava_nodes[i][1], ") "
                                #                                 nodelist.append(ava_nodes[i])
                                #                         t = threading.Timer(jobs_[0][1][1], unlock0, (RG.node[ava_nodes[i]], ava_nodes[i][0], ava_nodes[i][1], i, jobs_[0],)) #required processing time
                                #                         t.start()
                                x = node[0]
                                ssd_y = node[1] + torus_two_y
                                gpu_y = node[1] + (2 * torus_two_y)
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[x, ssd_y]["ssd"] -= 1
                                    RG.node[x, ssd_y]["jobs"].append(first_num)
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[x, gpu_y]["gpu"] -= 1
                                    RG.node[x, gpu_y]["jobs"].append(first_num)
                                mylock.release()
                                n = n + 1
                        if arch == "IRS-LOOP":
                            for node in ava_nodes:
                                mylock.acquire()
                                RG.node[node]["cpu"] -= 1
                                RG.node[node]["cpu_jobs"].append(first_num)
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[node]["ssd"] -= 1
                                    RG.node[node]["ssd_jobs"].append(first_num)
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[node]["gpu"] -= 1
                                    RG.node[node]["gpu_jobs"].append(first_num)
                                mylock.release()
                                n = n + 1

                        jobs_cpus_nodes[first_num] = copy.copy(ava_nodes)

                        t = threading.Timer(first_time, unlock_unava, (ava_nodes, first,))  # required processing time
                        t.start()
                        queue.pop(0)
                        #                     fill = 0
                        fso_not_found = False
                        return
                if (a == torus_two_x - 1 and b == torus_two_y - 1):
                    fso_not_found = True


# 150926 huyao
transform_fso_random = False
fso_lowest_ratio = 0.1  # 0.05 ->0.1
fso_used = 0
lowest_sub_nodes = int(tn * 0.01)  # 0.02 -> 0.01

# test
jump_1 = 0
jump_2 = 0
jump_3 = 0


# normal_to_fso = False
# fso_to_normal = 0
def fso_random():
    global transform_fso_random
    global transform
    global fill
    global first
    global first_num
    global first_cpu
    global first_time
    global to_first
    global g
    global origin
    global jobs_dispatch
    global fso_used
    global jump_1, jump_2, jump_3
    #     global normal_to_fso
    #     global  fso_to_normal
    global first_ssd
    global first_gpu
    global cpu_ssdgpu_improved_by_fso

    if (transform_fso_random == True):
        g.insert(0, g.pop(-1))
        if (g == origin):
            #             transform = False
            reset()
            #                 if(GUI.mode=="FSO"):
            #                     fso()
            to_first = False
            #             continue
            return
    else:
        g = divi_torus(first_cpu + fill)
        origin = g  # required cpus
        if (torus_d == 2 and fill == 1 and (g[0] > torus_two_x or g[1] > torus_two_y)):
            print(datetime.datetime.now(), "job: ", first, " can not be scheduled due to lack of resources")
            queue.pop(0)
            to_first = True
            #             checkover()
            reset()
            #             continue
            return
        if (g[0] > torus_two_x and g[0] == first_cpu):
            fill = 1
            to_first = False
            #             continue
            return

    #     found = False   #allocated cpus
    #     sub_found = False #huyao 151003 sub graph with lowest ratio of fso nodes is found

    #     flag = True #if each cpu is available in x*y grid
    #     flag_ = True #useful if fill!=0

    #     fso_ratio = 1.0
    #     fn = []
    #     sub = []
    #     nouse = []
    #
    #     fnl = [] #fso node link
    #     nn = [] #node neighbors
    #     subnodes = [] #substitue nodes

    #     if(normal_to_fso==False or first_cpu > lowest_sub_nodes ):
    if (first_cpu > lowest_sub_nodes):
        lowest_fso_nodes = 0
    else:
        lowest_fso_nodes = int(fso_lowest_ratio * (first_cpu + 7))

    if (torus_d == 2):  # 2-d torus 8*8

        #         flag = True #if each cpu is available in x*y grid
        #         flag_ = True #useful if fill!=0
        #
        #         fso_ratio = 1.0
        #         fn = []
        #         sub = []
        #         nouse = []
        #
        #         fnl = [] #fso node link
        #         nn = [] #node neighbors
        #         subnodes = [] #substitue nodes

        # huyao 151019 normal first, fso follows
        for b in range(torus_two_y):
            for a in range(torus_two_x):
                flag = True  # if each cpu is available in x*y grid
                flag_ = True  # useful if fill!=0
                noused = []
                for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                    for bbb in range(b, b + g[1]):
                        aaaa = aaa % torus_two_x
                        bbbb = bbb % torus_two_y
                        if (RG.node[(aaaa, bbbb)]["cpu"] == 0 and fill == 0):
                            flag = False
                            break
                        if (RG.node[(aaaa, bbbb)]["cpu"] == 0 and fill == 1):
                            if (flag_ == True):
                                flag_ = False
                                noused.append((aaaa, bbbb))
                            else:
                                flag = False
                                break
                    if (flag == False):
                        break
                if (flag == True):
                    fso_ratio = 0.0
                    print(datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                        fso_ratio) + " : ")
                    print(datetime.datetime.now(), "fso links are used for ", str(fso_used), " times")
                    jobs_dispatch[first_num] = time.time()
                    jobs_cpus[first_num] = first_cpu
                    jobs_runtime[first_num] = first_time
                    jobs_ssds[first_num] = first_ssd
                    jobs_gpus[first_num] = first_gpu

                    job_x.append(g[0])
                    job_y.append(g[1])

                    ava_to_unava = []
                    n = 0
                    if arch == "RS":
                        for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                            for bbb in range(b, b + g[1]):
                                aaaa = aaa % torus_two_x
                                bbbb = bbb % torus_two_y
                                if (fill == 1 and len(noused) > 0):
                                    if ((aaaa, bbbb) == noused[0]):
                                        continue
                                mylock.acquire()
                                RG.node[(aaaa, bbbb)]["cpu"] = 0
                                RG.node[(aaaa, bbbb)]["jobs"].append(first_num)
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[(aaaa, bbbb)]["ssd"] = 0
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[(aaaa, bbbb)]["gpu"] = 0
                                mylock.release()
                                n = n + 1
                                #                             nodelist.append((aaaa,bbbb))
                                ava_to_unava.append((aaaa, bbbb))
                    if arch == "IRS-REPEAT":
                        cpu_ssdgpu = first_ssd + first_gpu
                        for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                            for bbb in range(b, b + g[1]):
                                aaaa = aaa % torus_two_x
                                bbbb = bbb % torus_two_y
                                if (fill == 1 and len(noused) > 0):
                                    if ((aaaa, bbbb) == noused[0]):
                                        continue
                                if RG.node[(aaaa, bbbb)]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                    RG.node[(aaaa, bbbb)]["fso_cpu_ssdgpu"] -= 1
                                    cpu_ssdgpu -= 1
                                    RG.node[(aaaa, bbbb)][first_num] = 1
                                    cpu_ssdgpu_improved_by_fso += 1
                                    if RG.node[(aaaa, bbbb)]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                        RG.node[(aaaa, bbbb)]["fso_cpu_ssdgpu"] -= 1
                                        cpu_ssdgpu -= 1
                                        RG.node[(aaaa, bbbb)][first_num] = 2
                                        cpu_ssdgpu_improved_by_fso += 1
                                    #                                 if RG.node[(aaaa,bbbb)]["cpu"] == 1:
                                #                                     cpus_one[first_num] += 1
                                #                                 elif RG.node[(aaaa,bbbb)]["cpu"] == 2:
                                #                                     cpus_two[first_num] += 1
                                #                                 elif RG.node[(aaaa,bbbb)]["cpu"] == 3:
                                #                                     cpus_three[first_num] += 1
                                mylock.acquire()
                                RG.node[(aaaa, bbbb)]["cpu"] -= 1
                                RG.node[(aaaa, bbbb)]["jobs"].append(first_num)
                                x = aaaa
                                ssd_y = bbbb + torus_two_y
                                gpu_y = bbbb + (2 * torus_two_y)
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[x, ssd_y]["ssd"] -= 1
                                    RG.node[x, ssd_y]["jobs"].append(first_num)
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[x, gpu_y]["gpu"] -= 1
                                    RG.node[x, gpu_y]["jobs"].append(first_num)
                                mylock.release()
                                n = n + 1
                                ava_to_unava.append((aaaa, bbbb))
                    if arch == "IRS-LOOP":
                        for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                            for bbb in range(b, b + g[1]):
                                aaaa = aaa % torus_two_x
                                bbbb = bbb % torus_two_y
                                if (fill == 1 and len(noused) > 0):
                                    if ((aaaa, bbbb) == noused[0]):
                                        continue
                                mylock.acquire()
                                RG.node[(aaaa, bbbb)]["cpu"] -= 1
                                RG.node[(aaaa, bbbb)]["cpu_jobs"].append(first_num)
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[(aaaa, bbbb)]["ssd"] -= 1
                                    RG.node[(aaaa, bbbb)]["ssd_jobs"].append(first_num)
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[(aaaa, bbbb)]["gpu"] -= 1
                                    RG.node[(aaaa, bbbb)]["gpu_jobs"].append(first_num)
                                mylock.release()
                                n = n + 1
                                ava_to_unava.append((aaaa, bbbb))

                    jobs_cpus_nodes[first_num] = copy.copy(ava_to_unava)

                    t = threading.Timer(first_time, unlock_unava, (ava_to_unava, first,))  # required processing time
                    t.start()
                    queue.pop(0)
                    reset()
                    to_first = True
                    return

        for b in range(torus_two_y):
            for a in range(torus_two_x):

                flag = True
                flag_ = True  # useful if fill!=0
                #                 fso_nodes = []
                sub = []  # sub graph
                fn = []  # fso nodes (not available nodes)
                nouse = []  # not used nodes (fill==1)
                #                 fn_connect = [] #fso nodes and mutual connection
                fnl = []  # fso node link
                nn = []  # node neighbors
                subnodes = []  # substitue nodes

                over = False

                for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                    for bbb in range(b, b + g[1]):
                        aaaa = aaa % torus_two_x
                        bbbb = bbb % torus_two_y
                        sub.append((aaaa, bbbb))
                        if (RG.node[(aaaa, bbbb)]["cpu"] == 0):
                            if (fill == 0):
                                fn.append((aaaa, bbbb))

                                if (len(fn) > lowest_fso_nodes):
                                    over = True
                                    break

                            if (fill == 1):
                                if (flag_ == True):
                                    flag_ = False
                                    nouse.append((aaaa, bbbb))
                                else:
                                    fn.append((aaaa, bbbb))

                                    if (len(fn) > lowest_fso_nodes):
                                        over = True
                                        break

                        if (fill == 1 and aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and len(nouse) == 0):
                            nouse.append((aaaa, bbbb))
                    if (over == True):
                        break

                if (over == False):
                    fso_ratio = float(len(fn)) / first_cpu
                    for node in fn:
                        fl = 0  # fso links
                        for neighbor in RG.neighbors(node):
                            if (neighbor in sub):
                                if (RG.node[neighbor]["fso"] == 0):
                                    #                                     print "1"
                                    jump_1 = jump_1 + 1
                                    flag = False
                                    break
                                #                                     transform_fso_random = True
                                #                                     return
                                fl = fl + 1
                                #                             if(neighbor in fn):
                                #                                 fl_connect = fl_connect+1
                                #                                 node_neighbors.append(neighbor)
                                #                             else:
                                nn.append(neighbor)
                        if (flag == False):
                            break
                        fnl.append((node, fl))
                    #                     fnl.append((node,fl,fl_connect)) #min fso links = fl-fl_connect

                    if (flag == True):
                        nnn = list(set(nn))
                        if (fill == 1 and nouse[0] in nnn):
                            nnn.remove(nouse[0])
                        for item in nnn:
                            if (RG.node[item]["fso"] < nn.count(item)):
                                #                                 print "2..."
                                #                                 print RG.node[item]["fso"]
                                #                                 print nn.count(item)
                                jump_2 = jump_2 + 1
                                flag = False
                                break
                            #                                 transform_fso_random = True
                    #                                 return

                    if (flag == True):
                        for each in fnl:
                            RG_ = RG.copy()
                            RG_.remove_nodes_from(sub)
                            for n in RG_.nodes():
                                #                                 if((n not in sub or (fill==1 and n==nouse[0])) and RG.node[n]["ava"] == "yes"):
                                if (RG.node[n]["cpu"] > 0):
                                    if (RG.node[n]["fso"] >= each[1]):
                                        subnodes.append(n)
                                        break
                                #                                     elif(RG.node[n]["fso"] >= fl-fl_connect):
                                #                                         temp = []
                                #                                         for neighbor in RG.neighbors(n):
                                #                                             if(neighbor not in sub and RG.node[neighbor]["ava"] == "yes"):
                                #                                                 temp.append(neighbor)
                                #                                         if(len(temp) >= fl_connect or (len(temp) < fl_connect and RG.node[n]["fso"]-(fl_connect-len(temp)) >= fl-fl_connect)):
                                #                                             subnodes.append(n)
                                #
                                #                             while(len(subgraph) > 0):
                                #                                 for i in range(fl_connect):
                                #                                     for n in RG.neighbors(temp[i]):
                                #                                         if(n not in sub and RG.node[n]["ava"] == "yes"):
                                #                                             subnodes.append(temp[i])
                                #                                             subgraph.remove()
                                if (n == RG_.nodes()[-1]):
                                    #                                     print "3"
                                    jump_3 = jump_3 + 1
                                    if (fill == 1 and RG.node[nouse[0]]["cpu"] > 0 and RG.node[nouse[0]]["fso"] >= each[
                                        1]):
                                        subnodes.append(nouse[0])
                                        break
                                    else:
                                        flag = False
                                        break
                                    #                                     transform_fso_random = True
                            #                                     return
                            if (flag == False):
                                break

                    if (flag == True):
                        print(datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                            fso_ratio) + " : ")

                        if (fso_ratio > 0.0):
                            fso_used = fso_used + 1
                            time.sleep(fso_config_time)

                        print(datetime.datetime.now(), "fso links are used for ", str(fso_used), " times")

                        jobs_dispatch[first_num] = time.time()
                        jobs_cpus[first_num] = first_cpu
                        jobs_runtime[first_num] = first_time

                        jobs_ssds[first_num] = first_ssd
                        jobs_gpus[first_num] = first_gpu

                        job_x.append(g[0])
                        job_y.append(g[1])

                        ava_to_unava = []
                        #                         for aaa in range(a, a+g[0]):
                        #                             for bbb in range(b, b+g[1]):
                        #                                 aaaa = aaa%aa
                        #                                 bbbb = bbb%bb
                        #                                 if(RG.node[(aaaa,bbbb)]["ava"] == "yes"):
                        #                                     RG.node[(aaaa,bbbb)]["ava"] = "no"
                        #     #                                     print "(", aaaa, ", ", bbbb, ") "
                        #                                     nodelist.append((aaaa,bbbb))
                        #                                     #print RG.node[(xxx,yyy)]
                        #                                     ava_to_unava.append((aaaa,bbbb))
                        n = 0
                        if arch == "RS":
                            for node in sub:
                                if (node not in fn):
                                    if (fill == 1 and node == nouse[0]):
                                        continue
                                    mylock.acquire()
                                    RG.node[node]["cpu"] = 0
                                    RG.node[node]["jobs"].append(first_num)
                                    if first_ssd != 0 and n < first_ssd:
                                        RG.node[node]["ssd"] = 0
                                    if first_gpu != 0 and n < first_gpu:
                                        RG.node[node]["gpu"] = 0
                                    mylock.release()
                                    n = n + 1
                                    #                                 nodelist.append(node)
                                    ava_to_unava.append(node)

                            for each in subnodes:
                                mylock.acquire()
                                RG.node[each]["cpu"] = 0
                                RG.node[node]["jobs"].append(first_num)
                                #                                     print "(", aaaa, ", ", bbbb, ") "
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[each]["ssd"] = 0
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[each]["gpu"] = 0
                                mylock.release()
                                n = n + 1
                                #                             nodelist.append(each)
                                # print RG.node[(xxx,yyy)]
                                ava_to_unava.append(each)

                                #                         if(fill==1 and nouse[0] in ava_to_unava):
                        #                             RG.node[nouse[0]]["ava"] = "yes"
                        #                             nodelist.remove(nouse[0])
                        #                             ava_to_unava.remove(nouse[0])

                        if arch == "IRS-REPEAT":
                            cpu_ssdgpu = first_ssd + first_gpu
                            for node in sub:
                                if (node not in fn):
                                    if (fill == 1 and node == nouse[0]):
                                        continue
                                    if RG.node[node]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                        RG.node[node]["fso_cpu_ssdgpu"] -= 1
                                        cpu_ssdgpu -= 1
                                        RG.node[node][first_num] = 1
                                        cpu_ssdgpu_improved_by_fso += 1
                                        if RG.node[node]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                            RG.node[node]["fso_cpu_ssdgpu"] -= 1
                                            cpu_ssdgpu -= 1
                                            RG.node[node][first_num] = 2
                                            cpu_ssdgpu_improved_by_fso += 1
                                        #                                     if RG.node[node]["cpu"] == 1:
                                    #                                         cpus_one[first_num] += 1
                                    #                                     elif RG.node[node]["cpu"] == 2:
                                    #                                         cpus_two[first_num] += 1
                                    #                                     elif RG.node[node]["cpu"] == 3:
                                    #                                         cpus_three[first_num] += 1
                                    mylock.acquire()
                                    RG.node[node]["cpu"] -= 1
                                    RG.node[node]["jobs"].append(first_num)
                                    x = node[0]
                                    ssd_y = node[1] + torus_two_y
                                    gpu_y = node[1] + (2 * torus_two_y)
                                    if first_ssd != 0 and n < first_ssd:
                                        RG.node[x, ssd_y]["ssd"] -= 1
                                        RG.node[x, ssd_y]["jobs"].append(first_num)
                                    if first_gpu != 0 and n < first_gpu:
                                        RG.node[x, gpu_y]["gpu"] -= 1
                                        RG.node[x, gpu_y]["jobs"].append(first_num)
                                    mylock.release()
                                    n = n + 1
                                    #                                 nodelist.append(node)
                                    ava_to_unava.append(node)

                            for each in subnodes:
                                if RG.node[node]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                    RG.node[node]["fso_cpu_ssdgpu"] -= 1
                                    cpu_ssdgpu -= 1
                                    RG.node[node][first_num] = 1
                                    cpu_ssdgpu_improved_by_fso += 1
                                    if RG.node[node]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                        RG.node[node]["fso_cpu_ssdgpu"] -= 1
                                        cpu_ssdgpu -= 1
                                        RG.node[node][first_num] = 2
                                        cpu_ssdgpu_improved_by_fso += 1
                                    #                                 if RG.node[node]["cpu"] == 1:
                                #                                     cpus_one[first_num] += 1
                                #                                 elif RG.node[node]["cpu"] == 2:
                                #                                     cpus_two[first_num] += 1
                                #                                 elif RG.node[node]["cpu"] == 3:
                                #                                     cpus_three[first_num] += 1
                                mylock.acquire()
                                RG.node[each]["cpu"] -= 1
                                RG.node[node]["jobs"].append(first_num)
                                x = each[0]
                                ssd_y = each[1] + torus_two_y
                                gpu_y = each[1] + (2 * torus_two_y)
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[x, ssd_y]["ssd"] -= 1
                                    RG.node[x, ssd_y]["jobs"].append(first_num)
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[x, gpu_y]["gpu"] -= 1
                                    RG.node[x, gpu_y]["jobs"].append(first_num)
                                mylock.release()
                                n = n + 1
                                #                             nodelist.append(each)
                                # print RG.node[(xxx,yyy)]
                                ava_to_unava.append(each)

                        if arch == "IRS-LOOP":
                            for node in sub:
                                if (node not in fn):
                                    if (fill == 1 and node == nouse[0]):
                                        continue
                                    mylock.acquire()
                                    RG.node[node]["cpu"] -= 1
                                    RG.node[node]["cpu_jobs"].append(first_num)
                                    if first_ssd != 0 and n < first_ssd:
                                        RG.node[node]["ssd"] -= 1
                                        RG.node[node]["ssd_jobs"].append(first_num)
                                    if first_gpu != 0 and n < first_gpu:
                                        RG.node[node]["gpu"] -= 1
                                        RG.node[node]["gpu_jobs"].append(first_num)
                                    mylock.release()
                                    n = n + 1
                                    #                                 nodelist.append(node)
                                    ava_to_unava.append(node)

                            for each in subnodes:
                                mylock.acquire()
                                RG.node[each]["cpu"] -= 1
                                RG.node[node]["cpu_jobs"].append(first_num)
                                if first_ssd != 0 and n < first_ssd:
                                    RG.node[each]["ssd"] -= 1
                                    RG.node[each]["ssd_jobs"].append(first_num)
                                if first_gpu != 0 and n < first_gpu:
                                    RG.node[each]["gpu"] -= 1
                                    RG.node[each]["gpu_jobs"].append(first_num)
                                mylock.release()
                                n = n + 1
                                #                             nodelist.append(each)
                                # print RG.node[(xxx,yyy)]
                                ava_to_unava.append(each)

                        jobs_cpus_nodes[first_num] = copy.copy(ava_to_unava)

                        t = threading.Timer(first_time, unlock_unava,
                                            (ava_to_unava, first,))  # required processing time
                        t.start()
                        queue.pop(0)
                        #                 found = True
                        #                 transform = False
                        #                 fill = 0
                        reset()
                        to_first = True
                        #                         normal_to_fso = False
                        return

                if (a == torus_two_x - 1 and b == torus_two_y - 1):
                    #                     if normal_to_fso == False:
                    #                         normal_to_fso==True
                    #                     else:
                    transform_fso_random = True


#             if(found == True):
#                 break 


def reset():
    global transform_fso_random
    global transform
    global fill
    global g
    global origin
    #     global lock
    transform_fso_random = False
    transform = False
    fill = 0
    g = []
    origin = []


#     lock = False

# stopwrite = False

# def checkover():
#     if(len(queue)<1):
#         global stopwrite
#         stopwrite = True 

# huyao151001
def output_queue_time(fn):
    #     dt = str(datetime.datetime.now())
    #     dt = dt.replace(" ", "-")
    #     dt = dt.replace(".", "-")
    #     dt = dt.replace(":", "-")
    #     ar = MyPWA.archive.replace(".", "-")
    #     fn = "stat_queue_" + dt + "_" + GUI.topo + "_" + str(tn) + "_" + arch + "_" + GUI.schedule + "_" + GUI.mode + "_" + str(GUI.fso_r) + "_fsoconfigtime_" + str(fso_config_time) + "_" + GUI.speedup + "_" + ar #file name
    f = open(fn, "a")  # system utilization
    f.write("\n\n")
    f.write(
        "#job_number  submit  dispatch  queue  cpu#  runtime  weight  response(turnaround)  cpu_aspl  cpu_diameter\n")
    num = 0
    num_aspl = 0
    num_diameter = 0
    total_queue_time = 0.0
    total_job_weight = 0.0
    total_weight_response = 0.0
    total_weight_runtime = 0.0
    total_aspl = 0.0
    total_diameter = 0
    for i in range(num_jobs):
        queue_time = jobs_dispatch[i] - jobs_submit[i]
        job_weight = jobs_cpus[i] * jobs_runtime[i]
        response = queue_time + jobs_runtime[i]
        weight_response = job_weight * response
        weight_runtime = job_weight * jobs_runtime[i]

        cpus = RG.subgraph(jobs_cpus_nodes[i])
        if is_connected(cpus):
            if len(cpus) == 1:
                jobs_cpus_aspl[i] = 1
                jobs_cpus_diameter[i] = 1
            else:
                jobs_cpus_aspl[i] = nx.average_shortest_path_length(cpus)
                jobs_cpus_diameter[i] = nx.diameter(cpus)
        else:
            jobs_cpus_aspl[i] = 0.0
            jobs_cpus_diameter[i] = 0

        #         s = str(i) + "    " + str(jobs_submit[i]) + "    " + str(jobs_dispatch[i]) + "    " + str(queue_time) + "    " + str(jobs_cpus[i])+ "(" + str(cpus_one[i]) + "," + str(cpus_two[i]) + "," + str(cpus_three[i]) + ")" + "    " + str(jobs_runtime[i]) + "    " + str(job_weight) + "    " + str(response) + "    " + str(jobs_cpus_aspl[i])+ "    " + str(jobs_cpus_diameter[i]) + "\n"
        s = str(i) + "    " + str(jobs_submit[i]) + "    " + str(jobs_dispatch[i]) + "    " + str(
            queue_time) + "    " + str(jobs_cpus[i]) + "    " + str(jobs_runtime[i]) + "    " + str(
            job_weight) + "    " + str(response) + "    " + str(jobs_cpus_aspl[i]) + "    " + str(
            jobs_cpus_diameter[i]) + "\n"
        f.write(s)
        if (jobs_dispatch[i] > 0.0):
            num = num + 1
            total_queue_time = total_queue_time + queue_time
            total_job_weight = total_job_weight + job_weight
            total_weight_response = total_weight_response + weight_response
            total_weight_runtime = total_weight_runtime + weight_runtime

    for i in range(num_jobs):
        if jobs_cpus_aspl[i] > 0.0:
            num_aspl += 1
            total_aspl += jobs_cpus_aspl[i]
        if jobs_cpus_diameter[i] > 0:
            num_diameter += 1
            total_diameter += jobs_cpus_diameter[i]

    avg_queue_time = total_queue_time / num
    overall_utilization = total_job_weight / (tn * (end - start))
    avg_response = total_weight_response / total_job_weight
    avg_slowdown = total_weight_response / total_weight_runtime

    avg_aspl = total_aspl / num_aspl
    avg_diameter = total_diameter / float(num_diameter)

    cpu_request = 0
    ssd_request = 0
    gpu_request = 0
    cpu_run = 0
    ssd_run = 0
    gpu_run = 0
    #     total_cpus_one = 0
    #     total_cpus_two = 0
    #     total_cpus_three = 0
    for i in range(num_jobs):
        cpu_request += jobs[i][0]
        ssd_request += jobs[i][1]
        gpu_request += jobs[i][2]
    #         if arch == "IRS-REPEAT":
    #             total_cpus_one += cpus_one[i]
    #             total_cpus_two += cpus_two[i]
    #             total_cpus_three += cpus_three[i]
    for node in RG.nodes():
        if arch == "RS":
            cpu_run += len(RG.node[node]["jobs"])
        if arch == "IRS-REPEAT":
            if node[1] < torus_two_y:
                cpu_run += len(RG.node[node]["jobs"])
            if node[1] >= torus_two_y and node[1] < torus_two_y * 2:
                ssd_run += len(RG.node[node]["jobs"])
            if node[1] >= torus_two_y * 2:
                gpu_run += len(RG.node[node]["jobs"])
        if arch == "IRS-LOOP":
            cpu_run += len(RG.node[node]["cpu_jobs"])
            ssd_run += len(RG.node[node]["ssd_jobs"])
            gpu_run += len(RG.node[node]["gpu_jobs"])

    avg_x = 0.0
    avg_y = 0.0
    if len(job_x) > 0 and len(job_y) > 0:
        avg_x = sum(job_x) / float(len(job_x))
        avg_y = sum(job_y) / float(len(job_y))

    f.write("\n")
    f.write("dispatched jobs are: " + str(num) + " out of " + str(num_jobs) + "\n")
    f.write("average queue time is: " + str(avg_queue_time) + "\n")
    f.write("fso links are used for " + str(fso_used) + " times" + "\n")
    f.write("overall utilization is " + str(overall_utilization) + "\n")
    f.write("average response time is " + str(avg_response) + "\n")
    f.write("average slowdown is " + str(avg_slowdown) + "\n")
    #     f.write("cpu_request: " + str(cpu_request) +", cpu_run: " + str(cpu_run)+ " (" + str(total_cpus_one) + "," + str(total_cpus_two) + "," + str(total_cpus_three) + ")" + "\n")
    f.write("cpu_request: " + str(cpu_request) + ", cpu_run: " + str(cpu_run) + "\n")
    f.write("ssd_request: " + str(ssd_request) + ", ssd_run: " + str(ssd_run) + "\n")
    f.write("gpu_request: " + str(gpu_request) + ", gpu_run: " + str(gpu_run) + "\n")
    f.write("cpu aspl: " + str(avg_aspl) + "\n")
    f.write("cpu diameter: " + str(avg_diameter) + "\n")

    #     avg_hops_cpu_ssdgpu_fso_zero = torus_two_y+1
    #     avg_hops_cpu_ssdgpu_fso_one = ((total_cpus_one+total_cpus_two)*(torus_two_y+1)+total_cpus_three*2)/float(cpu_run)
    #     avg_hops_cpu_ssdgpu_fso_two = (total_cpus_one*(torus_two_y+1)+(total_cpus_two+total_cpus_three)*2)/float(cpu_run)
    #     avg_hops_cpu_ssdgpu_fso_three = 2
    #     f.write("average hops between cpu/ssd(gpu) when fso == 0: " + str(avg_hops_cpu_ssdgpu_fso_zero) + "\n")
    #     f.write("average hops between cpu/ssd(gpu) when fso == 1: " + str(avg_hops_cpu_ssdgpu_fso_one) + "\n")
    #     f.write("average hops between cpu/ssd(gpu) when fso == 2: " + str(avg_hops_cpu_ssdgpu_fso_two) + "\n")
    #     f.write("average hops between cpu/ssd(gpu) when fso == 3: " + str(avg_hops_cpu_ssdgpu_fso_three) + "\n")
    #     total_hops_between_fso_and_ssdgpu = (ssd_run+gpu_run)*(torus_two_y+1)
    if arch == "IRS-REPEAT":
        if GUI.mode == "FSO":  # fat-tree
            avg_hops_between_fso_and_ssdgpu = (cpu_ssdgpu_improved_by_fso * 2 + (
                        ssd_run + gpu_run - cpu_ssdgpu_improved_by_fso) * 5) / float(ssd_run + gpu_run)
            f.write("fso betweeen cpu and ssd/gpu: " + str(fso_cpu_ssdgpu) + "\n")
            f.write("improved hops between cpu/ssd(gpu) by fso: " + str(cpu_ssdgpu_improved_by_fso) + " / " + str(
                ssd_run + gpu_run) + " = " + str(float(cpu_ssdgpu_improved_by_fso) / (ssd_run + gpu_run)) + "\n")
            f.write("average hops between cpu/ssd(gpu): " + str(avg_hops_between_fso_and_ssdgpu) + "\n")
        else:
            avg_hops_between_fso_and_ssdgpu = (cpu_ssdgpu_improved_by_fso * 2 + (
                        ssd_run + gpu_run - cpu_ssdgpu_improved_by_fso) * (torus_two_y + 1)) / float(ssd_run + gpu_run)
            f.write("fso betweeen cpu and ssd/gpu: " + str(fso_cpu_ssdgpu) + "\n")
            f.write("improved hops between cpu/ssd(gpu) by fso: " + str(cpu_ssdgpu_improved_by_fso) + " / " + str(
                ssd_run + gpu_run) + " = " + str(float(cpu_ssdgpu_improved_by_fso) / (ssd_run + gpu_run)) + "\n")
            f.write("average hops between cpu/ssd(gpu): " + str(avg_hops_between_fso_and_ssdgpu) + "\n")

    f.write("job x: " + str(avg_x) + "\n")
    f.write("job y: " + str(avg_y) + "\n")

    f.close()


# timestep = 0.5     150826 huyao scheduling->pwa  0.5->1 
timestep = 2
utilization = []
utilization_cpu = []
utilization_ssd = []
utilization_gpu = []
queuingjobs = []
total = 0


def dostat():
    global timestep
    global total
    global end
    global utilization
    global utilization_cpu
    global utilization_ssd
    global utilization_gpu
    global queuingjobs
    ts = 0  # time step
    #     total_utilization = 0.0
    #     f = open("stat_su", "w") #system utilization
    dt = str(datetime.datetime.now())
    dt = dt.replace(" ", "-")
    dt = dt.replace(".", "-")
    dt = dt.replace(":", "-")
    ar = MyPWA.archive.replace(".", "-")
    fn = dt + "_" + GUI.topo + "_" + str(tn) + "_" + arch + "_" + GUI.schedule + "_" + GUI.mode + "_" + str(
        GUI.fso_r) + "_fsoconfigtime_" + str(fso_config_time) + "_fso_cpu_ssdgpu_" + str(
        fso_cpu_ssdgpu) + "_" + GUI.speedup + "_" + ar  # file name
    f = open(fn, "w")  # system utilization
    f.write("#timestep  occupied  total  utilization  queuingjobs\n")
    f.close()
    #     while(stopwrite==False):
    while (True):
        total_cpu = 0
        total_ssd = 0
        total_gpu = 0
        for node in RG.nodes():
            total_cpu += RG.node[node]["cpu"]
            total_ssd += RG.node[node]["ssd"]
            total_gpu += RG.node[node]["gpu"]
        #             print RG.node[node]["cpu"], RG.node[node]["cpu"], RG.node[node]["cpu"]
        total = total_cpu + total_ssd + total_gpu

        ts = ts + 1
        uti_cpu = 1 - (float(total_cpu) / tn)
        uti_ssd = 1 - (float(total_ssd) / tn)
        uti_gpu = 1 - (float(total_gpu) / tn)
        uti = 1 - (float(total) / (tn * 3))
        #         total_utilization = total_utilization + uti
        #         print ts, "    ", total/tn
        utilization_cpu.append(uti_cpu)
        utilization_ssd.append(uti_ssd)
        utilization_gpu.append(uti_gpu)
        utilization.append(uti)
        queuing = len(queue)
        queuingjobs.append(queuing)
        s = str(ts * timestep) + "    " + str(tn * 3 - total) + "    " + str(tn * 3) + "    " + str(uti) + "    " + str(
            queuing) + "\n"  # 150826 huyao ts->ts*timestep
        f = open(fn, "a")  # system utilization
        f.write(s)
        f.close()
        time.sleep(timestep)
        #         print total_cpu, total_ssd, total_gpu, total, len(queue), all_submitted
        if (total == tn * 3 and len(queue) == 0 and all_submitted == True):
            end = time.time()
            f = open(fn, "a")
            #             average_utilization = total_utilization/ts
            average_utilization_cpu = sum(utilization_cpu) / len(utilization_cpu)
            average_utilization_ssd = sum(utilization_ssd) / len(utilization_ssd)
            average_utilization_gpu = sum(utilization_gpu) / len(utilization_gpu)
            average_utilization = sum(utilization) / len(utilization)
            f.write("\n")
            f.write("average cpu utilization is: " + str(average_utilization_cpu) + "\n")
            f.write("average ssd utilization is: " + str(average_utilization_ssd) + "\n")
            f.write("average gpu utilization is: " + str(average_utilization_gpu) + "\n")
            f.write("average utilization is: " + str(average_utilization) + "\n")
            average_queuingjobs = float(sum(queuingjobs)) / len(queuingjobs)
            max_queuingjobs = max(queuingjobs)
            f.write("average queuing jobs are: " + str(average_queuingjobs) + "\n")
            f.write("maximum queuing jobs are: " + str(max_queuingjobs) + "\n")
            f.close()
            output_queue_time(fn)

            print(" jump_1: ", str(jump_1), " jump_2: ", str(jump_2), " jump_3: ", str(jump_3))
            print("simulation is over!")
            break


sj = threading.Timer(0, submit_jobs)  # submit jobs
sj.start()

stat = threading.Timer(0, dostat)  # required processing time
stat.start()

transform = False
fill = 0

# 150821 huyao jobs_->queue  avoid any other job inserted during transform
# lock = False

# 150821 huyao available except FIFO
if (GUI.schedule == "LIFO"):
    queue.insert(0, queue.pop(-1))
first = queue[0]
first_num = queue[0][0]
first_cpu = queue[0][1][0]
first_time = queue[0][1][4]

first_ssd = queue[0][1][1]
first_gpu = queue[0][1][2]
# first_submit = queue[0][1][3]

# 150825 huyao to_first in normal = fso_not_found in fso
to_first = True

# 150913 huyao current g, original g
g = []
origin = []

# 151201 huyao
specified_cpu = 0
specified_time = 0
start = time.time()
end = 0.0

# while(len(queue)>0):
while (True):
    if (len(queue) > 0):

        #     print "haha", jobs_[0]
        #     print x
        #     print y
        #     print transform
        #     print tempX
        #     print tempY
        #     print fill

        # 150821 huyao available except FIFO
        #         if(lock==False):
        if (transform == False and to_first == True and fso_not_found == False):
            if (GUI.schedule == "LIFO"):
                queue.insert(0, queue.pop(-1))
            first = queue[0]
            first_num = queue[0][0]
            first_cpu = queue[0][1][0]
            first_time = queue[0][1][4]

            first_ssd = queue[0][1][1]
            first_gpu = queue[0][1][2]

            specified_cpu = first_cpu
            specified_time = first_time

            # 151222 huyao top of rack (tor) switch 160111
            if GUI.speedup == "tor" or (GUI.speedup == "tor-sub3d" and torus_d > 3):
                allnodes = tn * nodes_in_cabinet
                tb = (2 * allnodes - 1 + specified_cpu) / (2 * float(specified_cpu))  # time before
                first_cpu = (specified_cpu + nodes_in_cabinet - 1) / nodes_in_cabinet
                nodes = first_cpu * nodes_in_cabinet
                ta = (2 * allnodes - 1 + nodes) / (2 * float(nodes))
                first_time = (ta / tb) * specified_time
                #                 print "job", first, ": cpu# is changed from ", specified_cpu, " to ", first_cpu, "cabinets, runtime has been extended from ", specified_time, " to ", first_time
                specified_cpu = first_cpu
                specified_time = first_time

            if (first_cpu < 1 or first_cpu > tn or first_time < 0):
                print(datetime.datetime.now(), "job: ", first, " can not be scheduled due to errorous requests")
                queue.pop(0)
                reset()
                #         checkover()
                to_first = True
                continue

                # 151201 huyao expansion or shrinkage / backfilling
            #         if to_first == True:
            if GUI.speedup == "yes" or GUI.speedup == "tor" or (GUI.speedup == "tor-sub3d" and torus_d > 3):
                if ((tn - total) > specified_cpu * 2):
                    tb = (2 * tn - 1 + specified_cpu) / (2 * float(specified_cpu))  # time before
                    first_cpu = specified_cpu * 2  # two times
                    if (len(queue) == 1 and (tn - total) > specified_cpu * 4):
                        first_cpu = specified_cpu * 4  # four times
                    ta = (2 * tn - 1 + first_cpu) / (2 * float(first_cpu))  # time after
                    first_time = (ta / tb) * specified_time
                    print("job", first, ": cpu# is expanded from ", specified_cpu, " to ", first_cpu, ", runtime has been shortened from ", specified_time, " to ", first_time)
                elif ((tn - total) < specified_cpu):
                    if (tn - total) > specified_cpu / 4:
                        tb = (2 * tn - 1 + specified_cpu) / (2 * float(specified_cpu))
                        first_cpu = specified_cpu / 4
                        if first_cpu == 0:
                            first_cpu = 1
                        if ((tn - total) > specified_cpu / 2):
                            first_cpu = specified_cpu / 2
                            if first_cpu == 0:
                                first_cpu = 1
                        ta = (2 * tn - 1 + first_cpu) / (2 * float(first_cpu))
                        first_time = (ta / tb) * specified_time
                        print("job", first, ": cpu# is decreased from ", specified_cpu, " to ", first_cpu, ", runtime has been extended from ", specified_time, " to ", first_time)
                    else:  # backfilling
                        backfilling = False
                        for i in range(len(queue)):
                            if queue[i][1][0] <= tn - total:
                                queue.insert(0, queue.pop(i))
                                backfilling = True
                                break
                        if backfilling == True:
                            continue

        else:
            first_cpu = specified_cpu
            first_time = specified_time

        # 150819 huyao pure fso
        if (GUI.mode == "FSO"):
            fso()
            continue
        # 150922 huyao partial fso links
        #         if(GUI.mode=="FSO_random" and transform==True):
        if (GUI.mode == "FSO_random"):
            fso_random()
            continue

        if (transform == True):
            #             g = divi_torus(first_cpu+fill)
            #             if(g[0] == g[-1]):
            #                 reset()
            #                 torus_d = False
            #                 continue
            g.insert(0, g.pop(-1))
            if (g == origin):
                #             transform = False
                reset()
                #                 if(GUI.mode=="FSO"):
                #                     fso()
                to_first = False
                continue
        else:
            g = divi_torus(first_cpu + fill)
            origin = g  # required cpus
            if (torus_d == 2 and fill == 1 and (g[0] > torus_two_x or g[1] > torus_two_y)):
                print(datetime.datetime.now(), "job: ", first, " can not be scheduled due to lack of resources")
                queue.pop(0)
                to_first = True
                #             checkover()
                reset()
                continue
            if (g[0] > torus_two_x and g[0] == first_cpu):
                fill = 1
                to_first = False
                continue
        found = False  # allocated cpus
        if (torus_d == 2):  # 2-d
            for b in range(torus_two_y):
                for a in range(torus_two_x):
                    flag = True  # if each cpu is available in x*y grid
                    flag_ = True  # useful if fill!=0
                    for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                        for bbb in range(b, b + g[1]):
                            aaaa = aaa % torus_two_x
                            bbbb = bbb % torus_two_y
                            if (RG.node[(aaaa, bbbb)]["cpu"] == 0 and fill == 0):
                                flag = False
                                break
                            if (RG.node[(aaaa, bbbb)]["cpu"] == 0 and fill == 1):
                                if (flag_ == True):
                                    flag_ = False
                                else:
                                    flag = False
                                    break

                        if (flag == False):
                            break
                    if (flag == True):
                        print(datetime.datetime.now(), "job: ", first, " is scheduled to the nodes:")

                        jobs_dispatch[first_num] = time.time()
                        jobs_cpus[first_num] = first_cpu
                        jobs_runtime[first_num] = first_time

                        jobs_ssds[first_num] = first_ssd
                        jobs_gpus[first_num] = first_gpu

                        job_x.append(g[0])
                        job_y.append(g[1])

                        ava_to_unava = []
                        n = 0
                        if arch == "RS":
                            for aaa in range(a, a + g[0]):
                                for bbb in range(b, b + g[1]):
                                    aaaa = aaa % torus_two_x
                                    bbbb = bbb % torus_two_y
                                    if (aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and fill == 1 and
                                            RG.node[(aaaa, bbbb)]["cpu"] > 0):
                                        #                                     print xxx, yyy
                                        break
                                    if (RG.node[(aaaa, bbbb)]["cpu"] == 1):
                                        mylock.acquire()
                                        RG.node[(aaaa, bbbb)]["cpu"] = 0
                                        RG.node[(aaaa, bbbb)]["jobs"].append(first_num)
                                        #                                     print "(", aaaa, ", ", bbbb, ") "
                                        if first_ssd != 0 and n < first_ssd:
                                            RG.node[(aaaa, bbbb)]["ssd"] = 0
                                        if first_gpu != 0 and n < first_gpu:
                                            RG.node[(aaaa, bbbb)]["gpu"] = 0
                                        mylock.release()
                                        n = n + 1
                                        #                                     nodelist.append((aaaa,bbbb))
                                        # print RG.node[(xxx,yyy)]
                                        ava_to_unava.append((aaaa, bbbb))
                        #                             t = threading.Timer(jobs_[0][1][1], unlock, (RG.node[(xxx,yyy)], xxx, yyy, xx, yy, jobs_[0],)) #required processing time
                        #                             t.start()

                        if arch == "IRS-REPEAT":
                            cpu_ssdgpu = first_ssd + first_gpu
                            for aaa in range(a, a + g[0]):
                                for bbb in range(b, b + g[1]):
                                    aaaa = aaa % torus_two_x
                                    bbbb = bbb % torus_two_y
                                    if (aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and fill == 1 and
                                            RG.node[(aaaa, bbbb)]["cpu"] > 0):
                                        #                                     print xxx, yyy
                                        break
                                    if RG.node[(aaaa, bbbb)]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                        RG.node[(aaaa, bbbb)]["fso_cpu_ssdgpu"] -= 1
                                        cpu_ssdgpu -= 1
                                        RG.node[(aaaa, bbbb)][first_num] = 1
                                        cpu_ssdgpu_improved_by_fso += 1
                                        if RG.node[(aaaa, bbbb)]["fso_cpu_ssdgpu"] > 0 and cpu_ssdgpu > 0:
                                            RG.node[(aaaa, bbbb)]["fso_cpu_ssdgpu"] -= 1
                                            cpu_ssdgpu -= 1
                                            RG.node[(aaaa, bbbb)][first_num] = 2
                                            cpu_ssdgpu_improved_by_fso += 1
                                    if (RG.node[(aaaa, bbbb)]["cpu"] > 0):
                                        #                                         if RG.node[(aaaa,bbbb)]["cpu"] == 1:
                                        #                                             cpus_one[first_num] += 1
                                        #                                         elif RG.node[(aaaa,bbbb)]["cpu"] == 2:
                                        #                                             cpus_two[first_num] += 1
                                        #                                         elif RG.node[(aaaa,bbbb)]["cpu"] == 3:
                                        #                                             cpus_three[first_num] += 1
                                        mylock.acquire()
                                        RG.node[(aaaa, bbbb)]["cpu"] -= 1
                                        RG.node[(aaaa, bbbb)]["jobs"].append(first_num)
                                        x = aaaa
                                        ssd_y = bbbb + torus_two_y
                                        gpu_y = bbbb + (2 * torus_two_y)
                                        if first_ssd != 0 and n < first_ssd:
                                            RG.node[x, ssd_y]["ssd"] -= 1
                                            RG.node[x, ssd_y]["jobs"].append(first_num)
                                        if first_gpu != 0 and n < first_gpu:
                                            RG.node[x, gpu_y]["gpu"] -= 1
                                            RG.node[x, gpu_y]["jobs"].append(first_num)
                                        mylock.release()
                                        n = n + 1
                                        #                                     nodelist.append((aaaa,bbbb))
                                        # print RG.node[(xxx,yyy)]
                                        ava_to_unava.append((aaaa, bbbb))
                        #                             t = threading.Timer(jobs_[0][1][1], unlock, (RG.node[(xxx,yyy)], xxx, yyy, xx, yy, jobs_[0],)) #required processing time
                        #                             t.start()

                        if arch == "IRS-LOOP":
                            for aaa in range(a, a + g[0]):
                                for bbb in range(b, b + g[1]):
                                    aaaa = aaa % torus_two_x
                                    bbbb = bbb % torus_two_y
                                    if (aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and fill == 1 and
                                            RG.node[(aaaa, bbbb)]["cpu"] > 0):
                                        #                                     print xxx, yyy
                                        break
                                    if (RG.node[(aaaa, bbbb)]["cpu"] > 0):
                                        mylock.acquire()
                                        RG.node[(aaaa, bbbb)]["cpu"] -= 1
                                        RG.node[(aaaa, bbbb)]["cpu_jobs"].append(first_num)
                                        if first_ssd != 0 and n < first_ssd:
                                            RG.node[(aaaa, bbbb)]["ssd"] -= 1
                                            RG.node[(aaaa, bbbb)]["ssd_jobs"].append(first_num)
                                        if first_gpu != 0 and n < first_gpu:
                                            RG.node[(aaaa, bbbb)]["gpu"] -= 1
                                            RG.node[(aaaa, bbbb)]["gpu_jobs"].append(first_num)
                                        mylock.release()
                                        n = n + 1
                                        ava_to_unava.append((aaaa, bbbb))

                        jobs_cpus_nodes[first_num] = copy.copy(ava_to_unava)

                        t = threading.Timer(first_time, unlock_unava,
                                            (ava_to_unava, first,))  # required processing time
                        t.start()
                        queue.pop(0)
                        found = True
                        #                 transform = False
                        #                 fill = 0
                        reset()
                        to_first = True
                        break
                    if (a == torus_two_x - 1 and b == torus_two_y - 1):
                        transform = True
                if (found == True):
                    break
    elif (all_submitted == True):
        break

# nx.draw(RG, node_size=30, with_labels=True)  
# nx.draw_networkx_nodes(RG,pos,nodelist=[(0,0)],node_color='b')
# nx.draw_networkx_nodes(RG,nodelist=nodelist,node_color='b')
# plt.setp(plt.gca(), 'ylim', list(reversed(plt.getp(plt.gca(), 'ylim'))))
# plt.setp(plt.gca(), 'xlim', list(reversed(plt.getp(plt.gca(), 'xlim'))))
# plt.show(block = False)
# plt.show()

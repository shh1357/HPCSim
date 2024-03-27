'''
Created on 2015/09/10

@author: smallcat

torus
'''

# from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
# import itertools
import threading
import GUI
import PWA
import time
import datetime
# import Torus
import random

app = GUI.MyApp(0)  # Create an instance of the application class
app.MainLoop()  # Tell it to start processing events

RG = nx.Graph()

torus_d = int(GUI.topo[0])
# pos = {}

# 8*8*4*4*4 for 5-d torus, 8*8*8*8 for 4-d torus, 16*16*16 for 3-d torus, 64*64 for 2-d torus (4096)
# 16*8*4*2*2 for 5-d torus, 16*8*4*4 for 4-d torus, 16*16*8 for 3-d torus, 64*32 for 2-d torus (2048)
# 16*8*2*2*2 for 5-d torus, 16*8*4*2 for 4-d torus, 16*8*8 for 3-d torus, 32*32 for 2-d torus (1024)
aa = 16
bb = 8
cc = 2
dd = 2
ee = 2

tn = 1  # total nodes
fso_config_time = 5  # huyao 151016 s

# degree = dimention*2
# links = nodes*degree/2 = nodes*dimention (nodes>4)
if (torus_d == 2):  # 2-d torus 8*8
    tn = aa * bb
    RG = nx.grid_graph(dim=[aa, bb], periodic=True)
    #         pos = dict(zip(RG,RG))
    #     pos = nx.spring_layout(RG)
    for a in range(aa):
        for b in range(bb):
            #                 RG.add_node((a,b))
            RG.node[(a, b)]["ava"] = "yes"
            RG.node[(a, b)]["fso"] = 0
#             RG.node[(a,b)]["fso_ava"] = 0
if (torus_d == 3):  # 3-d torus 8*8*8
    tn = aa * bb * cc
    RG = nx.grid_graph(dim=[aa, bb, cc], periodic=True)
    #         pos = dict(zip(RG,RG))
    #     pos = nx.spring_layout(RG)
    for a in range(aa):
        for b in range(bb):
            for c in range(cc):
                #                     RG.add_node((a,b,c))
                RG.node[(a, b, c)]["ava"] = "yes"
                RG.node[(a, b, c)]["fso"] = 0
#                 RG.node[(a,b,c)]["fso_ava"] = 0
if (torus_d == 4):  # 4-d torus 8*8*8*4
    tn = aa * bb * cc * dd
    RG = nx.grid_graph(dim=[aa, bb, cc, dd], periodic=True)
    #         pos = dict(zip(RG,RG))
    #     pos = nx.spring_layout(RG)
    for a in range(aa):
        for b in range(bb):
            for c in range(cc):
                for d in range(dd):
                    #                         RG.add_node((a,b,c,d))
                    RG.node[(a, b, c, d)]["ava"] = "yes"
                    RG.node[(a, b, c, d)]["fso"] = 0
#                     RG.node[(a,b,c,d)]["fso_ava"] = 0
if (torus_d == 5):  # 5-d torus 8*8*8*4*4
    tn = aa * bb * cc * dd * ee
    RG = nx.grid_graph(dim=[aa, bb, cc, dd, ee], periodic=True)
    #         pos = dict(zip(RG,RG))
    #     pos = nx.spring_layout(RG)
    for a in range(aa):
        for b in range(bb):
            for c in range(cc):
                for d in range(dd):
                    for e in range(ee):
                        #                             RG.add_node((a,b,c,d,e))
                        RG.node[(a, b, c, d, e)]["ava"] = "yes"
                        RG.node[(a, b, c, d, e)]["fso"] = 0
#                         RG.node[(a,b,c,d,e)]["fso_ava"] = 0


# 150922 huyao
if (GUI.mode == "FSO_random"):
    #     fso_links = random.sample(RG.edges(), int(tn*torus_d*GUI.fso_r))

    #     fso_links = random.sample(RG.edges(), int(len(RG.edges())*GUI.fso_r))
    #
    #     for link in fso_links:
    #         RG.node[link[0]]["fso"] = RG.node[link[0]]["fso"]+1 #endnode0 of link
    #         RG.node[link[1]]["fso"] = RG.node[link[1]]["fso"]+1 #endnode1 of link

    # huyao 151114
    for node in RG.nodes():
        RG.node[node]["fso"] = int(GUI.fso_r * 100)

#         RG.node[link[0]]["fso_ava"] = RG.node[link[0]]["fso_ava"]+1 #endnode0 of link
#         RG.node[link[1]]["fso_ava"] = RG.node[link[1]]["fso_ava"]+1 #endnode1 of link
#     for i in RG.nodes():
#         if(RG.node[i]["fso"]>3):
#             print i


k = 10000.0
# k = 1.0

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

data = PWA.data
# for i in range(len(data)):
# 151016 huyao 10000
num_jobs = 1000
# num_jobs = len(data)
for i in range(num_jobs):
    #     jobs[i] = (data["Requested Number of Processors"][i], data["Requested Time"][i]/k)
    jobs[i] = (data["Number of Allocated Processors"][i], data["Run Time"][i] / k, data["Submit Time"][i] / k)
    jobs_submit[i] = 0.0
    jobs_dispatch[i] = 0.0

# jobs_ = zip(jobs.keys(), jobs.values())

job_samples = jobs.items()
queue = [job_samples[0]]

jobs_submit[0] = time.time()

# current = job_samples[0][1][2]
num = len(job_samples)
all_submitted = False


# lock = False
def submit_jobs():
    current = job_samples[0][1][2]
    global queue, all_submitted, jobs_submit
    for i in range(1, num):
        wait = job_samples[i][1][2] - current
        if (wait >= 0):
            time.sleep(wait)
            current = job_samples[i][1][2]
            queue.append(job_samples[i])

            # 150824 huyao
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
            print datetime.datetime.now(), "job: ", job_samples[i], " is submitted"

            jobs_submit[i] = time.time()
        else:
            print datetime.datetime.now(), "job: ", job_samples[i], " can not be submitted"
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

nodelist = []


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

def unlock_unava(nl, job):
    while (len(nl) > 0):
        RG.node[nl[0]]["ava"] = "yes"
        nodelist.remove(nl[0])
        nl.pop(0)
    print datetime.datetime.now(), "job: ", job, "is finished"


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
    global fso_not_found, jobs_dispatch, first_num

    if (torus_d == 2):  # 2-d torus 8*8
        for b in range(bb):
            for a in range(aa):
                if (RG.node[(a, b)]["ava"] == "yes"):
                    count = count + 1
                    ava_nodes.append((a, b))
                    if (count == first_cpu):
                        print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso):"

                        time.sleep(fso_config_time / k)

                        jobs_dispatch[first_num] = time.time()

                        for i in range(len(ava_nodes)):
                            RG.node[ava_nodes[i]]["ava"] = "no"
                            #                         print "(", ava_nodes[i][0], ", ", ava_nodes[i][1], ") "
                            nodelist.append(ava_nodes[i])
                        #                         t = threading.Timer(jobs_[0][1][1], unlock0, (RG.node[ava_nodes[i]], ava_nodes[i][0], ava_nodes[i][1], i, jobs_[0],)) #required processing time
                        #                         t.start()
                        t = threading.Timer(first_time, unlock_unava, (ava_nodes, first,))  # required processing time
                        t.start()
                        queue.pop(0)
                        #                     fill = 0
                        fso_not_found = False
                        return
                if (a == aa - 1 and b == bb - 1):
                    fso_not_found = True
    if (torus_d == 3):  # 3-d torus 8*8*8
        for c in range(cc):
            for b in range(bb):
                for a in range(aa):
                    if (RG.node[(a, b, c)]["ava"] == "yes"):
                        count = count + 1
                        ava_nodes.append((a, b, c))
                        if (count == first_cpu):
                            print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso):"

                            time.sleep(fso_config_time / k)

                            jobs_dispatch[first_num] = time.time()

                            for i in range(len(ava_nodes)):
                                RG.node[ava_nodes[i]]["ava"] = "no"
                                #                         print "(", ava_nodes[i][0], ", ", ava_nodes[i][1], ") "
                                nodelist.append(ava_nodes[i])
                            #                         t = threading.Timer(jobs_[0][1][1], unlock0, (RG.node[ava_nodes[i]], ava_nodes[i][0], ava_nodes[i][1], i, jobs_[0],)) #required processing time
                            #                         t.start()
                            t = threading.Timer(first_time, unlock_unava,
                                                (ava_nodes, first,))  # required processing time
                            t.start()
                            queue.pop(0)
                            #                     fill = 0
                            fso_not_found = False
                            return
                    if (a == aa - 1 and b == bb - 1 and c == cc - 1):
                        fso_not_found = True
    if (torus_d == 4):  # 4-d torus 8*8*8*4
        for d in range(dd):
            for c in range(cc):
                for b in range(bb):
                    for a in range(aa):
                        if (RG.node[(a, b, c, d)]["ava"] == "yes"):
                            count = count + 1
                            ava_nodes.append((a, b, c, d))
                            if (count == first_cpu):
                                print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso):"

                                time.sleep(fso_config_time / k)

                                jobs_dispatch[first_num] = time.time()

                                for i in range(len(ava_nodes)):
                                    RG.node[ava_nodes[i]]["ava"] = "no"
                                    #                         print "(", ava_nodes[i][0], ", ", ava_nodes[i][1], ") "
                                    nodelist.append(ava_nodes[i])
                                #                         t = threading.Timer(jobs_[0][1][1], unlock0, (RG.node[ava_nodes[i]], ava_nodes[i][0], ava_nodes[i][1], i, jobs_[0],)) #required processing time
                                #                         t.start()
                                t = threading.Timer(first_time, unlock_unava,
                                                    (ava_nodes, first,))  # required processing time
                                t.start()
                                queue.pop(0)
                                #                     fill = 0
                                fso_not_found = False
                                return
                        if (a == aa - 1 and b == bb - 1 and c == cc - 1 and d == dd - 1):
                            fso_not_found = True
    if (torus_d == 5):  # 5-d torus 8*8*8*4*4
        for e in range(ee):
            for d in range(dd):
                for c in range(cc):
                    for b in range(bb):
                        for a in range(aa):
                            if (RG.node[(a, b, c, d, e)]["ava"] == "yes"):
                                count = count + 1
                                ava_nodes.append((a, b, c, d, e))
                                if (count == first_cpu):
                                    print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso):"

                                    time.sleep(fso_config_time / k)

                                    jobs_dispatch[first_num] = time.time()

                                    for i in range(len(ava_nodes)):
                                        RG.node[ava_nodes[i]]["ava"] = "no"
                                        #                         print "(", ava_nodes[i][0], ", ", ava_nodes[i][1], ") "
                                        nodelist.append(ava_nodes[i])
                                    #                         t = threading.Timer(jobs_[0][1][1], unlock0, (RG.node[ava_nodes[i]], ava_nodes[i][0], ava_nodes[i][1], i, jobs_[0],)) #required processing time
                                    #                         t.start()
                                    t = threading.Timer(first_time, unlock_unava,
                                                        (ava_nodes, first,))  # required processing time
                                    t.start()
                                    queue.pop(0)
                                    #                     fill = 0
                                    fso_not_found = False
                                    return
                            if (a == aa - 1 and b == bb - 1 and c == cc - 1 and d == dd - 1 and e == ee - 1):
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
        if ((torus_d == 2 and fill == 1 and (g[0] > aa or g[1] > bb)) or
                (torus_d == 3 and fill == 1 and (g[0] > aa or g[1] > bb or g[2] > cc)) or
                (torus_d == 4 and fill == 1 and (g[0] > aa or g[1] > bb or g[2] > cc or g[3] > dd)) or
                (torus_d == 5 and fill == 1 and (g[0] > aa or g[1] > bb or g[2] > cc or g[3] > dd or g[4] > ee))):
            print datetime.datetime.now(), "job: ", first, " can not be scheduled due to lack of resources"
            queue.pop(0)
            to_first = True
            #             checkover()
            reset()
            #             continue
            return
        if (g[0] > aa and g[0] == first_cpu):
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
        for b in range(bb):
            for a in range(aa):
                flag = True  # if each cpu is available in x*y grid
                flag_ = True  # useful if fill!=0
                noused = []
                for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                    for bbb in range(b, b + g[1]):
                        aaaa = aaa % aa
                        bbbb = bbb % bb
                        if (RG.node[(aaaa, bbbb)]["ava"] == "no" and fill == 0):
                            flag = False
                            break
                        if (RG.node[(aaaa, bbbb)]["ava"] == "no" and fill == 1):
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
                    print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                        fso_ratio) + " : "
                    print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"
                    jobs_dispatch[first_num] = time.time()
                    ava_to_unava = []
                    for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                        for bbb in range(b, b + g[1]):
                            aaaa = aaa % aa
                            bbbb = bbb % bb
                            if (fill == 1 and len(noused) > 0):
                                if ((aaaa, bbbb) == noused[0]):
                                    continue
                            RG.node[(aaaa, bbbb)]["ava"] = "no"
                            nodelist.append((aaaa, bbbb))
                            ava_to_unava.append((aaaa, bbbb))
                    t = threading.Timer(first_time, unlock_unava, (ava_to_unava, first,))  # required processing time
                    t.start()
                    queue.pop(0)
                    reset()
                    to_first = True
                    return

        for b in range(bb):
            for a in range(aa):

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
                        aaaa = aaa % aa
                        bbbb = bbb % bb
                        sub.append((aaaa, bbbb))
                        if (RG.node[(aaaa, bbbb)]["ava"] == "no"):
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
                    #                     if(ratio < fso_ratio):
                    #                     print fso_ratio
                    #                     fso_ratio = ratio
                    #                     fn = current_fn
                    #                     sub = current_sub
                    #                     nouse = current_nouse
                    #                         if(ratio < 0.05):
                    #                     sub_found = True
                    #                     break
                    #             if(sub_found==True):
                    #                 break

                    #                     #huyao 151018 normal first, fso follows
                    #                     if(fso_ratio > 0):
                    #                         for b_ in range(b,bb):
                    #                             for a_ in range(a,aa):
                    #                                 better = True #if each cpu is available in x*y grid
                    #                                 better_ = True #useful if fill!=0
                    #                                 noused = []
                    #                                 for aaa in range(a_, a_+g[0]): #ergodic in x*y grid
                    #                                     for bbb in range(b_, b_+g[1]):
                    #                                         aaaa = aaa%aa
                    #                                         bbbb = bbb%bb
                    #                                         if(RG.node[(aaaa,bbbb)]["ava"] == "no" and fill == 0):
                    #                                             better = False
                    #                                             break
                    #                                         if(RG.node[(aaaa,bbbb)]["ava"] == "no" and fill == 1):
                    #                                             if(better_ == True):
                    #                                                 better_ = False
                    #                                                 noused.append((aaaa,bbbb))
                    #                                             else:
                    #                                                 better = False
                    #                                                 break
                    #                                     if(better == False):
                    #                                         break
                    #                                 if(better == True):
                    # #                                     fso_to_normal = fso_to_normal+1
                    # #                                     print datetime.datetime.now(), "fso to normal: ", fso_to_normal
                    # #                                     fn = []
                    #                                     fso_ratio = 0.0
                    # #                                     sub = [] #sub graph
                    # #                                     nouse = [] #not used nodes (fill==1)
                    #                                     print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(fso_ratio) + " : "
                    #                                     print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"
                    #                                     jobs_dispatch[first_num] = time.time()
                    #                                     ava_to_unava = []
                    #
                    #                                     for aaa in range(a_, a_+g[0]): #ergodic in x*y grid
                    #                                         for bbb in range(b_, b_+g[1]):
                    #                                             aaaa = aaa%aa
                    #                                             bbbb = bbb%bb
                    #                                             if(fill==1 and (aaaa,bbbb)==noused[0]):
                    #                                                 continue
                    #                                             RG.node[(aaaa,bbbb)]["ava"] = "no"
                    #                                             nodelist.append((aaaa,bbbb))
                    #                                             ava_to_unava.append((aaaa,bbbb))
                    #
                    #                                     t = threading.Timer(first_time, unlock_unava, (ava_to_unava, first,)) #required processing time
                    #                                     t.start()
                    #                                     queue.pop(0)
                    #
                    #                                     reset()
                    #                                     to_first = True
                    #
                    #                                     return

                    #                     print len(fn)
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
                                if (RG.node[n]["ava"] == "yes"):
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
                                    if (fill == 1 and RG.node[nouse[0]]["ava"] == "yes" and RG.node[nouse[0]]["fso"] >=
                                            each[1]):
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
                        print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                            fso_ratio) + " : "

                        if (fso_ratio > 0.0):
                            fso_used = fso_used + 1
                            time.sleep(fso_config_time / k)

                        print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"

                        jobs_dispatch[first_num] = time.time()

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
                        for node in sub:
                            if (node not in fn):
                                if (fill == 1 and node == nouse[0]):
                                    continue
                                RG.node[node]["ava"] = "no"
                                nodelist.append(node)
                                ava_to_unava.append(node)

                        for each in subnodes:
                            RG.node[each]["ava"] = "no"
                            #                                     print "(", aaaa, ", ", bbbb, ") "
                            nodelist.append(each)
                            # print RG.node[(xxx,yyy)]
                            ava_to_unava.append(each)

                            #                         if(fill==1 and nouse[0] in ava_to_unava):
                        #                             RG.node[nouse[0]]["ava"] = "yes"
                        #                             nodelist.remove(nouse[0])
                        #                             ava_to_unava.remove(nouse[0])

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

                if (a == aa - 1 and b == bb - 1):
                    #                     if normal_to_fso == False:
                    #                         normal_to_fso==True
                    #                     else:
                    transform_fso_random = True
    #             if(found == True):
    #                 break

    if (torus_d == 3):
        # huyao 151019 normal first, fso follows
        for c in range(cc):
            for b in range(bb):
                for a in range(aa):
                    flag = True  # if each cpu is available in x*y grid
                    flag_ = True  # useful if fill!=0
                    noused = []
                    for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                        for bbb in range(b, b + g[1]):
                            for ccc in range(c, c + g[2]):
                                aaaa = aaa % aa
                                bbbb = bbb % bb
                                cccc = ccc % cc
                                if (RG.node[(aaaa, bbbb, cccc)]["ava"] == "no" and fill == 0):
                                    flag = False
                                    break
                                if (RG.node[(aaaa, bbbb, cccc)]["ava"] == "no" and fill == 1):
                                    if (flag_ == True):
                                        flag_ = False
                                        noused.append((aaaa, bbbb, cccc))
                                    else:
                                        flag = False
                                        break
                            if (flag == False):
                                break
                        if (flag == False):
                            break
                    if (flag == True):
                        fso_ratio = 0.0
                        print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                            fso_ratio) + " : "
                        print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"
                        jobs_dispatch[first_num] = time.time()
                        ava_to_unava = []
                        for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                            for bbb in range(b, b + g[1]):
                                for ccc in range(c, c + g[2]):
                                    aaaa = aaa % aa
                                    bbbb = bbb % bb
                                    cccc = ccc % cc
                                    if (fill == 1 and len(noused) > 0):
                                        if ((aaaa, bbbb, cccc) == noused[0]):
                                            continue
                                    RG.node[(aaaa, bbbb, cccc)]["ava"] = "no"
                                    nodelist.append((aaaa, bbbb, cccc))
                                    ava_to_unava.append((aaaa, bbbb, cccc))
                        t = threading.Timer(first_time, unlock_unava,
                                            (ava_to_unava, first,))  # required processing time
                        t.start()
                        queue.pop(0)
                        reset()
                        to_first = True
                        return

        for c in range(cc):
            for b in range(bb):
                for a in range(aa):
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
                            for ccc in range(c, c + g[2]):
                                aaaa = aaa % aa
                                bbbb = bbb % bb
                                cccc = ccc % cc
                                sub.append((aaaa, bbbb, cccc))
                                if (RG.node[(aaaa, bbbb, cccc)]["ava"] == "no"):
                                    if (fill == 0):
                                        fn.append((aaaa, bbbb, cccc))

                                        if (len(fn) > lowest_fso_nodes):
                                            over = True
                                            break

                                    if (fill == 1):
                                        if (flag_ == True):
                                            flag_ = False
                                            nouse.append((aaaa, bbbb, cccc))
                                        else:
                                            fn.append((aaaa, bbbb, cccc))

                                            if (len(fn) > lowest_fso_nodes):
                                                over = True
                                                break

                                if (fill == 1 and aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and ccc == c + g[
                                    2] - 1 and len(nouse) == 0):
                                    nouse.append((aaaa, bbbb, cccc))
                            if (over == True):
                                break
                        if (over == True):
                            break
                    if (over == False):
                        fso_ratio = float(len(fn)) / first_cpu

                        for node in fn:
                            fl = 0  # fso links
                            for neighbor in RG.neighbors(node):
                                if (neighbor in sub):
                                    if (RG.node[neighbor]["fso"] == 0):
                                        flag = False
                                        break
                                    fl = fl + 1
                                    nn.append(neighbor)
                            if (flag == False):
                                break
                            fnl.append((node, fl))

                        if (flag == True):
                            nnn = list(set(nn))
                            if (fill == 1 and nouse[0] in nnn):
                                nnn.remove(nouse[0])
                            for item in nnn:
                                if (RG.node[item]["fso"] < nn.count(item)):
                                    flag = False
                                    break

                        if (flag == True):
                            for each in fnl:
                                RG_ = RG.copy()
                                RG_.remove_nodes_from(sub)
                                for n in RG_.nodes():
                                    if (RG.node[n]["ava"] == "yes"):
                                        if (RG.node[n]["fso"] >= each[1]):
                                            subnodes.append(n)
                                            break
                                    if (n == RG_.nodes()[-1]):
                                        if (fill == 1 and RG.node[nouse[0]]["ava"] == "yes" and RG.node[nouse[0]][
                                            "fso"] >= each[1]):
                                            subnodes.append(nouse[0])
                                            break
                                        else:
                                            flag = False
                                            break
                                if (flag == False):
                                    break

                        if (flag == True):
                            print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                                fso_ratio) + " : "

                            if (fso_ratio > 0.0):
                                fso_used = fso_used + 1
                                time.sleep(fso_config_time / k)

                            print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"

                            jobs_dispatch[first_num] = time.time()

                            ava_to_unava = []

                            for node in sub:
                                if (node not in fn):
                                    if (fill == 1 and node == nouse[0]):
                                        continue
                                    RG.node[node]["ava"] = "no"
                                    nodelist.append(node)
                                    ava_to_unava.append(node)

                            for each in subnodes:
                                RG.node[each]["ava"] = "no"
                                #                                     print "(", aaaa, ", ", bbbb, ") "
                                nodelist.append(each)
                                # print RG.node[(xxx,yyy)]
                                ava_to_unava.append(each)

                            t = threading.Timer(first_time, unlock_unava,
                                                (ava_to_unava, first,))  # required processing time
                            t.start()
                            queue.pop(0)
                            reset()
                            to_first = True
                            return
                    if (a == aa - 1 and b == bb - 1 and c == cc - 1):
                        transform_fso_random = True

    if (torus_d == 4):
        # huyao 151019 normal first, fso follows
        for d in range(dd):
            for c in range(cc):
                for b in range(bb):
                    for a in range(aa):
                        flag = True  # if each cpu is available in x*y grid
                        flag_ = True  # useful if fill!=0
                        noused = []
                        for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                            for bbb in range(b, b + g[1]):
                                for ccc in range(c, c + g[2]):
                                    for ddd in range(d, d + g[3]):
                                        aaaa = aaa % aa
                                        bbbb = bbb % bb
                                        cccc = ccc % cc
                                        dddd = ddd % dd
                                        if (RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] == "no" and fill == 0):
                                            flag = False
                                            break
                                        if (RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] == "no" and fill == 1):
                                            if (flag_ == True):
                                                flag_ = False
                                                noused.append((aaaa, bbbb, cccc, dddd))
                                            else:
                                                flag = False
                                                break
                                    if (flag == False):
                                        break
                                if (flag == False):
                                    break
                            if (flag == False):
                                break
                        if (flag == True):
                            fso_ratio = 0.0
                            print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                                fso_ratio) + " : "
                            print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"
                            jobs_dispatch[first_num] = time.time()
                            ava_to_unava = []
                            for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                                for bbb in range(b, b + g[1]):
                                    for ccc in range(c, c + g[2]):
                                        for ddd in range(d, d + g[3]):
                                            aaaa = aaa % aa
                                            bbbb = bbb % bb
                                            cccc = ccc % cc
                                            dddd = ddd % dd
                                            if (fill == 1 and len(noused) > 0):
                                                if ((aaaa, bbbb, cccc, dddd) == noused[0]):
                                                    continue
                                            RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] = "no"
                                            nodelist.append((aaaa, bbbb, cccc, dddd))
                                            ava_to_unava.append((aaaa, bbbb, cccc, dddd))
                            t = threading.Timer(first_time, unlock_unava,
                                                (ava_to_unava, first,))  # required processing time
                            t.start()
                            queue.pop(0)
                            reset()
                            to_first = True
                            return

        for d in range(dd):
            for c in range(cc):
                for b in range(bb):
                    for a in range(aa):
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
                                for ccc in range(c, c + g[2]):
                                    for ddd in range(d, d + g[3]):
                                        aaaa = aaa % aa
                                        bbbb = bbb % bb
                                        cccc = ccc % cc
                                        dddd = ddd % dd
                                        sub.append((aaaa, bbbb, cccc, dddd))
                                        if (RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] == "no"):
                                            if (fill == 0):
                                                fn.append((aaaa, bbbb, cccc, dddd))

                                                if (len(fn) > lowest_fso_nodes):
                                                    over = True
                                                    break

                                            if (fill == 1):
                                                if (flag_ == True):
                                                    flag_ = False
                                                    nouse.append((aaaa, bbbb, cccc, dddd))
                                                else:
                                                    fn.append((aaaa, bbbb, cccc, dddd))

                                                    if (len(fn) > lowest_fso_nodes):
                                                        over = True
                                                        break

                                        if (fill == 1 and aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and ccc == c + g[
                                            2] - 1 and ddd == d + g[3] - 1 and len(nouse) == 0):
                                            nouse.append((aaaa, bbbb, cccc, dddd))
                                    if (over == True):
                                        break
                                if (over == True):
                                    break
                            if (over == True):
                                break
                        if (over == False):
                            fso_ratio = float(len(fn)) / first_cpu

                            for node in fn:
                                fl = 0  # fso links
                                for neighbor in RG.neighbors(node):
                                    if (neighbor in sub):
                                        if (RG.node[neighbor]["fso"] == 0):
                                            flag = False
                                            break
                                        fl = fl + 1
                                        nn.append(neighbor)
                                if (flag == False):
                                    break
                                fnl.append((node, fl))

                            if (flag == True):
                                nnn = list(set(nn))
                                if (fill == 1 and nouse[0] in nnn):
                                    nnn.remove(nouse[0])
                                for item in nnn:
                                    if (RG.node[item]["fso"] < nn.count(item)):
                                        flag = False
                                        break

                            if (flag == True):
                                for each in fnl:
                                    RG_ = RG.copy()
                                    RG_.remove_nodes_from(sub)
                                    for n in RG_.nodes():
                                        if (RG.node[n]["ava"] == "yes"):
                                            if (RG.node[n]["fso"] >= each[1]):
                                                subnodes.append(n)
                                                break
                                        if (n == RG_.nodes()[-1]):
                                            if (fill == 1 and RG.node[nouse[0]]["ava"] == "yes" and RG.node[nouse[0]][
                                                "fso"] >= each[1]):
                                                subnodes.append(nouse[0])
                                                break
                                            else:
                                                flag = False
                                                break
                                    if (flag == False):
                                        break

                            if (flag == True):
                                print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                                    fso_ratio) + " : "

                                if (fso_ratio > 0.0):
                                    fso_used = fso_used + 1
                                    time.sleep(fso_config_time / k)

                                print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"

                                jobs_dispatch[first_num] = time.time()

                                ava_to_unava = []

                                for node in sub:
                                    if (node not in fn):
                                        if (fill == 1 and node == nouse[0]):
                                            continue
                                        RG.node[node]["ava"] = "no"
                                        nodelist.append(node)
                                        ava_to_unava.append(node)

                                for each in subnodes:
                                    RG.node[each]["ava"] = "no"
                                    #                                     print "(", aaaa, ", ", bbbb, ") "
                                    nodelist.append(each)
                                    # print RG.node[(xxx,yyy)]
                                    ava_to_unava.append(each)

                                t = threading.Timer(first_time, unlock_unava,
                                                    (ava_to_unava, first,))  # required processing time
                                t.start()
                                queue.pop(0)
                                reset()
                                to_first = True
                                return
                        if (a == aa - 1 and b == bb - 1 and c == cc - 1 and d == dd - 1):
                            transform_fso_random = True
    if (torus_d == 5):
        # huyao 151019 normal first, fso follows
        for e in range(ee):
            for d in range(dd):
                for c in range(cc):
                    for b in range(bb):
                        for a in range(aa):
                            flag = True  # if each cpu is available in x*y grid
                            flag_ = True  # useful if fill!=0
                            noused = []
                            for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                                for bbb in range(b, b + g[1]):
                                    for ccc in range(c, c + g[2]):
                                        for ddd in range(d, d + g[3]):
                                            for eee in range(e, e + g[4]):
                                                aaaa = aaa % aa
                                                bbbb = bbb % bb
                                                cccc = ccc % cc
                                                dddd = ddd % dd
                                                eeee = eee % ee
                                                if (RG.node[(aaaa, bbbb, cccc, dddd, eeee)][
                                                    "ava"] == "no" and fill == 0):
                                                    flag = False
                                                    break
                                                if (RG.node[(aaaa, bbbb, cccc, dddd, eeee)][
                                                    "ava"] == "no" and fill == 1):
                                                    if (flag_ == True):
                                                        flag_ = False
                                                        noused.append((aaaa, bbbb, cccc, dddd, eeee))
                                                    else:
                                                        flag = False
                                                        break
                                            if (flag == False):
                                                break
                                        if (flag == False):
                                            break
                                    if (flag == False):
                                        break
                                if (flag == False):
                                    break
                            if (flag == True):
                                fso_ratio = 0.0
                                print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                                    fso_ratio) + " : "
                                print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"
                                jobs_dispatch[first_num] = time.time()
                                ava_to_unava = []
                                for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                                    for bbb in range(b, b + g[1]):
                                        for ccc in range(c, c + g[2]):
                                            for ddd in range(d, d + g[3]):
                                                for eee in range(e, e + g[4]):
                                                    aaaa = aaa % aa
                                                    bbbb = bbb % bb
                                                    cccc = ccc % cc
                                                    dddd = ddd % dd
                                                    eeee = eee % ee
                                                    if (fill == 1 and len(noused) > 0):
                                                        if ((aaaa, bbbb, cccc, dddd, eeee) == noused[0]):
                                                            continue
                                                    RG.node[(aaaa, bbbb, cccc, dddd, eeee)]["ava"] = "no"
                                                    nodelist.append((aaaa, bbbb, cccc, dddd, eeee))
                                                    ava_to_unava.append((aaaa, bbbb, cccc, dddd, eeee))
                                t = threading.Timer(first_time, unlock_unava,
                                                    (ava_to_unava, first,))  # required processing time
                                t.start()
                                queue.pop(0)
                                reset()
                                to_first = True
                                return

        for e in range(ee):
            for d in range(dd):
                for c in range(cc):
                    for b in range(bb):
                        for a in range(aa):
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
                                    for ccc in range(c, c + g[2]):
                                        for ddd in range(d, d + g[3]):
                                            for eee in range(e, e + g[4]):
                                                aaaa = aaa % aa
                                                bbbb = bbb % bb
                                                cccc = ccc % cc
                                                dddd = ddd % dd
                                                eeee = eee % ee
                                                sub.append((aaaa, bbbb, cccc, dddd, eeee))
                                                if (RG.node[(aaaa, bbbb, cccc, dddd, eeee)]["ava"] == "no"):
                                                    if (fill == 0):
                                                        fn.append((aaaa, bbbb, cccc, dddd, eeee))

                                                        if (len(fn) > lowest_fso_nodes):
                                                            over = True
                                                            break

                                                    if (fill == 1):
                                                        if (flag_ == True):
                                                            flag_ = False
                                                            nouse.append((aaaa, bbbb, cccc, dddd, eeee))
                                                        else:
                                                            fn.append((aaaa, bbbb, cccc, dddd, eeee))

                                                            if (len(fn) > lowest_fso_nodes):
                                                                over = True
                                                                break

                                                if (fill == 1 and aaa == a + g[0] - 1 and bbb == b + g[
                                                    1] - 1 and ccc == c + g[2] - 1 and ddd == d + g[
                                                    3] - 1 and eee == e + g[4] - 1 and len(nouse) == 0):
                                                    nouse.append((aaaa, bbbb, cccc, dddd, eeee))
                                            if (over == True):
                                                break
                                        if (over == True):
                                            break
                                    if (over == True):
                                        break
                                if (over == True):
                                    break
                            if (over == False):
                                fso_ratio = float(len(fn)) / first_cpu

                                for node in fn:
                                    fl = 0  # fso links
                                    for neighbor in RG.neighbors(node):
                                        if (neighbor in sub):
                                            if (RG.node[neighbor]["fso"] == 0):
                                                flag = False
                                                break
                                            fl = fl + 1
                                            nn.append(neighbor)
                                    if (flag == False):
                                        break
                                    fnl.append((node, fl))

                                if (flag == True):
                                    nnn = list(set(nn))
                                    if (fill == 1 and nouse[0] in nnn):
                                        nnn.remove(nouse[0])
                                    for item in nnn:
                                        if (RG.node[item]["fso"] < nn.count(item)):
                                            flag = False
                                            break

                                if (flag == True):
                                    for each in fnl:
                                        RG_ = RG.copy()
                                        RG_.remove_nodes_from(sub)
                                        for n in RG_.nodes():
                                            if (RG.node[n]["ava"] == "yes"):
                                                if (RG.node[n]["fso"] >= each[1]):
                                                    subnodes.append(n)
                                                    break
                                            if (n == RG_.nodes()[-1]):
                                                if (fill == 1 and RG.node[nouse[0]]["ava"] == "yes" and
                                                        RG.node[nouse[0]]["fso"] >= each[1]):
                                                    subnodes.append(nouse[0])
                                                    break
                                                else:
                                                    flag = False
                                                    break
                                        if (flag == False):
                                            break

                                if (flag == True):
                                    print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso_random), with fso_ratio " + str(
                                        fso_ratio) + " : "

                                    if (fso_ratio > 0.0):
                                        fso_used = fso_used + 1
                                        time.sleep(fso_config_time / k)

                                    print datetime.datetime.now(), "fso links are used for ", str(fso_used), " times"

                                    jobs_dispatch[first_num] = time.time()

                                    ava_to_unava = []

                                    for node in sub:
                                        if (node not in fn):
                                            if (fill == 1 and node == nouse[0]):
                                                continue
                                            RG.node[node]["ava"] = "no"
                                            nodelist.append(node)
                                            ava_to_unava.append(node)

                                    for each in subnodes:
                                        RG.node[each]["ava"] = "no"
                                        #                                     print "(", aaaa, ", ", bbbb, ") "
                                        nodelist.append(each)
                                        # print RG.node[(xxx,yyy)]
                                        ava_to_unava.append(each)

                                    t = threading.Timer(first_time, unlock_unava,
                                                        (ava_to_unava, first,))  # required processing time
                                    t.start()
                                    queue.pop(0)
                                    reset()
                                    to_first = True
                                    return
                            if (a == aa - 1 and b == bb - 1 and c == cc - 1 and d == dd - 1 and e == ee - 1):
                                transform_fso_random = True


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
def output_queue_time():
    dt = str(datetime.datetime.now())
    dt = dt.replace(" ", "-")
    dt = dt.replace(".", "-")
    dt = dt.replace(":", "-")
    ar = PWA.archive.replace(".", "-")
    fn = "stat_queue_" + dt + "_" + GUI.topo + "_" + str(tn) + "_" + GUI.schedule + "_" + GUI.mode + "_" + str(
        GUI.fso_r) + "_fsoconfigtime_" + str(fso_config_time) + "_" + ar  # file name
    f = open(fn, "w")  # system utilization
    f.write("#job_number  submit  dispatch  queue\n")
    num = 0
    total_queue_time = 0.0
    for i in range(num_jobs):
        queue_time = jobs_dispatch[i] - jobs_submit[i]
        s = str(i) + "    " + str(jobs_submit[i]) + "    " + str(jobs_dispatch[i]) + "    " + str(queue_time) + "\n"
        f.write(s)
        if (jobs_dispatch[i] > 0.0):
            num = num + 1
            total_queue_time = total_queue_time + queue_time
    avg_queue_time = total_queue_time / num
    f.write("dispatched jobs are: " + str(num) + " out of " + str(num_jobs) + "\n")
    f.write("average queue time is: " + str(avg_queue_time) + "\n")
    f.write("fso links are used for " + str(fso_used) + " times" + "\n")
    f.close()


# timestep = 0.5     150826 huyao scheduling->pwa  0.5->1 
timestep = 2
utilization = []
queuingjobs = []


def dostat():
    global timestep
    ts = 0  # time step
    #     total_utilization = 0.0
    #     f = open("stat_su", "w") #system utilization
    dt = str(datetime.datetime.now())
    dt = dt.replace(" ", "-")
    dt = dt.replace(".", "-")
    dt = dt.replace(":", "-")
    ar = PWA.archive.replace(".", "-")
    fn = "stat_su_" + dt + "_" + GUI.topo + "_" + str(tn) + "_" + GUI.schedule + "_" + GUI.mode + "_" + str(
        GUI.fso_r) + "_fsoconfigtime_" + str(fso_config_time) + "_" + ar  # file name
    f = open(fn, "w")  # system utilization
    f.write("#timestep  occupied  total  utilization  queuingjobs\n")
    f.close()
    #     while(stopwrite==False):
    while (True):
        total = 0

        if (torus_d == 2):  # 2-d torus 8*8
            for a in range(aa):
                for b in range(bb):
                    if (RG.node[(a, b)]["ava"] == "no"):
                        total = total + 1
        if (torus_d == 3):  # 3-d torus 8*8*8
            for a in range(aa):
                for b in range(bb):
                    for c in range(cc):
                        if (RG.node[(a, b, c)]["ava"] == "no"):
                            total = total + 1
        if (torus_d == 4):  # 4-d torus 8*8*8*4
            for a in range(aa):
                for b in range(bb):
                    for c in range(cc):
                        for d in range(dd):
                            if (RG.node[(a, b, c, d)]["ava"] == "no"):
                                total = total + 1
        if (torus_d == 5):  # 5-d torus 8*8*8*4*4
            for a in range(aa):
                for b in range(bb):
                    for c in range(cc):
                        for d in range(dd):
                            for e in range(ee):
                                if (RG.node[(a, b, c, d, e)]["ava"] == "no"):
                                    total = total + 1

        ts = ts + 1
        uti = float(total) / tn
        #         total_utilization = total_utilization + uti
        #         print ts, "    ", total/tn
        utilization.append(uti)
        queuing = len(queue)
        queuingjobs.append(queuing)
        s = str(ts * timestep) + "    " + str(total) + "    " + str(tn) + "    " + str(uti) + "    " + str(
            queuing) + "\n"  # 150826 huyao ts->ts*timestep
        f = open(fn, "a")  # system utilization
        f.write(s)
        f.close()
        time.sleep(timestep)
        if (total == 0 and len(queue) == 0 and all_submitted == True):
            f = open(fn, "a")
            #             average_utilization = total_utilization/ts
            average_utilization = sum(utilization) / len(utilization)
            f.write("average utilization is: " + str(average_utilization) + "\n")
            average_queuingjobs = float(sum(queuingjobs)) / len(queuingjobs)
            max_queuingjobs = max(queuingjobs)
            f.write("average queuing jobs are: " + str(average_queuingjobs) + "\n")
            f.write("maximum queuing jobs are: " + str(max_queuingjobs) + "\n")
            f.close()
            output_queue_time()
            print " jump_1: ", str(jump_1), " jump_2: ", str(jump_2), " jump_3: ", str(jump_3)
            print "simulation is over!"
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
first_time = queue[0][1][1]

# 150825 huyao to_first in normal = fso_not_found in fso
to_first = True

# 150913 huyao current g, original g
g = []
origin = []

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
            first_time = queue[0][1][1]

            if (first_cpu < 1 or first_cpu > tn or first_time < 0):
                print datetime.datetime.now(), "job: ", first, " can not be scheduled due to errorous requests"
                queue.pop(0)
                reset()
                #         checkover()
                to_first = True
                continue

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
            if ((torus_d == 2 and fill == 1 and (g[0] > aa or g[1] > bb)) or
                    (torus_d == 3 and fill == 1 and (g[0] > aa or g[1] > bb or g[2] > cc)) or
                    (torus_d == 4 and fill == 1 and (g[0] > aa or g[1] > bb or g[2] > cc or g[3] > dd)) or
                    (torus_d == 5 and fill == 1 and (g[0] > aa or g[1] > bb or g[2] > cc or g[3] > dd or g[4] > ee))):
                print datetime.datetime.now(), "job: ", first, " can not be scheduled due to lack of resources"
                queue.pop(0)
                to_first = True
                #             checkover()
                reset()
                continue
            if (g[0] > aa and g[0] == first_cpu):
                fill = 1
                to_first = False
                continue
        found = False  # allocated cpus
        if (torus_d == 2):  # 2-d torus 8*8
            for b in range(bb):
                for a in range(aa):
                    flag = True  # if each cpu is available in x*y grid
                    flag_ = True  # useful if fill!=0
                    for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                        for bbb in range(b, b + g[1]):
                            aaaa = aaa % aa
                            bbbb = bbb % bb
                            if (RG.node[(aaaa, bbbb)]["ava"] == "no" and fill == 0):
                                flag = False
                                break
                            if (RG.node[(aaaa, bbbb)]["ava"] == "no" and fill == 1):
                                if (flag_ == True):
                                    flag_ = False
                                else:
                                    flag = False
                                    break

                        if (flag == False):
                            break
                    if (flag == True):
                        print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes:"

                        jobs_dispatch[first_num] = time.time()

                        all = True
                        ava_to_unava = []
                        for aaa in range(a, a + g[0]):
                            for bbb in range(b, b + g[1]):
                                aaaa = aaa % aa
                                bbbb = bbb % bb
                                if (aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and fill == 1 and all == True and
                                        RG.node[(aaaa, bbbb)]["ava"] == "yes"):
                                    #                                     print xxx, yyy
                                    break
                                if (RG.node[(aaaa, bbbb)]["ava"] == "yes"):
                                    RG.node[(aaaa, bbbb)]["ava"] = "no"
                                    #                                     print "(", aaaa, ", ", bbbb, ") "
                                    nodelist.append((aaaa, bbbb))
                                    # print RG.node[(xxx,yyy)]
                                    ava_to_unava.append((aaaa, bbbb))
                                #                             t = threading.Timer(jobs_[0][1][1], unlock, (RG.node[(xxx,yyy)], xxx, yyy, xx, yy, jobs_[0],)) #required processing time
                                #                             t.start()
                                else:
                                    all = False
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
                    if (a == aa - 1 and b == bb - 1):
                        transform = True
                if (found == True):
                    break
        if (torus_d == 3):  # 3-d torus 8*8*8
            for c in range(cc):
                for b in range(bb):
                    for a in range(aa):
                        flag = True  # if each cpu is available in x*y grid
                        flag_ = True  # useful if fill!=0
                        for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                            for bbb in range(b, b + g[1]):
                                for ccc in range(c, c + g[2]):
                                    aaaa = aaa % aa
                                    bbbb = bbb % bb
                                    cccc = ccc % cc
                                    if (RG.node[(aaaa, bbbb, cccc)]["ava"] == "no" and fill == 0):
                                        flag = False
                                        break
                                    if (RG.node[(aaaa, bbbb, cccc)]["ava"] == "no" and fill == 1):
                                        if (flag_ == True):
                                            flag_ = False
                                        else:
                                            flag = False
                                            break
                                if (flag == False):
                                    break
                            if (flag == False):
                                break
                        if (flag == True):
                            print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes:"

                            jobs_dispatch[first_num] = time.time()

                            all = True
                            ava_to_unava = []
                            for aaa in range(a, a + g[0]):
                                for bbb in range(b, b + g[1]):
                                    for ccc in range(c, c + g[2]):
                                        aaaa = aaa % aa
                                        bbbb = bbb % bb
                                        cccc = ccc % cc
                                        if (aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and ccc == c + g[
                                            2] - 1 and fill == 1 and all == True and RG.node[(aaaa, bbbb, cccc)][
                                            "ava"] == "yes"):
                                            #                                     print xxx, yyy
                                            break
                                        if (RG.node[(aaaa, bbbb, cccc)]["ava"] == "yes"):
                                            RG.node[(aaaa, bbbb, cccc)]["ava"] = "no"
                                            #                             print "(", xxx, ", ", yyy, ") "
                                            nodelist.append((aaaa, bbbb, cccc))
                                            # print RG.node[(xxx,yyy)]
                                            ava_to_unava.append((aaaa, bbbb, cccc))
                                        #                             t = threading.Timer(jobs_[0][1][1], unlock, (RG.node[(xxx,yyy)], xxx, yyy, xx, yy, jobs_[0],)) #required processing time
                                        #                             t.start()
                                        else:
                                            all = False
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
                        if (a == aa - 1 and b == bb - 1 and c == cc - 1):
                            transform = True
                    if (found == True):
                        break
                if (found == True):
                    break
        if (torus_d == 4):  # 4-d torus 8*8*8*4
            for d in range(dd):
                for c in range(cc):
                    for b in range(bb):
                        for a in range(aa):
                            flag = True  # if each cpu is available in x*y grid
                            flag_ = True  # useful if fill!=0
                            for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                                for bbb in range(b, b + g[1]):
                                    for ccc in range(c, c + g[2]):
                                        for ddd in range(d, d + g[3]):
                                            aaaa = aaa % aa
                                            bbbb = bbb % bb
                                            cccc = ccc % cc
                                            dddd = ddd % dd
                                            if (RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] == "no" and fill == 0):
                                                flag = False
                                                break
                                            if (RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] == "no" and fill == 1):
                                                if (flag_ == True):
                                                    flag_ = False
                                                else:
                                                    flag = False
                                                    break
                                        if (flag == False):
                                            break
                                    if (flag == False):
                                        break
                                if (flag == False):
                                    break
                            if (flag == True):
                                print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes:"

                                jobs_dispatch[first_num] = time.time()

                                all = True
                                ava_to_unava = []
                                for aaa in range(a, a + g[0]):
                                    for bbb in range(b, b + g[1]):
                                        for ccc in range(c, c + g[2]):
                                            for ddd in range(d, d + g[3]):
                                                aaaa = aaa % aa
                                                bbbb = bbb % bb
                                                cccc = ccc % cc
                                                dddd = ddd % dd
                                                if (aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and ccc == c + g[
                                                    2] - 1 and ddd == d + g[3] - 1 and fill == 1 and all == True and
                                                        RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] == "yes"):
                                                    #                                     print xxx, yyy
                                                    break
                                                if (RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] == "yes"):
                                                    RG.node[(aaaa, bbbb, cccc, dddd)]["ava"] = "no"
                                                    #                             print "(", xxx, ", ", yyy, ") "
                                                    nodelist.append((aaaa, bbbb, cccc, dddd))
                                                    # print RG.node[(xxx,yyy)]
                                                    ava_to_unava.append((aaaa, bbbb, cccc, dddd))
                                                #                             t = threading.Timer(jobs_[0][1][1], unlock, (RG.node[(xxx,yyy)], xxx, yyy, xx, yy, jobs_[0],)) #required processing time
                                                #                             t.start()
                                                else:
                                                    all = False
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
                            if (a == aa - 1 and b == bb - 1 and c == cc - 1 and d == dd - 1):
                                transform = True
                        if (found == True):
                            break
                    if (found == True):
                        break
                if (found == True):
                    break
        if (torus_d == 5):  # 5-d torus 8*8*8*4*4
            for e in range(ee):
                for d in range(dd):
                    for c in range(cc):
                        for b in range(bb):
                            for a in range(aa):
                                flag = True  # if each cpu is available in x*y grid
                                flag_ = True  # useful if fill!=0
                                for aaa in range(a, a + g[0]):  # ergodic in x*y grid
                                    for bbb in range(b, b + g[1]):
                                        for ccc in range(c, c + g[2]):
                                            for ddd in range(d, d + g[3]):
                                                for eee in range(e, e + g[4]):
                                                    aaaa = aaa % aa
                                                    bbbb = bbb % bb
                                                    cccc = ccc % cc
                                                    dddd = ddd % dd
                                                    eeee = eee % ee
                                                    if (RG.node[(aaaa, bbbb, cccc, dddd, eeee)][
                                                        "ava"] == "no" and fill == 0):
                                                        flag = False
                                                        break
                                                    if (RG.node[(aaaa, bbbb, cccc, dddd, eeee)][
                                                        "ava"] == "no" and fill == 1):
                                                        if (flag_ == True):
                                                            flag_ = False
                                                        else:
                                                            flag = False
                                                            break
                                                if (flag == False):
                                                    break
                                            if (flag == False):
                                                break
                                        if (flag == False):
                                            break
                                    if (flag == False):
                                        break
                                if (flag == True):
                                    print datetime.datetime.now(), "job: ", first, " is scheduled to the nodes:"

                                    jobs_dispatch[first_num] = time.time()

                                    all = True
                                    ava_to_unava = []
                                    for aaa in range(a, a + g[0]):
                                        for bbb in range(b, b + g[1]):
                                            for ccc in range(c, c + g[2]):
                                                for ddd in range(d, d + g[3]):
                                                    for eee in range(e, e + g[4]):
                                                        aaaa = aaa % aa
                                                        bbbb = bbb % bb
                                                        cccc = ccc % cc
                                                        dddd = ddd % dd
                                                        eeee = eee % ee
                                                        if (aaa == a + g[0] - 1 and bbb == b + g[1] - 1 and ccc == c +
                                                                g[2] - 1 and ddd == d + g[3] - 1 and eee == e + g[
                                                                    4] - 1 and fill == 1 and all == True and
                                                                RG.node[(aaaa, bbbb, cccc, dddd, eeee)][
                                                                    "ava"] == "yes"):
                                                            #                                     print xxx, yyy
                                                            break
                                                        if (RG.node[(aaaa, bbbb, cccc, dddd, eeee)]["ava"] == "yes"):
                                                            RG.node[(aaaa, bbbb, cccc, dddd, eeee)]["ava"] = "no"
                                                            #                             print "(", xxx, ", ", yyy, ") "
                                                            nodelist.append((aaaa, bbbb, cccc, dddd, eeee))
                                                            # print RG.node[(xxx,yyy)]
                                                            ava_to_unava.append((aaaa, bbbb, cccc, dddd, eeee))
                                                        #                             t = threading.Timer(jobs_[0][1][1], unlock, (RG.node[(xxx,yyy)], xxx, yyy, xx, yy, jobs_[0],)) #required processing time
                                                        #                             t.start()
                                                        else:
                                                            all = False
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
                                if (a == aa - 1 and b == bb - 1 and c == cc - 1 and d == dd - 1 and e == ee - 1):
                                    transform = True
                            if (found == True):
                                break
                        if (found == True):
                            break
                    if (found == True):
                        break
                if (found == True):
                    break
    elif (all_submitted == True):
        break

nx.draw(RG, node_size=30, with_labels=True)
# nx.draw_networkx_nodes(RG,pos,nodelist=[(0,0)],node_color='b')
nx.draw_networkx_nodes(RG, nodelist=nodelist, node_color='b')
plt.setp(plt.gca(), 'ylim', list(reversed(plt.getp(plt.gca(), 'ylim'))))
# plt.setp(plt.gca(), 'xlim', list(reversed(plt.getp(plt.gca(), 'xlim'))))
# plt.show(block = False)
plt.show()

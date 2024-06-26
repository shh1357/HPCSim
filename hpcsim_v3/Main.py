'''
Created on 2015/07/17

@author: smallcat

grid
'''

# from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
# import itertools
import threading
#from . import GUI
import GUI
import PWA
import time
import datetime

# import Torus

# xa = 5  #grid length
# ya = 5  #grid width

app = GUI.MyApp(0)  # Create an instance of the application class
app.MainLoop()  # Tell it to start processing events

# torus_d = 1

xa = GUI.xxxx
ya = GUI.yyyy

# RG = nx.Graph()   
# pos = dict(zip(RG,RG))  

# if(GUI.topo == "grid"): 
RG = nx.grid_2d_graph(xa, ya)
pos = dict(list(zip(RG, RG)))

for i in range(xa):
    for j in range(ya):
        RG.nodes[(i, j)]["ava"] = "yes"  # node availabitily
# else:
#     torus_d = int(GUI.topo[0])
#     if(torus_d == 2): #8*8
#         RG = nx.grid_graph(dim=[8,8], periodic=True)
# #         pos = dict(zip(RG,RG)) 
#         for a in range(8):
#             for b in range(8):
# #                 RG.add_node((a,b))
#                 RG.node[(a,b)]["ava"] = "yes"
#     if(torus_d == 3): #8*8*8
#         RG = nx.grid_graph(dim=[8,8,8], periodic=True)
# #         pos = dict(zip(RG,RG)) 
#         for a in range(8):
#             for b in range(8):
#                 for c in range(8):
# #                     RG.add_node((a,b,c))
#                     RG.node[(a,b,c)]["ava"] = "yes"
#     if(torus_d == 4): #8*8*8*4
#         RG = nx.grid_graph(dim=[8,8,8,4], periodic=True)
# #         pos = dict(zip(RG,RG)) 
#         for a in range(8):
#             for b in range(8):
#                 for c in range(8):
#                     for d in range(4):
# #                         RG.add_node((a,b,c,d))
#                         RG.node[(a,b,c,d)]["ava"] = "yes"
#     if(torus_d == 5): #8*8*8*4*4
#         RG = nx.grid_graph(dim=[8,8,8,4,4], periodic=True)
# #         pos = dict(zip(RG,RG)) 
#         for a in range(8):
#             for b in range(8):
#                 for c in range(8):
#                     for d in range(4):
#                         for e in range(4):
# #                             RG.add_node((a,b,c,d,e))
#                             RG.node[(a,b,c,d,e)]["ava"] = "yes"


k = 100000.0

# nx.write_adjlist(RG,"test.adjlist")

jobs = {}

# jobs[0] = (4,8)   #job number, required cpus, required time (in seconds)
# jobs[1] = (2,4)
# jobs[2] = (6,8)
# jobs[3] = (2,1)
# jobs[4] = (4,4)
# jobs[5] = (2,3)
# jobs[6] = (4,8)
# jobs[7] = (6,5)
# jobs[8] = (1,7)
# jobs[9] = (5,2)
# jobs[10] = (5,6)
# jobs[11] = (-1,2)

data = PWA.data
for i in range(len(data)):
    #     jobs[i] = (data["Requested Number of Processors"][i], data["Requested Time"][i]/k)
    jobs[i] = (data["Number of Allocated Processors"][i], data["Run Time"][i] / k, data["Submit Time"][i] / k)

# jobs = []
# jobs.append(0, (4,800))
# jobs.append(1, (2,400))
# jobs.append(2, (6,800))
# jobs.append(3, (2,100))
# jobs.append(4, (4,400))
# jobs.append(5, (2,300))
# jobs.append(6, (4,800))
# jobs.append(7, (6,500))


# jobs_ = zip(jobs.keys(), jobs.values())

job_samples = list(jobs.items())
queue = [job_samples[0]]
# current = job_samples[0][1][2]
#num = len(job_samples)
num = 100
all_submitted = False


# lock = False
def submit_jobs():
    current = job_samples[0][1][2]
    global queue, all_submitted
    global wait_sum
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
            #wait_sum = wait_sum + wait
            print(datetime.datetime.now(), "job: ", job_samples[i], " is submitted")
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


def divi(n, start=2):
    if (n == 1):
        return 1, 1
    for i in range(start, n + 1):
        if (n % i == 0):
            return i, int(n / i)  # i width; n/i length


# def unlock(node, endx, endy, endxx, endyy, job): 
#     node["ava"] = "yes"
#     nodelist.remove((endx,endy))
#     if(endx==endxx and endy==endyy):
#         print datetime.datetime.now(), "job: ", job, "is finished"

def unlock_unava(nl, job):
    while (len(nl) > 0):
        RG.nodes[nl[0]]["ava"] = "yes"
        nodelist.remove(nl[0])
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
    global fso_not_found
    for yy in range(ya):
        for xx in range(xa):
            if (RG.nodes[(xx, yy)]["ava"] == "yes"):
                count = count + 1
                ava_nodes.append((xx, yy))
                if (count == first_cpu):
                    print(datetime.datetime.now(), "job: ", first, " is scheduled to the nodes (fso):")
                    for i in range(len(ava_nodes)):
                        RG.nodes[ava_nodes[i]]["ava"] = "no"
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
            if (xx == xa - 1 and yy == ya - 1):
                fso_not_found = True


def reset():
    global x
    global y
    global transform
    global tempX
    global tempY
    global fill
    #     global lock
    x = 0
    y = 0
    transform = False
    tempX = 0
    tempY = 0
    fill = 0


#     lock = False

# stopwrite = False

# def checkover():
#     if(len(queue)<1):
#         global stopwrite
#         stopwrite = True 

# timestep = 0.5     150826 huyao scheduling->pwa  0.5->1 
timestep = 1


def dostat():
    global timestep
    ts = 0  # time step
    tn = xa * ya  # total nodes
    #     f = open("stat_su", "w") #system utilization
    dt = str(datetime.datetime.now())
    dt = dt.replace(" ", "-")
    dt = dt.replace(".", "-")
    dt = dt.replace(":", "-")
    ar = PWA.archive.replace(".", "-")
    fn = "stat_su_" + dt + "_" + str(xa * ya) + "_" + GUI.schedule + "_" + GUI.mode + "_" + ar  # file name
    f = open(fn, "w")  # system utilization
    f.write("#timestep  occupied  total  utilization\n")
    f.close()
    #     while(stopwrite==False):
    while (True):
        total = 0
        for ax in range(ya):
            for ay in range(xa):
                if (RG.nodes[(ax, ay)]["ava"] == "no"):
                    total = total + 1
        ts = ts + 1
        #         print ts, "    ", total/tn
        s = str(ts * timestep) + "    " + str(total) + "    " + str(tn) + "    " + str(
            float(total) / tn) + "\n"  # 150826 huyao ts->ts*timestep
        f = open(fn, "a")  # system utilization
        f.write(s)
        f.close()
        time.sleep(timestep)
        if (total == 0 and len(queue) == 0 and all_submitted == True):
            break


sj = threading.Timer(0, submit_jobs)  # submit jobs
sj.start()

stat = threading.Timer(0, dostat)  # required processing time
stat.start()

x = 0
y = 0
transform = False
tempX = 0
tempY = 0
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


#wait_times = []
wait_sum = 0

#for i in range(1, num):
#    wait_times[i] = 0

# while(len(queue)>0):
while (True):
    if (len(queue) > 0):
        wait_sum = wait_sum + 1

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

            if (first_cpu < 1 or first_cpu > xa * ya or first_time < 0):
                print(datetime.datetime.now(), "job: ", first, " can not be scheduled due to errorous requests")
                queue.pop(0)
                reset()
                #         checkover()
                to_first = True
                continue

                # 150819 huyao pure fso
        if (GUI.mode == "FSO"):
            fso()
            continue

        if (transform == True):
            #             while(True):
            #                 if(lock==False):
            #                     break
            g = divi(first_cpu + fill, tempY + 1)
            x = g[1]
            y = g[0]
            if (x == 1 and y > 2):
                #             transform = False
                reset()
                #                 if(GUI.mode=="FSO"):
                #                     fso()
                to_first = False
                continue
        else:
            g = divi(first_cpu + fill)  # required cpus
            x = g[1]  # length
            y = g[0]  # width
        while (x > xa):
            g = divi(first_cpu + fill, y + 1)
            x = g[1]
            y = g[0]
        if (y > ya):
            if (transform == False):
                print(datetime.datetime.now(), "job: ", first, " can not be scheduled due to lack of resources")
                queue.pop(0)
                to_first = True
            #             checkover()
            else:
                to_first = False
            reset()
            continue
        if (x == 1 and y > 2):
            fill = 1
            g = divi(first_cpu + fill)
            x = g[1]  # length
            y = g[0]  # width
        found = False  # allocated cpus
        for yy in range(ya - y + 1):  # left top vertex of x*y grid
            for xx in range(xa - x + 1):
                flag = True  # if each cpu is available in x*y grid
                flag_ = True  # useful if fill!=0
                for xxx in range(xx, xx + x):  # ergodic in x*y grid
                    for yyy in range(yy, yy + y):
                        if (RG.nodes[(xxx, yyy)]["ava"] == "no" and fill == 0):
                            flag = False
                            break
                        if (RG.nodes[(xxx, yyy)]["ava"] == "no" and fill == 1):
                            if (flag_ == True):
                                flag_ = False
                            else:
                                flag = False
                                break

                    if (flag == False):
                        break
                if (flag == True):
                    print(datetime.datetime.now(), "job: ", first, " is scheduled to the nodes:")
                    all = True
                    ava_to_unava = []
                    for xxx in range(xx, xx + x):
                        for yyy in range(yy, yy + y):
                            if (xxx == xx + x - 1 and yyy == yy + y - 1 and fill == 1 and all == True and
                                    RG.nodes[(xxx, yyy)]["ava"] == "yes"):
                                #                                 print xxx, yyy
                                break
                            if (RG.nodes[(xxx, yyy)]["ava"] == "yes"):
                                RG.nodes[(xxx, yyy)]["ava"] = "no"
                                #                             print "(", xxx, ", ", yyy, ") "
                                nodelist.append((xxx, yyy))
                                # print RG.node[(xxx,yyy)]
                                ava_to_unava.append((xxx, yyy))
                            #                             t = threading.Timer(jobs_[0][1][1], unlock, (RG.node[(xxx,yyy)], xxx, yyy, xx, yy, jobs_[0],)) #required processing time
                            #                             t.start()
                            else:
                                all = False
                    t = threading.Timer(first_time, unlock_unava, (ava_to_unava, first,))  # required processing time
                    t.start()
                    queue.pop(0)
                    found = True
                    #                 transform = False
                    #                 fill = 0
                    reset()
                    to_first = True
                    break
                if (yy == ya - y and xx == xa - x):
                    # 150821 huyao check if any other job inserted during transform
                    #                     if(first_num != queue[0][0]):
                    #                         reset()
                    #                         break
                    # print datetime.datetime.now(), "job: ", jobs_[0], " can not be scheduled due to no available resources"
                    # jobs_.pop(0)    #temp
                    # 150828 huyao
                    if (first_cpu == 2):
                        reset()
                        to_first = False
                    transform = True
                    #                     lock = True
                    tempX = x
                    tempY = y
            if (found == True):
                break
                # print len(jobs_)
    elif (all_submitted == True):
        break

# nx.draw(RG, pos, node_size=30, with_labels=True)
# # nx.draw_networkx_nodes(RG,pos,nodelist=[(0,0)],node_color='b')
# nx.draw_networkx_nodes(RG, pos, nodelist=nodelist, node_color='b')
# plt.setp(plt.gca(), 'ylim', list(reversed(plt.getp(plt.gca(), 'ylim'))))
# # plt.setp(plt.gca(), 'xlim', list(reversed(plt.getp(plt.gca(), 'xlim'))))
# # plt.show(block = False)
# plt.show()


print("-------------", xa, "wait_sum: ", wait_sum.real/100.0)

"""
Created on 2015/07/17

@author: smallcat

grid
"""

# from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
# import itertools
import threading
# from . import GUI
import GUI
import PWA
import time
import datetime
# import Torus


# simulation constants
TIMESTEP_UNIT = 1
SPEED_UP_FACTOR = 100000.0
NUM_SIMULATION_JOBS = 100

# global variables
size_grid_x = 0
size_grid_y = 0
RG = None
all_jobs = None
job_queue = None
all_jobs_submitted = False
result_wait_sum = 0

#wait_times = []
#for i in range(1, num):
#    wait_times[i] = 0


def set_gui_parameters():
    app = GUI.MyApp(0)  # Create an instance of the application class
    app.MainLoop()  # Tell it to start processing events


def initialize_graph():
    global size_grid_x, size_grid_y
    set_gui_parameters()
    # torus_d = 1
    # xa = 5  # grid length
    # ya = 5  # grid width
    size_grid_x = GUI.xxxx  # grid length
    size_grid_y = GUI.yyyy  # grid width
    initialize_RG()


def initialize_RG():
    global RG
    # RG = nx.Graph()
    # pos = dict(zip(RG,RG))

    # if(GUI.topo == "grid"):
    RG = nx.grid_2d_graph(size_grid_x, size_grid_y)
    # pos = dict(list(zip(RG, RG)))

    for i in range(size_grid_x):
        for j in range(size_grid_y):
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


# nx.write_adjlist(RG,"test.adjlist")


def initialize_all_jobs_list():
    global all_jobs
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
        jobs[i] = (data["Number of Allocated Processors"][i], data["Run Time"][i] / SPEED_UP_FACTOR, data["Submit Time"][i] / SPEED_UP_FACTOR)
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
    all_jobs = list(jobs.items())


def initialize_job_queue():
    global job_queue
    job_queue = [all_jobs[0]]
    # 150821 huyao available except FIFO
    if (GUI.schedule == "LIFO"):
        job_queue.insert(0, job_queue.pop(-1))


def submit_jobs():
    current_time = all_jobs[0][1][2]
    global job_queue, all_jobs_submitted
    for i in range(1, NUM_SIMULATION_JOBS):
        wait_time = all_jobs[i][1][2] - current_time
        if (wait_time >= 0):
            time.sleep(wait_time)
            current_time = all_jobs[i][1][2]
            job_queue.append(all_jobs[i])

            # 150824 huyao
            #             global lock
            #             lock = True
            if (GUI.schedule == "BF"):
                # 150824 huyao first unchanged during insertion
                one = job_queue.pop(0)
                job_queue = sorted(job_queue, key=lambda abc: abc[1], reverse=True)
                job_queue.insert(0, one)
            if (GUI.schedule == "SF"):
                one = job_queue.pop(0)
                job_queue = sorted(job_queue, key=lambda abc: abc[1])
                job_queue.insert(0, one)
            #             if(GUI.schedule == "LIFO"):
            #                 queue.insert(1, queue.pop(-1))
            #             lock = False
            print(datetime.datetime.now(), "job: ", all_jobs[i], " is submitted")
        else:
            print(datetime.datetime.now(), "job: ", all_jobs[i], " can not be submitted")
            i = i + 1
        if (i == NUM_SIMULATION_JOBS - 1):
            all_jobs_submitted = True


# jobs_ = jobs.items()    #dic -> tuple
# if(GUI.schedule == "BF"):
#     jobs_ = sorted(jobs.items(), key=lambda abc:abc[1], reverse=True)
# if(GUI.schedule == "SF"):
#     jobs_ = sorted(jobs.items(), key=lambda abc:abc[1])   

# print jobs_ 

# print RG.nodes(data = True)
# print RG.edges()


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

def unlock_unavailable(nl, job):
    while (len(nl) > 0):
        RG.nodes[nl[0]]["ava"] = "yes"
        nodelist_to_draw.remove(nl[0])
        nl.pop(0)
    #print(datetime.datetime.now(), "job: ", job, "is finished")


#     checkover()

# def unlock0(node, x, y, i, job): 
#     node["ava"] = "yes"
#     nodelist.remove((x,y))
#     if(i==0):
#         print datetime.datetime.now(), "job: ", job, "is finished"
# 150825 huyao

def qubo_allocation(first_job, first_job_cpu, first_job_time):
    global RG, all_jobs
    # you can do anything
    # return True if you have successfully allocated the first job
    return False


def fso(first_job, first_job_cpu, first_job_time):
    count = 0
    ava_nodes = []
    # global fso_not_found
    for yy in range(size_grid_y):
        for xx in range(size_grid_x):
            if (RG.nodes[(xx, yy)]["ava"] == "yes"):
                count = count + 1
                ava_nodes.append((xx, yy))
                if (count == first_job_cpu):
                    print(datetime.datetime.now(), "job: ", first_job, " is scheduled to the nodes (fso):")
                    for i in range(len(ava_nodes)):
                        RG.nodes[ava_nodes[i]]["ava"] = "no"
                        #                         print "(", ava_nodes[i][0], ", ", ava_nodes[i][1], ") "
                        nodelist_to_draw.append(ava_nodes[i])
                    # t = threading.Timer(jobs_[0][1][1], unlock0, (RG.node[ava_nodes[i]], ava_nodes[i][0],
                    # ava_nodes[i][1], i, jobs_[0],)) #required processing time
                    # t.start()
                    t = threading.Timer(first_job_time, unlock_unavailable, (ava_nodes, first_job,))  # required processing time
                    t.start()
                    job_queue.pop(0)
                    #                     fill = 0
                    # fso_not_found = False
                    # return
                    return False
            # if (xx == size_grid_x - 1 and yy == size_grid_y - 1):
            #     fso_not_found = True
    return True


#     lock = False

# stopwrite = False

# def checkover():
#     if(len(queue)<1):
#         global stopwrite
#         stopwrite = True 



def dostat():
    # global timestep
    # timestep = 0.5     150826 huyao scheduling->pwa  0.5->1
    # timestep = TIMESTEP

    wall_time_step = 0  # time step
    total_nodes_num = size_grid_x * size_grid_y  # total nodes
    #     f = open("stat_su", "w") #system utilization
    date_time_now = str(datetime.datetime.now()).replace(" ", "-").replace(".", "-").replace(":", "-")
    # date_time_now = date_time_now.replace(" ", "-")
    # date_time_now = date_time_now.replace(".", "-")
    # date_time_now = date_time_now.replace(":", "-")
    archive_name = PWA.archive.replace(".", "-")
    file_name = "stat_su_" + date_time_now + "_" + str(size_grid_x * size_grid_y) + "_" + GUI.schedule + "_" + GUI.mode + "_" + archive_name  # file name
    file_handle = open(file_name, "w")  # system utilization
    file_handle.write("#timestep  occupied  total  utilization\n")
    file_handle.close()
    #     while(stopwrite==False):
    while (True):
        total_time_step = 0
        for ax in range(size_grid_y):
            for ay in range(size_grid_x):
                if (RG.nodes[(ax, ay)]["ava"] == "no"):
                    total_time_step = total_time_step + TIMESTEP_UNIT
        wall_time_step = wall_time_step + TIMESTEP_UNIT
        #         print ts, "    ", total/tn
        log_message = (str(wall_time_step * TIMESTEP_UNIT) + "    " + str(total_time_step) + "    " + str(total_nodes_num) + "    "
                       + str(float(total_time_step) / total_nodes_num) + "\n")  # 150826 huyao ts->ts*timestep
        file_handle = open(file_name, "a")  # system utilization
        file_handle.write(log_message)
        file_handle.close()
        time.sleep(TIMESTEP_UNIT)
        if (total_time_step == 0 and len(job_queue) == 0 and all_jobs_submitted == True):
            break


def start_jobs_submitting_thread():
    sj = threading.Timer(0, submit_jobs)  # submit jobs
    sj.start()


def start_dostat_thread():
    stat = threading.Timer(0, dostat)  # required processing time
    stat.start()

nodelist_to_draw = []

def loop_allocate_all_jobs():
    global result_wait_sum

    fso_not_found = False
    # global to_first
    # 150825 huyao to_first in normal = fso_not_found in fso
    to_first = True

    # global first, first_num, first_cpu, first_time
    first = job_queue[0]
    first_num = job_queue[0][0]
    first_cpu = job_queue[0][1][0]
    first_time = job_queue[0][1][1]

    #
    x = 0
    y = 0
    transform = False
    temp_x = 0
    temp_y = 0
    fill = 0
    # 150821 huyao jobs_->queue  avoid any other job inserted during transform
    # lock = False

    def reset():
        # global x, y, fill, transform, tempX, tempY
        nonlocal x, y, fill, transform , temp_x, temp_y
        x = 0
        y = 0
        transform = False
        temp_x = 0
        temp_y = 0
        fill = 0


    # while(len(queue)>0):
    while (True):

        if (len(job_queue) > 0):
            result_wait_sum = result_wait_sum + 1

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
                    job_queue.insert(0, job_queue.pop(-1))
                first = job_queue[0]
                first_num = job_queue[0][0]
                first_cpu = job_queue[0][1][0]
                first_time = job_queue[0][1][1]

                if (first_cpu < 1 or first_cpu > size_grid_x * size_grid_y or first_time < 0):
                    print(datetime.datetime.now(), "job: ", first, " can not be scheduled due to errorous requests")
                    job_queue.pop(0)
                    reset()
                    #         checkover()
                    to_first = True
                    continue

                    # 150819 huyao pure fso
            if (GUI.mode == "FSO"):
                fso_not_found = fso(first, first_cpu, first_time)
                continue

            if (GUI.mode == "QUBO"):
                fso_not_found = qubo_allocation(first, first_cpu, first_time)
                continue

            if (transform == True):
                #             while(True):
                #                 if(lock==False):
                #                     break
                g = divi(first_cpu + fill, temp_y + 1)
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

            while (x > size_grid_x):
                g = divi(first_cpu + fill, y + 1)
                x = g[1]
                y = g[0]

            if (y > size_grid_y):
                if (transform == False):
                    print(datetime.datetime.now(), "job: ", first, " can not be scheduled due to lack of resources")
                    job_queue.pop(0)
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
            for yy in range(size_grid_y - y + 1):  # left top vertex of x*y grid
                for xx in range(size_grid_x - x + 1):
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
                                    nodelist_to_draw.append((xxx, yyy))
                                    # print RG.node[(xxx,yyy)]
                                    ava_to_unava.append((xxx, yyy))
                                #                             t = threading.Timer(jobs_[0][1][1], unlock, (RG.node[(xxx,yyy)], xxx, yyy, xx, yy, jobs_[0],)) #required processing time
                                #                             t.start()
                                else:
                                    all = False
                        t = threading.Timer(first_time, unlock_unavailable,
                                            (ava_to_unava, first,))  # required processing time
                        t.start()
                        job_queue.pop(0)
                        found = True
                        #                 transform = False
                        #                 fill = 0
                        reset()
                        to_first = True
                        break
                    if (yy == size_grid_y - y and xx == size_grid_x - x):
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
                        temp_x = x
                        temp_y = y
                if (found == True):
                    break
                    # print len(jobs_)
        elif (all_jobs_submitted == True):
            break


def simulation_main():
    initialize_graph()
    initialize_all_jobs_list()
    initialize_job_queue()

    # start two threads
    start_jobs_submitting_thread()
    start_dostat_thread()

    # job allocation
    loop_allocate_all_jobs()

    if (False):
        draw_image()

    print("", flush=True)
    print("-------------", size_grid_x, "wait_sum: ", result_wait_sum.real / 100.0)


simulation_main()

def draw_image():
    pos = dict(list(zip(RG, RG)))
    nx.draw(RG, pos, node_size=30, with_labels=True)
    # nx.draw_networkx_nodes(RG,pos,nodelist=[(0,0)],node_color='b')
    nx.draw_networkx_nodes(RG, pos, nodelist=nodelist_to_draw, node_color='b')
    plt.setp(plt.gca(), 'ylim', list(reversed(plt.getp(plt.gca(), 'ylim'))))
    # plt.setp(plt.gca(), 'xlim', list(reversed(plt.getp(plt.gca(), 'xlim'))))
    # plt.show(block = False)
    plt.show()



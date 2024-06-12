'''
Created on 2016/05/22

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


generate_jobs_poisson(100)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:20:34 2020

@author: eja26438
"""

#import nexus_iterator.KeyFollower as KeyFollower
#import nexus_iterator.DataSource as DataSource
from nexus_iterator.KeyFollower import Follower
from nexus_iterator.DataSource import DataFollower
from nexus_iterator.FrameGrabber import Grabber

import numpy as np
import dask
from dask.distributed import Client
from dask.threaded import get
import time
import h5py
from threading import Thread
from queue import Queue




         

#client = Client()
result_list = []




#thread 1: generate a queue of keys using Follower
#thread 2: access the keys and setup batch jobs 

#Iterate through the key generator
def array_sum(x):
    return x.sum(axis = 3)


def iterate_through_datasource(queue):
    with h5py.File("/home/eja26438/Documents/First_Year_Projects/Unique_Keys/Iterator_data/i18-81742.nxs", "r") as f:
        
        data = ['entry/Xspress3A/data']
        keys = ['entry/solstice_scan/keys']
        df = DataFollower(f, keys, data, timeout = 1)
        for data in range(10):
            queue.put(next(df))
        queue.put(None)
        
        
def iterate_through_keyfollower(queue):
    with h5py.File("/home/eja26438/Documents/First_Year_Projects/Unique_Keys/Iterator_data/i18-81742.nxs", "r") as f:
        keys = ["entry/solstice_scan/keys"]
        kf = Follower(f, keys, timeout = 10)
        for key in kf:
            queue.put(key)
        queue.put(None)





def read_client_list(queue):
    client = Client()
    while True:
        frame = queue.get()
        
        if frame:
            frame = frame[0]
            result_list.append(frame.sum(axis = 3))
            
        else:
            queue.task_done()
            break
    




def create_dask_job(number_of_frames, queue, fn):
    key_list = []
    for i in range(number_of_frames):
        key_list.append(queue.get())
        
    return_dict = {}
    for key in key_list:
        return_dict[str(key)] = key
        return_dict["function_"+str(key)] = (fn, str(key))
        
    return return_dict
    


inc = lambda x:x+1
add = lambda x,y: x+y


d = {"x": 1,
     "y": (inc, "x"),
     "z": (add, "y", 10)}


queue = Queue()
for i in range(20):
    queue.put(i)

dsk = {"load-1":(queue.get()),
       "load-2":(queue.get()),
       "load-3":(queue.get()),
       "load-4":(queue.get()),
       "load-5":(queue.get()),
       "evaluate-1": (lambda x:x**2, "load-1")}




def file_creator(write_file, dataset_list, shape = (40960,)):
    with h5py.File(write_file, "w", libver= "latest") as f:
        for ds in dataset_list:
            f.create_dataset(ds, chunks = (shape))
        
        
def write_frame_to_file(write_file, dataset):
    pass
    
        


f = h5py.File("/home/eja26438/Documents/First_Year_Projects/Unique_Keys/Iterator_data/i18-81742.nxs", "r")



grabber = Grabber(f, ['entry/Xspress3A/data', 'entry/Xspress3A/data'])










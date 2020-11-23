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

import numpy as np
import dask
from dask.distributed import Client
import time
import h5py
from threading import Thread
from queue import Queue



         

#client = Client()
result_list = []




#thread 1: generate a queue of keys using Follower
#thread 2: access the keys and setup batch jobs 

#Iterate through the key generator
def inc(x):
    return x.sum(axis = 3)


def iterate_through_datasource(queue):
    with h5py.File("/Users/richardparke/Documents/Diamond/Iterator_data/i18-81742.nxs", "r") as f:
        
        data = ['entry/Xspress3A/data']
        keys = ['entry/solstice_scan/keys']
        df = DataFollower(f, keys, data, timeout = 1)
        for data in range(20):
            queue.put(next(df))
        queue.put(None)
        
        
def iterate_through_keyfollower(queue):
    pass





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
    



queue = Queue(maxsize = 10)    
write_thread = Thread(target=(iterate_through_datasource), args = (queue,))
read_thread = Thread(target = (read_client_list), args = (queue,))
write_thread.start()
read_thread.start()
write_thread.join()
read_thread.join()







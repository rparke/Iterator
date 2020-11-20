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


data = ['entry/Xspress3A/data']
keys = ['entry/solstice_scan/keys']
         

client = Client()
client_list = []




#Iterate through the key generator
def inc(x):
    return x.sum(axis = 3)

with h5py.File("/home/eja26438/Documents/First_Year_Projects/Unique_Keys/Iterator_Data/Data/i18-81742.nxs", "r") as f:
    df = DataFollower(f, keys, data, timeout = 1)
    for data in df:
        client_list.append(client.submit(inc, data[0]))


result_list = []

for i in client_list:
    result_list.append(i.result())
    
    
    
#Demonstration


def inc(x):
    time.sleep(10)
    return x+1




start_time = time.time()
future_list = []
client = Client()
for i in range(10):
    future_list.append(client.submit(inc, i))
    
print(future_list)
    
result_list = []
for i in future_list:
    result_list.append(i.result())
futures_time = time.time() - start_time
    

start_time = time.time()
future_list = []
client = Client()
for i in range(10):
    future_list.append(inc(i))
non_future_time = time.time() - start_time



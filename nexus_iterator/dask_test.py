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
         

#client = Client()
client_list = []




#Iterate through the key generator
def inc(x):
    return x.sum(axis = 3)


def iterate_through_datasource(data, keys):
    with h5py.File("/Users/richardparke/Documents/Diamond/Iterator_data/i18-81742.nxs", "r") as f:
        
        
        df = DataFollower(f, keys, data, timeout = 1)
        for data in df:
            client_list.append(data)
            #client_list.append(client.submit(inc, data[0]))


    
    
thread = Thread(target=(iterate_through_datasource), args = (data, keys))
thread.start()
thread.join()







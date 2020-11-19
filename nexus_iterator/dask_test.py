#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:20:34 2020

@author: eja26438
"""

import nexus_iterator.KeyFollower as KeyFollower
import nexus_iterator.DataSource as DataSource
import numpy as np
import dask
from dask.distributed import Client
import time
import h5py


data = ['entry/Xspress3A/data']
keys = ['entry/solstice_scan/keys']
         
with h5py.File("/home/eja26438/Documents/First_Year_Projects/Unique_Keys/Iterator_Data/Data/i18-81742.nxs", "r") as f:
    
    kf = KeyFollower.Follower(f, keys, timeout = 1)
    
    for key in kf:
        print(key)



#Subclass numpy array
class DataSet(np.ndarray):pass
def create_dataset_from_numpy_array(numpy_array):
    ds = DataSet(numpy_array.shape)
    ds[:] = numpy_array[:]
    ds.refresh = lambda:None
    return ds



#Create a dataset of keys that is completely filled with non-zero values
#Number of iterations = 50
def complete_dataset():
    return create_dataset_from_numpy_array(np.arange(50).reshape(5,10,1,1)+1)

f = {"keys": {"complete": complete_dataset(), "also_complete": complete_dataset()}}

kf = KeyFollower.Follower(f, ["keys"], timeout = 2)





#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:45:13 2020

@author: eja26438
"""

import h5py
import numpy as np

class Grabber():
    
    def __init__(self, hdf5_file, data_paths = None, data = None):
        self.hdf5_file = hdf5_file
        self.data_paths = data_paths
        self.data = data
        
        
        
        
        
    def get_list(self, index):
        return_dict = {}
        for dataset in self.data_paths:
            ds = np.asarray(self.hdf5_file[dataset])
            frame_shape = tuple([1 for i in range(len(ds.shape)-2)] + [ds.shape[-2], ds.shape[-1]])
            shape = (ds.shape[-2], ds.shape[-1])
            size = ds.shape[-2] * ds.shape[-1]
            dimensions = len(ds.shape)
            ds = ds.flatten()
            return_array = ds[index*size: (index+1)*size]
            return_array = return_array.reshape(frame_shape)
            return_dict[str(dataset)] = return_array
        return return_dict
    
    def get(self, index):
        return_dict = {}
        ds = np.asarray(self.hdf5_file[self.data_paths])
        frame_shape = tuple([1 for i in range(len(ds.shape)-2)] + [ds.shape[-2], ds.shape[-1]])
        shape = (ds.shape[-2], ds.shape[-1])
        size = ds.shape[-2] * ds.shape[-1]
        dimensions = len(ds.shape)
        ds = ds.flatten()
        return_array = ds[index*size: (index+1)*size]
        return_array = return_array.reshape(frame_shape)
        return return_array
    
    


# =============================================================================
# frame_size = dataset.shape[-2] * dataset.shape[-1]
# frame_shape = [1 for i in range(len(dataset.shape)-2)] + [dataset.shape[-2], dataset.shape[-1]]
# =============================================================================

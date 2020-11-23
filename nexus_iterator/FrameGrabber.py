#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:45:13 2020

@author: eja26438
"""


class Grabber():
    
    def __init__(self, hdf5_file, data_paths):
        self.hdf5_file = hdf5_file
        self.data_paths = data_paths
        
        
        
        
        
    def get(self, index):
        return_dict = {}
        for dataset in self.data_paths:
            ds = self.hdf5_file[dataset][...]
            shape = (ds.shape[-2], ds.shape[-1])
            size = ds.shape[-2] * ds.shape[-1]
            dimensions = len(ds.shape)
            ds = ds.flatten()
            return_array = ds[index*size: (index+1)*size]
            print(return_array)
            return_dict[str(dataset)] = return_array
        return return_dict
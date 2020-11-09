#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 11:08:42 2020

@author: eja26438
"""


import numpy as np
from mock import mock, MagicMock


#Create subclass of np.ndarray
class DataSet(np.ndarray):
    pass


#Create a dataset np.ndarray subclass from an np.ndarray with refresh method
def create_dataset(arr):
    ds = DataSet(arr.shape)
    ds[:] = arr[:]
    
    def refresh_method():
        print("Refreshing")
    
    ds.refresh = refresh_method
    
    return ds




class Complete():
    
    def __init__(self):
        self.complete_dict = self.complete_dict()
    
    def __getitem__(self, key):
        return self.complete_dict[key]


    def complete_dict(self):
        complete_datasets = {"keys":self.complete_keys_dataset(), "data":self.complete_dataset()}
        return complete_datasets
    
    def complete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        complete_array = create_dataset(complete_array)
        
        
        
        complete_dict = {"dset_1": complete_array}
        
        #dataset_dict = {"data": complete_array}
        return complete_dict
    
    def complete_keys_dataset(self):
        #create complete datasets
        self.complete_array = np.arange(2814).reshape((42,67,1,1))
        self.complete_array = create_dataset(self.complete_array)
        
        self.complete_dict = {"key_1":self.complete_array}
        
        #dataset_dict = {"keys": complete_array}
        return self.complete_dict
    
    def refresh(self):
        return
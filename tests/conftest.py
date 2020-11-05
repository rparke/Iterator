#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 13:12:45 2020

@author: eja26438
"""


from mock import patch, Mock
import pytest
import numpy as np





#Function to mockup dataset creation
def complete_keys_dataset():
    #create complete datasets
    complete_array = np.arange(2814).reshape((42,67,1,1))
    
    dataset_dict = {"keys": complete_array}
    group_dict = {"complete":dataset_dict}
    return group_dict


#Function to mockup dataset creation
def complete_dataset():
    
    array_shape = (42,67,10,4096)
    
    #create complete datasets
    complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
    
    dataset_dict = {"data": complete_array}
    group_dict = {"complete":dataset_dict}
    return group_dict


def incomplete_keys_dataset():
    #create complete datasets
    complete_array = np.arange(2814)
    complete_array[2001:] = 0
    complete_array.reshape((42,67,1,1))
    dataset_dict = {"keys": complete_array}
    group_dict = {"incomplete":dataset_dict}
    return group_dict


def incomplete_dataset():
    complete_array = np.arange(42*67*10*4096)
    
    dataset_dict = {"data": complete_array}
    group_dict = {"incomplete":dataset_dict}
    return group_dict



class complete():
    
    def __init__(self):
        self.complete_dict = self.complete_dict()
    
    def __getitem__(self, key):
        return self.complete_dict[key]


    def complete_dict(self):
        complete_datasets = {"keys":self.complete_keys_dataset(), "data":self.complete_dataset()}
        complete_group = {"complete": complete_datasets}
        return complete_group
    
    def complete_dataset(self):
    
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        
        
        complete_dict = {"dset_1": complete_array}
        
        #dataset_dict = {"data": complete_array}
        return complete_dict
    
    def complete_keys_dataset(self):
        #create complete datasets
        complete_array = np.arange(2814).reshape((42,67,1,1))
        
        complete_dict = {"key_1":complete_array}
        
        #dataset_dict = {"keys": complete_array}
        return complete_dict
    
    
class incomplete():
    def __init__(self):
        self.incomplete_dict = self.incomplete_dict()
    
    def __getitem__(self, key):
        return self.incomplete_dict[key]


    def incomplete_dict(self):
        incomplete_datasets = {"keys":self.incomplete_keys_dataset(), "data":self.incomplete_dataset()}
        incomplete_group = {"complete": incomplete_datasets}
        return incomplete_group
    
    def incomplete_dataset(self):
    
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        incomplete_array = np.arange(np.asarray(array_shape).prod())
        incomplete_array[array_shape[-1]*array_shape[-2]*2000:] = 0
        
        incomplete_dict = {"dset_1": incomplete_array}
        
        #dataset_dict = {"data": complete_array}
        return incomplete_dict
    
    def complete_keys_dataset(self):
        #create complete datasets
        incomplete_array = np.arange(2814)
        incomplete_array = incomplete_array[2000:]
        incomplete_array.reshape((42,67,1,1))
        
        
        incomplete_dict = {"key_1":incomplete_array}
        
        #dataset_dict = {"keys": complete_array}
        return incomplete_dict

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 11:08:42 2020

@author: eja26438
"""


import numpy as np
from mock import mock, MagicMock



class DataSet(np.ndarray):
    pass



class Complete():
    
    def __init__(self):
        self.complete_dict = self.complete_dict()
        self.count = -1
    
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
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.complete_dataset = DataSet(complete_array.shape)
        self.complete_dataset[:] = complete_array[:]
        self.complete_dataset.refresh = self.refresh
        
        
        
        complete_dict = {"dset_1": self.complete_dataset}
        
        #dataset_dict = {"data": complete_array}
        return complete_dict
    
    def complete_keys_dataset(self):
        #create complete datasets
        complete_array = np.arange(2814).reshape((42,67,1,1))
        
        self.complete_key_dataset = DataSet(complete_array.shape)
        self.complete_key_dataset[:] = complete_array[:]
        self.complete_key_dataset.refresh = self.refresh
        

        complete_dict = {"key_1":self.complete_key_dataset}
        
        return complete_dict
    
    def refresh(self):
        print("Refreshing")
        return
    
    
class Incomplete():
    
    def __init__(self):
        self.complete_dict = self.complete_dict()
        self.count = -1
    
    def __getitem__(self, key):
        return self.complete_dict[key]


    def complete_dict(self):
        complete_datasets = {"keys":self._key_dict(), "data":self._dataset_dict()}
        return complete_datasets
    
    def _dataset_dict(self):
        return {"dset_1":self._incomplete_dataset()}
    
    def _key_dict(self):
        return {"key_1": self._incomplete_keys_dataset()}
    
    def _complete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.complete_dataset = DataSet(complete_array.shape)
        self.complete_dataset[:] = complete_array[:]
        self.complete_dataset.refresh = self.refresh
        
        return self.complete_dataset
    
    def _incomplete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.incomplete_dataset = DataSet(complete_array.shape)
        self.incomplete_dataset[:] = complete_array[:]
        self.incomplete_dataset.refresh = self.refresh
        
        return self.incomplete_dataset
    
    def _complete_keys_dataset(self):
        #create complete datasets
        complete_array = np.arange(2814).reshape((42,67,1,1))
        
        self.complete_key_dataset = DataSet(complete_array.shape)
        self.complete_key_dataset[:] = complete_array[:]
        self.complete_key_dataset.refresh = self.refresh
        
        return self.complete_key_dataset
    
    def _incomplete_keys_dataset(self):
        #Create set of sequential keys 2000 long
        complete_array = np.arange(2814).reshape((42,67,1,1))+1
        complete_array = complete_array.flatten()
        complete_array[2000:] = 0
        complete_array = complete_array.reshape((42,67,1,1))
        
        self.incomplete_key_dataset = DataSet(complete_array.shape)
        self.incomplete_key_dataset[:] = complete_array[:]
        self.incomplete_key_dataset.refresh = self.refresh
        

        return self.incomplete_key_dataset
    
    def refresh(self):
        print("Refreshing")       
        return
    

class MultipleIncomplete():
    
    def __init__(self):
        self.complete_dict = self.complete_dict()
        self.count = -1
    
    def __getitem__(self, key):
        return self.complete_dict[key]


    def complete_dict(self):
        complete_datasets = {"keys":self._key_dict(), "data":self._dataset_dict()}
        return complete_datasets
    
    def _dataset_dict(self):
        return {"dset_1":self._complete_dataset(), "dset_2":self._incomplete_dataset()}
    
    def _key_dict(self):
        return {"key_1":self._complete_keys_dataset(), "key_2": self._incomplete_keys_dataset()}
    
    def _complete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.complete_dataset = DataSet(complete_array.shape)
        self.complete_dataset[:] = complete_array[:]
        self.complete_dataset.refresh = self.refresh
        
        return self.complete_dataset
    
    def _incomplete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.incomplete_dataset = DataSet(complete_array.shape)
        self.incomplete_dataset[:] = complete_array[:]
        self.incomplete_dataset.refresh = self.refresh
        
        return self.incomplete_dataset
    
    def _complete_keys_dataset(self):
        #create complete datasets
        complete_array = np.arange(2814).reshape((42,67,1,1))
        
        self.complete_key_dataset = DataSet(complete_array.shape)
        self.complete_key_dataset[:] = complete_array[:]
        self.complete_key_dataset.refresh = self.refresh
        
        return self.complete_key_dataset
    
    def _incomplete_keys_dataset(self):
        #Create set of sequential keys 2000 long
        complete_array = np.arange(2814).reshape((42,67,1,1))+1
        complete_array = complete_array.flatten()
        complete_array[2000:] = 0
        complete_array = complete_array.reshape((42,67,1,1))
        
        self.incomplete_key_dataset = DataSet(complete_array.shape)
        self.incomplete_key_dataset[:] = complete_array[:]
        self.incomplete_key_dataset.refresh = self.refresh
        

        return self.incomplete_key_dataset
    
    def refresh(self):
        print("Refreshing")       
        return
    
    
class IncompleteUpdating():
    
    def __init__(self, update_count = 10, start_array_size = 2000, final_array_size = 2500):
        self.complete_dict = self.complete_dict()
        self.count = -1
        self.update_count = update_count
    
    def __getitem__(self, key):
        return self.complete_dict[key]


    def complete_dict(self):
        complete_datasets = {"keys":self._key_dict(), "data":self._dataset_dict()}
        return complete_datasets
    
    def _dataset_dict(self):
        return {"dset_1":self._incomplete_dataset()}
    
    def _key_dict(self):
        return {"key_1": self._incomplete_keys_dataset()}
    

    def _incomplete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.incomplete_dataset = DataSet(complete_array.shape)
        self.incomplete_dataset[:] = complete_array[:]
        self.incomplete_dataset.refresh = self.refresh
        
        return self.incomplete_dataset
    

    
    def _incomplete_keys_dataset(self):
        #Create set of sequential keys 2000 long
        
        complete_array = self._complete_keys_dataset()
        shape = complete_array.shape
        
        incomplete_array = complete_array.copy()
        incomplete_array = incomplete_array.flatten()
        incomplete_array[2000:] = 0
        incomplete_array = incomplete_array.reshape(shape)
        
        self.incomplete_key_dataset = incomplete_array
        self.incomplete_key_dataset.refresh = self.refresh
        return self.incomplete_key_dataset
        
        
    
    def _complete_keys_dataset(self):
        
        complete_array = DataSet((42,67,1,1))
        complete_array[:] = (np.arange(2814).reshape((42,67,1,1))+1)[:]
        
        return complete_array
    
    def refresh(self):
        self.count+=1
        if self.count == self.update_count:
            print("Updating the dataset")
            

            
            
            self.incomplete_key_dataset[:] = self._complete_keys_dataset()
            print (self.incomplete_key_dataset.max())
            
        
        else:
            print("Doing Nothing")
            print (self.incomplete_key_dataset.max())
            
        return
    

    

class IncompleteRowByRow():
    
    def __init__(self, update_count = 10):
        self.complete_dict = self.complete_dict()
        self.count = -1
        self.update_count = update_count
    
    def __getitem__(self, key):
        return self.complete_dict[key]


    def complete_dict(self):
        complete_datasets = {"keys":self._key_dict(), "data":self._dataset_dict()}
        return complete_datasets
    
    def _dataset_dict(self):
        return {"dset_1":self._incomplete_dataset()}
    
    def _key_dict(self):
        return {"key_1": self._incomplete_keys_dataset()}
    

    def _incomplete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.incomplete_dataset = DataSet(complete_array.shape)
        self.incomplete_dataset[:] = complete_array[:]
        self.incomplete_dataset.refresh = self.refresh
        
        return self.incomplete_dataset
    

    
    def _incomplete_keys_dataset(self):
        #Create set of sequential keys 2000 long
        
        #Create Arays
        complete_array = np.arange(2814).reshape((42,67,1,1))+1
        self.final_array = complete_array.copy()
        
        #Incompletely filled row on row by row scan
        complete_array[-1][4:] = [[0]]
        
        self.incomplete_key_dataset = DataSet(complete_array.shape)
        self.incomplete_key_dataset[:] = complete_array[:]
        self.incomplete_key_dataset.refresh = self.refresh
        

        return self.incomplete_key_dataset
    
    def refresh(self):
        print("Refreshing")
        return


class IncompleteSnakeScan():
    
    def __init__(self, update_count = 10):
        self.complete_dict = self.complete_dict()
        self.count = -1
        self.update_count = update_count
    
    def __getitem__(self, key):
        return self.complete_dict[key]


    def complete_dict(self):
        complete_datasets = {"keys":self._key_dict(), "data":self._dataset_dict()}
        return complete_datasets
    
    def _dataset_dict(self):
        return {"dset_1":self._incomplete_dataset()}
    
    def _key_dict(self):
        return {"key_1": self._incomplete_keys_dataset()}
    

    def _incomplete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.incomplete_dataset = DataSet(complete_array.shape)
        self.incomplete_dataset[:] = complete_array[:]
        self.incomplete_dataset.refresh = self.refresh
        
        return self.incomplete_dataset
    

    
    def _incomplete_keys_dataset(self):
        #Create set of sequential keys 2000 long
        
        #Create Arays
        complete_array = np.arange(2814).reshape((42,67,1,1))+1
        self.final_array = complete_array.copy()
        
        #Edit the array so the final line is following the pattern of a snake scan
        complete_array[-1][:-3] = [[0]]
        
        self.incomplete_key_dataset = DataSet(complete_array.shape)
        self.incomplete_key_dataset[:] = complete_array[:]
        self.incomplete_key_dataset.refresh = self.refresh
        

        return self.incomplete_key_dataset
    
    def refresh(self):
        print("Refreshing")
        return

    


#Finish This
class UpdatingSnakeScan():
    
    def __init__(self, update_count = 10):
        self.complete_dict = self.complete_dict()
        self.count = -1
        self.update_count = update_count
    
    def __getitem__(self, key):
        return self.complete_dict[key]


    def complete_dict(self):
        complete_datasets = {"keys":self._key_dict(), "data":self._dataset_dict()}
        return complete_datasets
    
    def _dataset_dict(self):
        return {"dset_1":self._incomplete_dataset()}
    
    def _key_dict(self):
        return {"key_1": self._incomplete_keys_dataset()}
    

    def _incomplete_dataset(self):
    
        #change to smaller array
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
        
        #Subclass the np.ndarray so that the Complete.refresh method can be called
        self.incomplete_dataset = DataSet(complete_array.shape)
        self.incomplete_dataset[:] = complete_array[:]
        self.incomplete_dataset.refresh = self.refresh
        
        return self.incomplete_dataset
    

    
    def _incomplete_keys_dataset(self):
        #Create set of sequential keys 2000 long
        
        #Create Arays
        complete_array = np.arange(2814).reshape((42,67,1,1))+1
        self.final_array = complete_array.copy()
        
        #Edit the array so the final line is following the pattern of a snake scan
        complete_array[-1][:-3] = [[0]]
        
        self.incomplete_key_dataset = DataSet(complete_array.shape)
        self.incomplete_key_dataset[:] = complete_array[:]
        self.incomplete_key_dataset.refresh = self.refresh
        

        return self.incomplete_key_dataset
    
    def refresh(self):
        self.count+=1
        if self.count == self.update_count:
            print("Updating the dataset")
            
            self.incomplete_key_dataset[:] = self.final_array[:]
            

            
        
        else:
            print("Doing Nothing")

            
        return




    

import numpy as np
import h5py
import os
from nexus_iterator import KeyFollower
import time



class DataFollower():
    
    def __init__(self, hdf5_file, keypaths, dataset_paths, timeout = 1):
        self.hdf5_file = hdf5_file
        self.dataset_paths = dataset_paths
        self.kf = KeyFollower.Follower(hdf5_file, keypaths, timeout)
        
            
        
    def __iter__(self):
        return(self)
    
    
    def __next__(self):
        
            

        if self.kf.is_finished():
            raise StopIteration
        
        else:
            
            current_dataset_index = next(self.kf)
            current_dataset_slice = self._get_dataset_flattened(current_dataset_index)
    
            
            return current_dataset_slice
        
        
    def reset(self):
        self.kf.reset()
        
        
    def _get_dataset_flattened(self, current_dataset_index):
        return_list = []
        for dataset_path in self.dataset_paths:
            dataset = self.hdf5_file[dataset_path]
            dataset.refresh()
            dataset = dataset[...]
            dataset_shape = self._get_slice_shape(dataset)
            restore_shape = self._restore_dataset_shape(dataset)
            return_list.append(  (dataset.flatten()[current_dataset_index*dataset_shape: (current_dataset_index + 1)*dataset_shape]).reshape(restore_shape)  )
        return return_list
    
        
        
    def _get_slice_shape(self, dataset):
            return (dataset.shape[-1]*dataset.shape[-2])
                
                
    def _restore_dataset_shape(self, dataset):
        for dataset_path in self.dataset_paths:
            
            full_shape = list(dataset.shape)
            length = len(full_shape)
            for i in range(length -2):
                full_shape[i] = 1
            return full_shape
            
            
    
    def _get_dataset_flattened_group(self, current_dataset_index):
        return_list = []
        slice_shape_generator = self._get_slice_shape()
        restore_shape = self._restore_dataset_shape()
        for group in self.dataset_paths:
            for dataset in self.hdf5_file[group].values():
                dataset_shape = next(slice_shape_generator)
                return_list.append(  (dataset.flatten()[current_dataset_index*dataset_shape: (current_dataset_index + 1)*dataset_shape]).reshape(next(restore_shape))  )
        return return_list
    
        
        
    def _get_slice_shape_group(self):
        for group in self.dataset_paths:
            for dataset in self.hdf5_file[group].values():
                yield (dataset.shape[-1]*dataset.shape[-2])
                
                
    def _restore_dataset_shape_group(self):
        for group in self.dataset_paths:
            for dataset in self.hdf5_file[group].values():
                full_shape = list(dataset.shape)
                length = len(full_shape)
                for i in range(length -2):
                    full_shape[i] = 1
                yield full_shape
                
                
        
            
            



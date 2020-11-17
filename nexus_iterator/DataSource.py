import numpy as np
import h5py
import os
from nexus_iterator import KeyFollower
import time



class DataFollower():
    
    def __init__(self, hdf5_file, keypaths, dataset_paths, timeout = 1):
        self.hdf5_file = hdf5_file
        self.keypaths = keypaths
        self.timeout = timeout
        self.dataset_paths = dataset_paths
        

        
        self.kf = KeyFollower.Follower(self.hdf5_file, self.keypaths, self.timeout)
        
            
        
    def __iter__(self):
        return(self)
    
    
    def __next__(self):
        
        #Fix for now to ensure we have correctly initialised the dataframe shape
        #self._get_frame_shape()
            

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
        slice_shape_generator = self._get_slice_shape()
        for group in self.dataset_paths:
            for dataset in self.hdf5_file[group].values():
                dataset_shape = next(slice_shape_generator)
                return_list.append(dataset.flatten()[current_dataset_index*dataset_shape: (current_dataset_index + 1)*dataset_shape])
        return return_list
        
        
    def _get_slice_shape(self):
        for group in self.dataset_paths:
            for dataset in self.hdf5_file[group].values():
                yield (dataset.shape[-1]*dataset.shape[-2])
                
                
    def _restore_dataset_shape(self):
        pass
        
            
            






# =============================================================================
# from unittest.mock import MagicMock
# 
# #Creating datasets from numpy arrays
# class DataSet(np.ndarray):pass
# 
# def create_dataset_from_numpy_array(numpy_array):
#     ds = DataSet(numpy_array.shape)
#     ds[:] = numpy_array[:]
#     ds.refresh = lambda:None
#     return ds
# 
# #Create a dataset of keys that is completely filled with non-zero values
# #Number of iterations = 50
# complete_dataset = create_dataset_from_numpy_array(np.arange(50).reshape(5,10,1,1)+1)
# 
# 
# key_paths = ["keys"]
# h5py.File = MagicMock()
# h5py.File.return_value = {'keys':{"complete":complete_dataset}}
# f = h5py.File("filepath")
# df = DataFollower(f, key_paths, timeout = 0.1)
# =============================================================================

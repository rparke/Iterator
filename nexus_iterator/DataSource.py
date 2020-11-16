import numpy as np
import h5py
import os
from nexus_iterator import KeyFollower
import time



class DataFollower(KeyFollower.Follower):
    
    def __init__(self,
                 hdf5_file,
                 key_datasets,
                 data_datasets,
                 timeout = 10,
                 sleep_time = 1):
        super().__init__(hdf5_file, key_datasets, timeout)
        self.data_datasets = data_datasets
        self.dataset_indices = np.asarray([0 for i in data_datasets])
        self.sleep_time = sleep_time
        
             
    def __iter__(self):
        self._get_frame_size()
        return(self)
    
    
    def __next__(self):
        
        #Fix for now to ensure we have correctly initialised the dataframe shape
        #self._get_frame_shape()
            
        
        if not self.is_finished():
            
            while not self._is_next():
                time.sleep(self.sleep_time)
                if self.is_finished():
                    raise StopIteration
            
            if self._is_next():
                x = self._get_dataset_slices_flattened()
                #x = self._restore_frame_shape(x)
                
                #Restore frame shape
                for i in range(len(x)):
                    x[i] = x[i].reshape(self.frame_shape[i])
                    
                self._update_dataset_start_index()
                self.current_key += 1
                self._timer_reset()
                return x
        
        else:
            raise StopIteration
            
    def reset(self):
        self.current_key = -1
        self.current_max = -1
        self.dataset_indices = np.asarray([0 for i in self.data_datasets])
            
      
    #Creates a list of frame shapes       
    def _get_frame_size(self):
        frame_size = []
        for datapath in self.data_datasets:
            for dataset in self.hdf5_file[datapath].values():
                frame_size.append((dataset.shape)[-2] * (dataset.shape)[-1])
        self.frame_size = np.asarray(frame_size)
        
        self._get_frame_shape()
        
    def _get_frame_shape(self):
        frame_shape = []
        for dataset in self.data_datasets:
            frame_shape.append( [1 for i in range(len(self.hdf5_file[dataset].shape)-2)]+\
                               [(self.hdf5_file[dataset].shape)[-2]] +\
                                   [(self.hdf5_file[dataset].shape)[-1]])
        self.frame_shape = frame_shape
            
    
    
    #Moves flattened dataset to correct index for all datasets
    def _update_dataset_start_index(self):
        self.dataset_indices = self.dataset_indices + self.frame_size
        
        
    def _get_dataset_slices_flattened(self):
        return_list = []
        for i in range(len(self.data_datasets)):
            ds = self.hdf5_file[self.data_datasets[i]]
            return_list.append(ds[...].flatten()[self.dataset_indices[i]:self.dataset_indices[i] + self.frame_size[i]])
        return(return_list)
    
    def _restore_frame_shape(self, x):
        for i in range(len(x)):
            x[i] = x[i].reshape(self.frame_shape[i])
            return x
    

    
 
#Documentations
DataFollower.__doc__ = "Nexus/HDF5 iterator object" 
    

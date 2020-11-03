
import numpy as np
import h5py
import pytest
import os
from nexus_iterator import DataSource
from nexus_iterator import KeyFollower




#Check correct number of iterations are completed
def test_iterates_complete_dataset():
          
      filepath = "hdf5_tests/complete_2.h5"
      key_paths = ["keys/2"]
      data_paths = ['data/2']
      with h5py.File(filepath, "r") as f:
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           current_key = 0
           for dset in df:
               current_key+= 1
      assert current_key == 10

    
    
def test_iterates_incomplete_dataset():
          
      filepath = "hdf5_tests/incomplete_2.h5"
      key_paths = ["keys/incomplete"]
      data_paths = ["data/incomplete"]
      with h5py.File(filepath, "r") as f:
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           current_key = 0
           for dset in df:
               current_key+= 1
      assert current_key == 2

      
def test_iterates_multiple_incomplete_dataset():
          
      filepath = "hdf5_tests/incomplete_2.h5"
      key_paths = ["keys/complete", "keys/incomplete"]
      data_paths = ['data/full', "data/incomplete"]
      with h5py.File(filepath, "r") as f:
          #data = f[key_paths[0]][...]

           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
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
        for dataset in self.data_datasets:
            frame_size.append((self.hdf5_file[dataset].shape)[-2] * (self.hdf5_file[dataset].shape)[-1])
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
             #kf._get_frame_shape()
           current_key = 0
           for dset in df:
               current_key+= 1
      assert current_key == 2
      

#Check that the correct dataset is returned ignoring shapes
def test_correct_return_data_complete():
      filepath = "hdf5_tests/complete_2.h5"
      key_paths = ["keys/2"]
      data_paths = ['data/2']
      with h5py.File(filepath, "r") as f:
           
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           full_dataset = np.array([])
           for dset in df:
               full_dataset = np.concatenate((full_dataset, dset[0].flatten()))
           assert((f[data_paths[0]][...].flatten() == full_dataset).all())
           
           
def test_correct_return_single_data_incomplete():
      filepath = "hdf5_tests/incomplete_2.h5"
      key_paths = ["keys/incomplete"]
      data_paths = ["data/incomplete"]
      with h5py.File(filepath, "r") as f:
           
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           full_dataset = np.array([])
           for dset in df:
               full_dataset = np.concatenate((full_dataset, dset[0].flatten()))
        
           assert((f[data_paths[0]][...].flatten()[:len(full_dataset)] == full_dataset).all())
           #return [[full_dataset], [f[data_paths[0]][...].flatten()]]
        


def test_correct_return_multiple_data_incomplete():
      filepath = "hdf5_tests/incomplete_2.h5"
      key_paths = ["keys/complete", "keys/incomplete"]
      data_paths = ['data/full', "data/incomplete"]
      with h5py.File(filepath, "r") as f:
           
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           full_dataset = np.array([])
           for dset in df:
               full_dataset = np.concatenate((full_dataset, dset[0].flatten()))
        
           assert((f[data_paths[0]][...].flatten()[:len(full_dataset)] == full_dataset).all())
           

#Test correct shapes are returned


def test_correct_return_shape():
    filepath = "hdf5_tests/shape_test.h5"
    key_paths = ["keys/3d", "keys/4d"]
    data_paths = ["data/3d", "data/4d"]
    with h5py.File(filepath, "r") as f:
        df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
        for dset in df:
            assert dset[0].shape == (1,10,4096) and dset[1].shape == (1,1,10,4096)
            
def test_reset_method_iterates_correct_length():
    filepath = "hdf5_tests/complete_2.h5"
    key_paths = ["keys/2"]
    data_paths = ['data/2']
    with h5py.File(filepath, "r") as f:
         df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
         current_key = 0
         for dset in df:
             current_key+= 1
         df.reset()
         for dset in df:
             current_key+= 1
    assert current_key == 20
    

def test_reset_method_correct_return():
      filepath = "hdf5_tests/complete_2.h5"
      key_paths = ["keys/2"]
      data_paths = ['data/2']
      with h5py.File(filepath, "r") as f:
           
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           full_dataset = np.array([])
           for dset in df:
               full_dataset = np.concatenate((full_dataset, dset[0].flatten()))
           df.reset()
           for dset in df:
               full_dataset = np.concatenate((full_dataset, dset[0].flatten()))
           
           full_dataset_test = (f[data_paths[0]][...].flatten())
           full_dataset_test = np.concatenate([full_dataset_test, full_dataset_test])
           
           assert( ( full_dataset_test == full_dataset).all())


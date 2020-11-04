
import numpy as np
import h5py
import pytest
import os
from nexus_iterator import DataSource
from nexus_iterator import KeyFollower




#Check correct number of iterations are completed
def test_iterates_complete_dataset():
          
      filepath = "hdf5_tests/complete_2.h5"
      key_paths = ["keys"]
      data_paths = ['data/2']
      with h5py.File(filepath, "r") as f:
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           current_key = 0
           for dset in df:
               current_key+= 1
      assert current_key == 10

    
    
def test_iterates_incomplete_dataset():
          
      filepath = "hdf5_tests/incomplete_2.h5"
      key_paths = ["keys"]
      data_paths = ["data/incomplete"]
      with h5py.File(filepath, "r") as f:
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           current_key = 0
           for dset in df:
               current_key+= 1
      assert current_key == 2

      
def test_iterates_multiple_incomplete_dataset():
          
      filepath = "hdf5_tests/incomplete_2.h5"
      key_paths = ["keys"]
      data_paths = ['data/full', "data/incomplete"]
      with h5py.File(filepath, "r") as f:
          #data = f[key_paths[0]][...]

           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           current_key = 0
           for dset in df:
               current_key+= 1
      assert current_key == 2
      

#Check that the correct dataset is returned ignoring shapes
def test_correct_return_data_complete():
      filepath = "hdf5_tests/complete_2.h5"
      key_paths = ["keys"]
      data_paths = ['data/2']
      with h5py.File(filepath, "r") as f:
           
           df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
           full_dataset = np.array([])
           for dset in df:
               full_dataset = np.concatenate((full_dataset, dset[0].flatten()))
           assert((f[data_paths[0]][...].flatten() == full_dataset).all())
           
           
def test_correct_return_single_data_incomplete():
      filepath = "hdf5_tests/incomplete_2.h5"
      key_paths = ["keys"]
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
      key_paths = ["keys"]
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
    key_paths = ["keys"]
    data_paths = ["data/3d", "data/4d"]
    with h5py.File(filepath, "r") as f:
        df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
        for dset in df:
            assert dset[0].shape == (1,10,4096) and dset[1].shape == (1,1,10,4096)
            
def test_reset_method_iterates_correct_length():
    filepath = "hdf5_tests/complete_2.h5"
    key_paths = ["keys"]
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
      key_paths = ["keys"]
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


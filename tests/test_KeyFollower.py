import numpy as np
import h5py
import pytest
import os
from nexus_iterator import KeyFollower
from unittest.mock import Mock, patch, MagicMock



#Creating datasets from numpy arrays
class DataSet(np.ndarray):pass

def create_dataset_from_numpy_array(numpy_array):
    ds = DataSet(numpy_array.shape)
    ds[:] = numpy_array[:]
    ds.refresh = lambda:None
    return ds

#Create a dataset of keys that is completely filled with non-zero values
#Number of iterations = 50
complete_dataset = create_dataset_from_numpy_array(np.arange(50).reshape(5,10,1,1)+1)

#Create a dataset of keys that is half filled with non-zero values
#Number of iterations = 25
incomplete_array = np.arange(50)+1
incomplete_array[25:] = 0
incomplete_array = incomplete_array.reshape(5,10,1,1)
incomplete_dataset = create_dataset_from_numpy_array(incomplete_array)


#Create a dataset of keys that is partially filled, writing row by row
#Number of iterations = 26
incomplete_row_by_row_array = np.arange(50)+1
incomplete_row_by_row_array[26:] = 0
incomplete_row_by_row_array = incomplete_row_by_row_array.reshape(5,10,1,1)
incomplete_row_by_row_dataset = create_dataset_from_numpy_array(incomplete_row_by_row_array)

#Create a dataset of keys that is partially filled, writing with a snake scan
#Number of iterations = 20

incomplete_snake_scan_array = np.arange(50)+1
incomplete_snake_scan_array = incomplete_snake_scan_array.reshape(5,10,1,1)
incomplete_snake_scan_array[3:] = 0
incomplete_snake_scan_array[2][:-3] = 0
incomplete_snake_scan_dataset = create_dataset_from_numpy_array(incomplete_snake_scan_array)

#Create a small incomplete dataset that will be updated to the full size
small_incomplete_array = np.arange(25)+1
small_incomplete_array = small_incomplete_array.reshape(5,5,1,1)
small_incomplete_dataset = create_dataset_from_numpy_array(small_incomplete_array)



      
def test_iterates_complete_dataset():
          

    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {'keys':{"complete":complete_dataset}}
    f = h5py.File("filepath")
    kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for key in kf:
        current_key+= 1
          
    assert current_key == 50
                        
        
def test_iterates_incomplete_dataset():
    
    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"incomplete": incomplete_dataset}}
    f = h5py.File("filepath")
    kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for key in kf:
        current_key+=1
    assert current_key == 25
    
    

def test_iterates_multiple_incomplete_dataset():
    
    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"complete": complete_dataset, "incomplete": incomplete_dataset}}
    f = h5py.File("filepath")
    kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for key in kf:
        current_key+=1
    assert current_key == 25
    


def test_iterates_row_by_row():
     key_paths = ['keys']
     h5py.File = MagicMock()
     h5py.File.return_value = {"keys":{"incomplete_row_by_row": incomplete_row_by_row_dataset}}
     
     f = h5py.File("filepath")
     
     kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
     current_key = 0
     for key in kf:
         current_key+=1
     assert current_key == 26

def test_iterates_snake_scan():
     key_paths = ['keys']
     h5py.File = MagicMock()
     h5py.File.return_value = {"keys":{"incomplete_snake_scan": incomplete_snake_scan_dataset}}
     
     f = h5py.File("filepath")
     
     kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
     current_key = 0
     for key in kf:
         current_key+=1
     assert current_key == 20



def test_reads_updates():
    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"incomplete": incomplete_dataset}}
    f = h5py.File("filepath")
    kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for i in range(5):
        next(kf)
        current_key+=1
    kf.hdf5_file = {"keys":{"updating":complete_dataset}}
    
    for key in kf:
        current_key += 1
        
    assert current_key == 50
    
def test_update_changes_shape():
    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"small_incomplete":small_incomplete_dataset}}
    f = h5py.File("filepath")
    kf =KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for i in range(5):
        next(kf)
        current_key+=1
    kf.hdf5_file = {"keys":{"small_incomplete":complete_dataset}}
    for key in kf:
        current_key+=1
    assert current_key == 50
    
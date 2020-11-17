import numpy as np
import h5py
import pytest
from nexus_iterator import KeyFollower
from unittest.mock import Mock, patch, MagicMock
import KeyFollowerDatasets as Dataset






      
def test_iterates_complete_dataset():
          

    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {'keys':{"complete":Dataset.complete_dataset()}}
    f = h5py.File("filepath")
    kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for key in kf:
        current_key+= 1
          
    assert current_key == 50
                        
        
def test_iterates_incomplete_dataset():
    
    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"incomplete": Dataset.incomplete_dataset()}}
    f = h5py.File("filepath")
    kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for key in kf:
        current_key+=1
    assert current_key == 25
    
    

def test_iterates_multiple_incomplete_dataset():
    
    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"complete": Dataset.complete_dataset(), 
                                      "incomplete": Dataset.incomplete_dataset()}}
    f = h5py.File("filepath")
    kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for key in kf:
        current_key+=1
    assert current_key == 25
    


def test_iterates_row_by_row():
     key_paths = ['keys']
     h5py.File = MagicMock()
     h5py.File.return_value = {"keys":{"incomplete_row_by_row": Dataset.incomplete_row_by_row_dataset()}}
     
     f = h5py.File("filepath")
     
     kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
     current_key = 0
     for key in kf:
         current_key+=1
     assert current_key == 26

def test_iterates_snake_scan():
     key_paths = ['keys']
     h5py.File = MagicMock()
     h5py.File.return_value = {"keys":{"incomplete_snake_scan": Dataset.incomplete_snake_scan_dataset()}}
     
     f = h5py.File("filepath")
     
     kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
     current_key = 0
     for key in kf:
         current_key+=1
     assert current_key == 20


def test_reads_updates():
    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"incomplete": Dataset.incomplete_dataset()}}
    f = h5py.File("filepath")
    kf = KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for i in range(5):
        next(kf)
        current_key+=1
    kf.hdf5_file = {"keys":{"updating":Dataset.complete_dataset()}}
    
    for key in kf:
        current_key += 1
        
    assert current_key == 50
    
def test_update_changes_shape():
    key_paths = ["keys"]
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"small_incomplete": Dataset.small_incomplete_dataset()}}
    f = h5py.File("filepath")
    kf =KeyFollower.Follower(f, key_paths, timeout = 0.1)
    current_key = 0
    for i in range(5):
        next(kf)
        current_key+=1
    kf.hdf5_file = {"keys":{"small_incomplete":Dataset.complete_dataset()}}
    for key in kf:
        current_key+=1
    assert current_key == 50
    
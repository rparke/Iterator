import numpy as np
import h5py
import pytest
import os
from nexus_iterator import KeyFollower
from unittest.mock import Mock, patch, MagicMock
import mocks





      
def test_iterates_complete_dataset():
          

      key_paths = ["keys"]
      
      f = mocks.Complete()

      kf = KeyFollower.Follower(f, key_paths, timeout = 1)
      current_key = 0
      for key in kf:
          current_key+= 1
            
      assert current_key == 2814
                        
        
def test_iterates_incomplete_dataset():
    
    #key_paths = ["incomplete_2814"]
    key_paths = ["keys"]
    f = mocks.Incomplete()
    kf = KeyFollower.Follower(f, key_paths, timeout = 1)
    current_key = 0
    for key in kf:
        current_key+= 1
    assert current_key == 2000
    
    

def test_iterates_multiple_incomplete_dataset():
    
    #key_paths = ["data/1000", 'data/2000']
    key_paths = ["keys"]
    f = mocks.MultipleIncomplete()
    kf = KeyFollower.Follower(f, key_paths, timeout = 1)
    current_key = 0
    for key in kf:
        current_key+=1
    assert current_key == 2000
    

def test_iterates_row_by_row():
    key_paths = ['keys']
    f = mocks.IncompleteRowByRow()
    kf = KeyFollower.Follower(f, key_paths, timeout = 1)
    current_key = 0
    for key in kf:
        current_key+=1
    assert current_key == 2751

def test_iterates_snake_scan():
    key_paths = ['keys']
    f = mocks.IncompleteSnakeScan()
    kf = KeyFollower.Follower(f, key_paths, timeout = 1)
    current_key = 0
    for key in kf:
        current_key+=1
    assert current_key == 2747
    
    
    
    
#Ensure that file is refreshed between calls of the iterator
def test_file_refreshed_between_iterations():
    
    
    
    pass


def test_updates_correctly():
    
    
    
    #Test array at the beginning of iteration, iterate through n steps to hit update step
    #Test that array has correctly updated and iterates to the correct point
    
    pass





    


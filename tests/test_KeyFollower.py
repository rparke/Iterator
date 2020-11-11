import numpy as np
import h5py
import pytest
import os
from nexus_iterator import KeyFollower
from unittest.mock import Mock, patch, MagicMock
import mocks





# =============================================================================
# def test_iterates_complete_dataset():
#           
#       filepath = "hdf5_tests/complete_1.h5"
#       ##key_paths = ["keys/complete"]
#       key_paths = ["keys"]
#       with h5py.File(filepath, "r") as f:
#           #data = f[key_paths[0]][...]
# 
#            kf = KeyFollower.Follower(f, key_paths, timeout = 1)
#            current_key = 0
#            for key in kf:
#                current_key+= 1
#             
#       assert current_key == 2814
# =============================================================================
      
      
def test_iterates_complete_dataset():
          
      filepath = "hdf5_tests/complete_1.h5"
      ##key_paths = ["keys/complete"]
      key_paths = ["keys"]
      
      f = Complete()

      kf = KeyFollower.Follower(f, key_paths, timeout = 1)
      current_key = 0
      for key in kf:
          current_key+= 1
            
      assert current_key == 2814
            
            
    
  
    
    
# =============================================================================
# def test_iterates_incomplete_dataset():
#     
#     filepath = "hdf5_tests/incomplete_1.h5"
#     #key_paths = ["incomplete_2814"]
#     key_paths = ["/"]
#     with h5py.File(filepath, "r") as f:
#         kf = KeyFollower.Follower(f, key_paths, timeout = 1)
#         current_key = 0
#         for key in kf:
#             current_key+= 1
#         assert current_key == 2001
# =============================================================================
        
def test_iterates_incomplete_dataset():
    
    #key_paths = ["incomplete_2814"]
    key_paths = ["keys"]
    f = Incomplete()
    kf = KeyFollower.Follower(f, key_paths, timeout = 1)
    current_key = 0
    for key in kf:
        current_key+= 1
    assert current_key == 2000
    
    

# =============================================================================
# def test_iterates_multiple_incomplete_dataset():
#     
#     filepath = "hdf5_tests/multiple_incomplete_1.h5"
#     #key_paths = ["data/1000", 'data/2000']
#     key_paths = ["data"]
#     with h5py.File(filepath, "r") as f:
#         kf = KeyFollower.Follower(f, key_paths, timeout = 1)
#         current_key = 0
#         for key in kf:
#             current_key+=1
#         assert current_key == 1001
# =============================================================================


def test_iterates_multiple_incomplete_dataset():
    
    #key_paths = ["data/1000", 'data/2000']
    key_paths = ["keys"]
    f = MultipleIncomplete()
    kf = KeyFollower.Follower(f, key_paths, timeout = 1)
    current_key = 0
    for key in kf:
        current_key+=1
    assert current_key == 2000






    


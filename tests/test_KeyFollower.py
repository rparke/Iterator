import numpy as np
import h5py
import pytest
import os
from nexus_iterator import KeyFollower
from unittest.mock import Mock, patch, MagicMock


class Complete():
    
    def __init__(self):
        self.complete_dict = self.complete_dict()
    
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
        
        
        
        complete_dict = {"dset_1": complete_array}
        
        #dataset_dict = {"data": complete_array}
        return complete_dict
    
    def complete_keys_dataset(self):
        #create complete datasets
        self.complete_array = np.arange(2814).reshape((42,67,1,1))
        self.complete_array.refresh = MagicMock(return_value = None)
        
        self.complete_dict = {"key_1":self.complete_array}
        
        #dataset_dict = {"keys": complete_array}
        return self.complete_dict
    
    def refresh(self):
        return
    
    
class Incomplete():
    def __init__(self):
        self.incomplete_dict = self.incomplete_dict()
    
    def __getitem__(self, key):
        return self.incomplete_dict[key]


    def incomplete_dict(self):
        incomplete_datasets = {"keys":self.incomplete_keys_dataset(), "data":self.incomplete_dataset()}
        return incomplete_datasets
    
    def incomplete_dataset(self):
    
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        incomplete_array = np.arange(1, np.asarray(array_shape).prod()+1)
        incomplete_array[array_shape[-1]*array_shape[-2]*2000:] = 0
        
        incomplete_dict = {"dset_1": incomplete_array}
        
        #dataset_dict = {"data": complete_array}
        return incomplete_dict
    
    def incomplete_keys_dataset(self):
        #create complete datasets
        incomplete_array = np.arange(1, 2814+1)
        incomplete_array[2000:] = 0
        incomplete_array.reshape((42,67,1,1))
        
        
        incomplete_dict = {"key_1":incomplete_array}
        
        #dataset_dict = {"keys": complete_array}
        return incomplete_dict
    
    def refresh(self):
        return


class MultipleIncomplete():
    def __init__(self):
        self.incomplete_dict = self.incomplete_dict()
    
    def __getitem__(self, key):
        return self.incomplete_dict[key]


    def incomplete_dict(self):
        incomplete_datasets = {"keys":self.multiple_incomplete_keys_dataset(), "data":self.multiple_incomplete_dataset()}
        return incomplete_datasets
    
    def multiple_incomplete_dataset(self):
        
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        complete_array = np.arange(np.asarray(array_shape).prod()).reshape(array_shape)
    
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        incomplete_array = np.arange(1, np.asarray(array_shape).prod()+1)
        incomplete_array[array_shape[-1]*array_shape[-2]*2000:] = 0
        
        incomplete_dict = {"dset_1": incomplete_array, "dset_2": complete_array}
        
        #dataset_dict = {"data": complete_array}
        return incomplete_dict
    
    def multiple_incomplete_keys_dataset(self):
        #create complete datasets
        incomplete_array = np.arange(1, 2814+1)
        incomplete_array[2000:] = 0
        incomplete_array.reshape((42,67,1,1))
        
        complete_array = np.arange(2814).reshape((42,67,1,1))
        
        
        incomplete_dict = {"key_1":incomplete_array, "key_2": complete_array}
        
        #dataset_dict = {"keys": complete_array}
        return incomplete_dict
    
    def refresh(self):
        return
    
class IncompleteUpdate():
    def __init__(self):
        self.incomplete_dict = self.incomplete_dict()
        self.count = 0
    
    def __getitem__(self, key):
        return self.incomplete_dict[key]


    def incomplete_dict(self):
        incomplete_datasets = {"keys":self.incomplete_keys_dataset(), "data":self.incomplete_dataset()}
        return incomplete_datasets
    
    def incomplete_dataset(self):
    
        array_shape = (42,67,10,4096)
        
        #create complete datasets
        self.incomplete_array = np.arange(1, np.asarray(array_shape).prod()+1)
        self.incomplete_array[array_shape[-1]*array_shape[-2]*2000:] = 0
        
        self.incomplete_dict = {"dset_1": self.incomplete_array}
        
        #dataset_dict = {"data": complete_array}
        return self.incomplete_dict
    
    def incomplete_keys_dataset(self):
        #create complete datasets
        self.incomplete_key_array = np.arange(1, 2814+1)
        self.incomplete_key_array[2000:] = 0
        self.incomplete_key_array.reshape((42,67,1,1))
        
        
        self.incomplete_dict = {"key_1":self.incomplete_key_array}
        
        #dataset_dict = {"keys": complete_array}
        return self.incomplete_dict
    
    def refresh(self):
        self.count += 1
        if self.count == 10:
            self.incomplete_key_array[2000:2500] = np.arange(2000,2500)
            self.incomplete_array[2000*40960:2500*40960] = np.arange(2000*40960, 2500*40960)


#1




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






    


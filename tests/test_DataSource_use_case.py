
import numpy as np
import h5py
import pytest
import os
from nexus_iterator import DataSource
from nexus_iterator import KeyFollower
from unittest.mock import MagicMock, Mock, patch


#Creating datasets from numpy arrays
class DataSet(np.ndarray):pass

def create_dataset_from_numpy_array(numpy_array):
    ds = DataSet(numpy_array.shape)
    ds[:] = numpy_array[:]
    ds.refresh = lambda:None
    return ds

#Create a dataset of keys that is completely filled with non-zero values
#Number of iterations = 50
complete_dataset_data = create_dataset_from_numpy_array(np.arange(50*10).reshape(5,10,1,10))
complete_dataset_keys = create_dataset_from_numpy_array(np.arange(50).reshape(5,10,1,1)+1)

#Number of iterations = 40
incomplete_dataset_data = complete_dataset_data.copy()
incomplete_dataset_data[-1] = 0
incomplete_dataset_data = create_dataset_from_numpy_array(incomplete_dataset_data)
incomplete_dataset_keys = complete_dataset_keys.copy()
incomplete_dataset_keys[-1] = 0
incomplete_dataset_keys = incomplete_dataset_keys.reshape(complete_dataset_keys.shape)
incomplete_dataset_keys = create_dataset_from_numpy_array(incomplete_dataset_keys)


four_dimensional_dataset_data = complete_dataset_data.copy()
four_dimensional_dataset_data = create_dataset_from_numpy_array(four_dimensional_dataset_data)

four_dimensional_dataset_keys = complete_dataset_keys.copy()
four_dimensional_dataset_keys = create_dataset_from_numpy_array(four_dimensional_dataset_keys)


three_dimensional_dataset_data = complete_dataset_data.copy()
three_dimensional_dataset_data = three_dimensional_dataset_data.reshape(50,1,10)
three_dimensional_dataset_data = create_dataset_from_numpy_array(three_dimensional_dataset_data)

three_dimensional_dataset_keys = complete_dataset_keys.copy()
three_dimensional_dataset_keys = three_dimensional_dataset_keys.reshape(50,1,1)
three_dimensional_dataset_keys = create_dataset_from_numpy_array(three_dimensional_dataset_keys)






def test_iterates_complete_dataset():

      
      h5py.File = MagicMock()
      h5py.File.return_value = {"keys": {'complete':complete_dataset_keys}, "data": {"complete": complete_dataset_data}}
      
      data_paths = ['data']
      key_paths = ['keys']
      f = h5py.File()
      df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
      current_key = 0
      for dset in df:
        current_key+= 1
      assert current_key == 50
      
def test_iterates_incomplete_dataset():

      
      h5py.File = MagicMock()
      h5py.File.return_value = {"keys": {'incomplete':incomplete_dataset_keys}, "data": {"incomplete": incomplete_dataset_data}}
      
      data_paths = ['data']
      key_paths = ['keys']
      f = h5py.File()
      df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
      current_key = 0
      for dset in df:
        current_key+= 1
      assert current_key == 40
      
      
def test_iterates_multiple_incomplete_dataset():

      
      h5py.File = MagicMock()
      h5py.File.return_value = {"keys": {'complete':complete_dataset_keys,
                                         'incomplete':incomplete_dataset_keys}, 
                                "data": {"complete": complete_dataset_data,
                                    "incomplete": incomplete_dataset_data}}
      
      data_paths = ['data']
      key_paths = ['keys']
      f = h5py.File()
      df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
      current_key = 0
      for dset in df:
        current_key+= 1
      assert current_key == 40
      





#Check that the correct dataset is returned ignoring shapes
def test_correct_return_data_complete():
      h5py.File = MagicMock()
      h5py.File.return_value = {"keys": {'complete':complete_dataset_keys}, 
                                "data": {"complete": complete_dataset_data}}
      data_paths = ['data']
      key_paths = ['keys']
      f = h5py.File()
      df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
      full_dataset = np.array([])
      for dset in df:
          full_dataset = np.concatenate((full_dataset, dset[0].flatten()))
      assert(complete_dataset_data.flatten() == full_dataset.flatten()).all()
      



#Test correct shapes are returned


def test_correct_return_shape():
    h5py.File = MagicMock()
    h5py.File.return_value = {"keys":{"four_dimensional": four_dimensional_dataset_keys,
                                      "three_dimensional": three_dimensional_dataset_keys},
                              "data":{"four_dimensional": four_dimensional_dataset_data,
                                      "three_dimensional": three_dimensional_dataset_data}}
    
    data_paths = ['data']
    key_paths = ['keys']
    f = h5py.File()
    df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
    for dset in df:
        assert dset[0].shape == (1,1,1,10) and dset[1].shape == (1,1,10)


            
def test_reset_method_iterates_correct_length():
      h5py.File = MagicMock()
      h5py.File.return_value = {"keys": {'complete':complete_dataset_keys}, "data": {"complete": complete_dataset_data}}
      
      data_paths = ['data']
      key_paths = ['keys']
      f = h5py.File()
      df = DataSource.DataFollower(f, key_paths, data_paths, timeout = 1)
      current_key = 0
      for dset in df:
        current_key+= 1
        
      df.reset()
      for dset in df:
        current_key+= 1
      assert current_key == 100
    




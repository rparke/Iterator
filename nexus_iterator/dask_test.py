#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:20:34 2020

@author: eja26438
"""

#import nexus_iterator.KeyFollower as KeyFollower
#import nexus_iterator.DataSource as DataSource
from nexus_iterator.KeyFollower import Follower
from nexus_iterator.DataSource import DataFollower
from nexus_iterator.FrameGrabber import Grabber

import numpy as np
import dask
from dask.distributed import Client
from dask.threaded import get
import time
import h5py
from threading import Thread
from queue import Queue
import multiprocessing



class ScalariseImage():
    
    def __init__(self,
                 hdf5_filepath,
                 dataset_path):
        self.hdf5_filepath = hdf5_filepath
        self.dataset_path = dataset_path
        self.first_row_written = False
        self.row_length = None
        
        
        #Set of methods for indexing the image
    def _first_row_written(self):
        with h5py.File(self.hdf5_filepath, "r", swmr = True) as f:
            shape = f[self.dataset_path].shape
            print(shape[1])
            if shape[1] > 1:
                self.first_row_written = True
                
                
    def _get_row_length(self):
        while not self.first_row_written:
            self._first_row_written()
            print("Sleeping")
            time.sleep(10)
        
        with h5py.File(self.hdf5_filepath, "r", swmr = True) as f:
            shape = f[self.dataset_path].shape
            self.row_length = shape[0]
            return shape[0]
                
                
    def _get_frame_index(self, index):
        self._get_row_length()
        if self.row_length == None:
            class FirstRowNotWritten(Exception):pass
            raise FirstRowNotWritten()
            
        else:
            x_index = index//self.row_length
            y_index = index%self.row_length
            
        return [x_index, y_index]
    
    
    def get_frame(self, index):
        x_index, y_index = self._get_frame_index(index)
        with h5py.File(self.hdf5_filepath, "r", swmr = True) as f:
            arr = f[self.dataset_path][x_index, y_index][...]
            return arr
            
    
    
    def scalarise (self, index):
        frame = self.get_frame(index)
        return [frame.sum(), index]
    
    def scalarise_write(self, index):
        frame = self.get_frame(index)
        frame_sum = frame.sum()
        
        with open("/Users/richardparke/Documents/Diamond/Iterator_data/test_write.txt", "r+") as wrt:
                  wrt.append(str(index) + ":" + str(frame_sum))
             
    
    
    
scalar_test = ScalariseImage("/Users/richardparke/Documents/Diamond/Iterator_data/i18-81742.nxs", 
                             'entry/Xspress3A/data')




def write_dask_futures():
    client = Client()
    scalar_array = []
    start_time = time.time()
    for index in range(1000):
        client.submit(scalar_test.scalarise_write, index)
    end_time = time.time()
    print("Dask Futures Time: {}".format(end_time - start_time))



def run_dask_futures():
    client = Client()
    scalar_array = []
    start_time = time.time()
    for index in range(1000):
        scalar_array.append(client.submit(scalar_test.scalarise, index))
    end_time = time.time()
    print("Dask Futures Time: {}".format(end_time - start_time))
    return [scalar_array, end_time - start_time]
    

def run_map_dask_futures():
    client = Client()
    start_time = time.time()
    scalar_array = client.map(scalar_test.scalarise, range(1000))
    end_time = time.time()
    print("Dask Futures Map Time: {}".format(end_time - start_time))
    return [scalar_array, end_time - start_time]

def run_serial_jobs():
    scalar_array = []
    start_time = time.time()
    for index in range(1000):
        scalar_array.append(scalar_test.scalarise(index))
    end_time = time.time()
    print("Normal Time: {}".format(end_time - start_time))
    return [scalar_array, end_time - start_time]


def run_map():
    start_time = time.time()
    scalar_array = map(scalar_test.scalarise, range(1000))
    end_time = time.time()
    print("Python Map Time: {}".format(end_time - start_time))
    return [scalar_array, end_time - start_time]


def append_futures_to_list():
    futures = run_dask_futures()
    arr = np.ones(1000)
    for f in futures[0]:
        f = f.result()
        result_index = f[1]
        result_sum = f[0]
        arr[result_index] = result_sum
    return arr

#arr = run_dask_futures()


    




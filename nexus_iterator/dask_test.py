#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:20:34 2020

@author: eja26438
"""

#import nexus_iterator.KeyFollower as KeyFollower
#import nexus_iterator.DataSource as DataSource
from nexus_iterator.KeyFollower import Follower, FrameGrabber
from nexus_iterator.DataSource import DataFollower

import numpy as np
import dask
from dask.distributed import Client, as_completed
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
        self.row_length = None
        
                
    def _get_row_length(self):        
        with h5py.File(self.hdf5_filepath, "r", swmr = True) as f:
            shape = f[self.dataset_path].shape
            self.row_length = shape[0]
            return shape[0]
                
                
    def _get_frame_index(self, index):
        self._get_row_length()
        x_index = index%self.row_length
        y_index = index//self.row_length
        return [x_index, y_index]
    
    
    def get_frame(self, index):
        x_index, y_index = self._get_frame_index(index)
        with h5py.File(self.hdf5_filepath, "r", swmr = True) as f:
            arr = f[self.dataset_path][x_index, y_index][...]
            return arr
            
    
    
    def scalarise (self, index):
        frame = self.get_frame(index)
        return [frame.sum(), index]
    
        
    
def scalarise(index,
              hdf5_file = "test_big_data.h5", 
                             dataset = 'datasets/data_1'):
    
    si = ScalariseImage(hdf5_file, dataset)
    frame = si.get_frame(index)
    return [frame.sum(), index]

def double(index,
              hdf5_file = "/Users/richardparke/Documents/Diamond/Iterator_data/i18-81742.nxs", 
                             dataset = 'entry/Xspress3A/data'):
    
    si = ScalariseImage(hdf5_file, dataset)
    frame = si.get_frame(index)
    return [frame + np.ones(frame.shape)*1000, index]
    
    
scalar_test = ScalariseImage("/Users/richardparke/Documents/Diamond/Iterator_data/i18-81742.nxs", 
                             'entry/Xspress3A/data')


def create_key_queue(hdf5_filepath, key_datasets, queue):
    with h5py.File(hdf5_filepath, "r", swmr = True) as f:
        kf = Follower(f, key_datasets)
        for key in kf:
            queue.put(key)
        queue.put("End")

def write_dask_futures():
    client = Client()
    scalar_array = []
    start_time = time.time()
    for index in range(1000):
        client.submit(scalar_test.scalarise_write, index)
    end_time = time.time()
    print("Dask Futures Time: {}".format(end_time - start_time))



def run_dask_futures(queue, scalar_array):
    client = Client()
    start_time = time.time()
    while True:
        current_key = queue.get()
        if current_key == "End":
            break
        
        else:
            scalar_array.append(client.submit(scalar_test.scalarise, current_key))
    end_time = time.time()
    print("Dask Futures Time: {}".format(end_time - start_time))
    return [scalar_array, end_time - start_time]
    

def run_map_dask_futures():
    client = Client()
    start_time = time.time()
    scalar_array = client.map(scalar_test.scalarise, range(5628))
    end_time = time.time()
    print("Dask Futures Map Time: {}".format(end_time - start_time))
    return [scalar_array, end_time - start_time]

def run_serial_jobs():
    scalar_array = []
    start_time = time.time()
    for index in range(2800):
        scalar_array.append(scalar_test.scalarise(index))
    end_time = time.time()
    print("Python Serial Time: {}".format(end_time - start_time))
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


def result_printer(futures_array):
    for future in as_completed(futures_array):
        print(future)
    return

def main():
    queue = Queue()
    futures_array = []
    t_queue_writer = Thread(name = "queue_writer", target = create_key_queue("/Users/richardparke/Documents/Diamond/Iterator_data/i18-81742.nxs",
                                                                             ['entry/solstice_scan/keys'],
                                                                             queue))
    t_dask_consumer = Thread(name = "dask_consumer", target = run_dask_futures(queue = queue, scalar_array = futures_array))
    t_result_printer = Thread(name = "result_printer", target = result_printer(futures_array))
    t_queue_writer.start()
    t_dask_consumer.start()
    t_result_printer.start()
    t_queue_writer.join()
    t_dask_consumer.join()
    t_result_printer.join()
    return futures_array
    



with h5py.File("/Users/richardparke/Documents/Diamond/Iterator_data/i18-81742.nxs", "r") as f:
    fg = FrameGrabber('entry/Xspress3A/data', f)
    ds = f['entry/Xspress3A/data']
    print(fg.Grabber(20))
    print(fg.Grabber(20).shape)





class Scalarise():
    def __init__(self,
                 hdf5_file,
                 datasets):
        self.hdf5_file = hdf5_file
        self.datasets = datasets
    
    def scl(self, index):
        with h5py.File(self.hdf5_file, "r", swmr = True) as f:
            fg = FrameGrabber(self.datasets, f)
            frame = fg.Grabber(index)
            frame_shape = [1 for i in range(len(frame.shape))]
            frame = frame.sum()
            frame = frame.reshape(frame_shape)
            return frame

sc = Scalarise("/Users/richardparke/Documents/Diamond/Iterator_data/i18-81742.nxs", 'entry/Xspress3A/data')








#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 17:00:21 2020

@author: eja26438
"""

import h5py
from swmr_tools.KeyFollower import Follower, FrameGrabber
import numpy as np
complete_keys = np.arange(25).reshape(5,5,1,1) + 1
complete_dataset = np.random.randint(low = 1, high = 5000, size = (5,5,10,20))

with h5py.File("test.h5", "w", libver = "latest") as f:
    f.create_group('keys')
    f.create_group('data')
    f['keys'].create_dataset("key_1", data = complete_keys)
    f['data'].create_dataset("data_1", data = complete_dataset)
    

import time

def long_function(key, filepath = "test.h5", dataset = "data/data_1"):
    time.sleep(1)
    print(f"Starting key {key}")
    with h5py.File(filepath, "r", swmr = True) as f:
        fg = FrameGrabber(dataset, f)
        frame = fg.Grabber(key)
        print(f"getting frame sum {frame.sum()}")
        return frame.sum()

def key_generator(queue, filepath = "test.h5"):
    with h5py.File(filepath, "r", swmr = True) as f:
        kf = Follower(f, ['keys'], timeout = 0.1)
        for key in kf:
            queue.put(key)
            
        queue.put("End")

def frame_consumer_serial(queue, filepath = "test.h5", dataset = "data/data_1"):
    return_list = []
    key = queue.get()
    while key != 'End':
        #print(key)
        return_list.append(long_function(key))
        key = queue.get()
    #print("Done")
    return return_list


from dask.distributed import Client

def frame_consumer_parallel(queue, filepath = "test.h5", dataset = "data/data_1"):
    return_list = []
    client = Client()
    key = queue.get()
    while key != 'End':
        return_list.append(client.submit(long_function, key))
        key = queue.get()
    return client.gather(return_list)

import time
from threading import Thread
from queue import Queue

def main_1():
    queue = Queue()
    key_generator_thread = Thread(target = key_generator(queue))
    frame_consumer_serial_thread = Thread(target = frame_consumer_serial, args = (queue,))

    start_time = time.time()
    key_generator_thread.start()
    frame_consumer_serial_thread.start()
    key_generator_thread.join()
    frame_consumer_serial_thread.join()
    finish_time = time.time()
    print(f"serial_time_taken = {finish_time - start_time}")

#main_1()

def main_2():
    queue = Queue()
    key_generator_thread = Thread(target = key_generator, args = (queue,))
    frame_consumer_serial_thread = Thread(target = frame_consumer_parallel, args = (queue,))

    start_time = time.time()
    key_generator_thread.start()
    frame_consumer_serial_thread.start()
    key_generator_thread.join()
    frame_consumer_serial_thread.join()
    finish_time = time.time()
    print(f"serial_time_taken = {finish_time - start_time}")

#main_2()




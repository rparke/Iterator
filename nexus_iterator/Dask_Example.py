#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 17:00:21 2020

@author: eja26438
"""

import h5py
import KeyFollower, FrameGrabber
import numpy as np
complete_keys = np.arange(25).reshape(5,5,1,1) + 1
complete_dataset = np.random.randint(low = 1, high = 5000, size = (5,5,10,20))

with h5py.File("test.h5", "w", libver = "latest") as f:
    f.create_group('keys')
    f.create_group('data')
    f['keys'].create_dataset("key_1", data = complete_keys)
    f['data'].create_dataset("data_1", data = complete_dataset)
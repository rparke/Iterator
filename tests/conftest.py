#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 13:12:45 2020

@author: eja26438
"""


from mock import patch, Mock
import pytest
import numpy as np




def complete_dataset():
    #create complete datasets
    complete_array = np.arange(2814).reshape((42,67,1,1))
    
    dataset_dict = {"complete": complete_array}
    group_dict = {"keys":dataset_dict}
    
    
    return group_dict



mock = Mock()
mock.my_name = "tom"

mock.method.return_value = {"This": [1], "Dictionary":[2]}


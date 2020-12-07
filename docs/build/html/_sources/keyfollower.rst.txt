###########
KeyFollower
###########

The KeyFollower class is designed to facilitate live data processing of
datasets contained within an hdf5 file. It achieves this through the use of
two main classes:

* Follower
* FrameGrabber

This tutorial assumes a basic level of skill using the h5py library.
Specifically, you should be comfortable with using h5py to:

* Open and create hdf5_files
* Navigate files using python dictionary methods: *e.g.* using the get() method
* Create groups and datasets

If you are unfamiliar with how to do any of this we recommend reading the
h5py quick start guide: https://docs.h5py.org/en/stable/quick.html


Follower
========

The Follower class can be used to create instances of a python iterator object.
The Follower is central to everything that swmr_tools does and most other
classes either directly use it or are dependent upon the keys it produces.

Example - Iteration through an all non-zero key dataset
-------------------------------------------------------

We will create a dataset of non-zero integers, respresenting a complete set of
scans all flushed to disk ::
 
    import h5py
    from swmr_tools.KeyFollower import Follower
    import numpy as np
    
    #create a sequential array of the numbers 1-8 and reshape them into an array
    # of shape (2,4,1,1)
    complete_key_array = np.arange(8).reshape(2,4,1,1) + 1


We will create an empty hdf5 file, create a group called "keys" and create
a dataset in that group called "key_1" where we will add our array of non-zero
keys ::

    with h5py.File("test_file.h5", "w", libver = "latest") as f:
        f.create_group("keys")
        f["keys"].create_dataset("key_1", data = complete_key_array)

Next, we shall create an instance of the Follower class and demonstrate a
simple example of its use. At a minimum we must pass the h5py.File object 
we wish to read from and a list containing the paths to the hdf5 groups 
containing our keys.

Shown below is an example of using an instance of Follower within a for loop, 
as you would with any standard iterable object. For this basic example of a 
dataset containing only non-zero values, the loop runs 8 times and stops as 
expected ::

    # using an instance of Follower in a for loop
    with h5py.File("test_file.h5", "r", swmr = True) as f:
        kf = Follower(f, ["keys"])
        for key in kf:
            print(key)
    0
    1
    2
    3
    4
    5
    6
    7
            

Example - Iteration through a dataset containg zeros
----------------------------------------------------

The key dataset is a form of metadata which (as we will see in 
detail when looking at the FrameGrabber class) represents whether a frame of 
a given dataset is complete and has been flushed to disk.

Non-zero key values represent frames that have been completely written and 
flushed to disk, while values of zero represent a frame that has not. We 
therefore expect the iterator to halt when the next key is zero and either to
wait for it to update to a non-zero value and continue or to stop iteration 
entirely if a termination condition is met.

We will demonstrate a simple example of this below using a timeout method as 
a termination condition. Timeout is the default method used by Follower 
(although others can be set) ::


    with h5py.File("test_file.h5", "r+") as f:
        #set all values in the second row to zero
        f["keys/key_1"][1,:,:,:] = 0

    with h5py.File("test_file.h5", "r", swmr = True) as f:
        kf = Follower(f, ["keys"], timeout = 1)
        for key in kf:
            print(key)
    0
    1
    2
    3
            
The example above clearly shows that the follower iterates through the first 
row waits for the timeout and then proceeds to halt iteration when the key at
index [1,0] does not change to a non-zero value within the 1 second timeout.

Example - Using other termination methods
-----------------------------------------

The timeout method is 



Follower does not have any inbuilt methods for managing resources, as such
it is the responsibility of the user to ensure that hdf5 files are opened and
closed correctly. This can either be done using exception handling or using
the context manager

Exception Handling 
^^^^^^^^^^^^^^^^^^
::

    try:
        f = h5py.File("test_file.h5", "r", swmr_mode = True)
        kf = Follower(f, "keys")
        for key in kf:
        ...
    finally:
        f.close()

Context Manager
^^^^^^^^^^^^^^^
::

    with h5py.File("test_file.h5", "r", swmr_mode = True) as f:
        kf = Follower(f, "keys")
        for key in kf:
        ...

Manual opening and closing of h5py.File objects is not recommneded.
We strongly recommend using the context manger as it ensures safe access to
resources and is less verbose than using exception handling.

Instances of the Follower class are iterators. They can be used within for
loops or called using the next method ::

    with h5py.File("test_file.h5", "r", swmr_mode = True) as f:
        kf = Follower(f, ["keys"])
        print(next(kf))
    1
        print(next(kf))
    2
        print(next(kf))
    3
        print(next(kf))
    4
        print(next(kf))
    5
        print(next(kf))
    6
        print(next(kf))
    7
        print(next(kf))
    8
    
    with h5py.File("test_file.h5", "r", swmr_mode = True) as f:
        kf = Follower(f, ["keys"])
        for i in kf:
            print(i)
    1
    2
    3
    4
    5
    6
    7
    8

FrameGrabber
============

Indices produced by instances of the KeyFollower class correspond to frames of
relavent datasets
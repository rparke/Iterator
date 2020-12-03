###########
KeyFollower
###########

The KeyFollower class is designed to facilitate live data processing of
datasets contained within an hdf5 file. It achieves this through the use of
two main classes:

* Follower
* FrameGrabber


Follower
========
::
 
    import h5py
    import swmr_tools
    import numpy as np
    complete_key_array = np.arange(8).reshape(2,4,1,1) + 1


We will create an empty hdf5 file using the context manager:

>>> with h5py.File("test_file.h5", "w", libver = "latest") as f:
>>> pass


We will save this array to a dataset in our hdf5 file ::

    with h5py.File("test_file.h5", "r+") as f:
        f.create_group["keys"]
        f["keys"].create_dataset("key_1", data = complete_key_array)


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
        kf = Follower(f, "keys")
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
        kf = Follower(f, "keys")
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
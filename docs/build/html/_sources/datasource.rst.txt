##########
DataSource
##########

The DataSource submodule provides an efficient wrapper for the 
KeyFollower.Follower and KeyFollower.FrameGrabber classes. Instances of the
DataSource.DataFollower class are iterators with similar functionality to
instances of the KeyFollower.Follower class, however rather than indices they
simply produce the frames themselves.

DataFollower
============

The DataFollower class requires 3 arguments:
* An instance of an h5py.File object containing the datasets of interest
* A list of paths to *groups* containing datasets of keys
* A list of paths to *datasets* containing the data you wish to process

THe DataFollower also has an optional timeout argument, which defaults to 1
second unless otherwise specified. This works in exactly the same way as the
timeout for the KeyFollower.Follower class.

First we will create a small dataset and corresponding unique key dataset to use
in our example. The keys will all be non-zero so we should expect to recieve
every frame of the dataset ::

    from swmr_tools.KeyFollower import Follower, FrameGrabber
    import h5py
    import numpy as np
    
    #Create a small dataset to extract frames from
    data = np.random.randint(low = -10000, high = 10000, size = (2,2,5,10))
    keys = np.arange(1,5).reshape(2,2,1,1)
    
    #Save data to an hdf5 File
    with h5py.File("example.h5", "w", libver = "latest") as f:
        f.create_group("keys")
        f.create_group("data")
        f["keys"].create_dataset("keys_1", data = keys)
        f["data"].create_dataset("data_1", data = data)
        
Firstly we will iterate through the frames just using the classes found in the
KeyFollower submodule ::

    with h5py.File("example.h5", "r") as f:
        kf = Follower(f, ["keys"], timeout = 1)
        fg = FrameGrabber("data/data_1", f)
        for key in kf:
            frame = fg.Grabber(key)
            print(f"Frame number: {key}")
            print(str(frame) + "\n")
            
    Frame number: 0
    [[[[-4281  6557 -1425  -627 -6986 -9047 -1977  7788  -580  6283]
       [  500  4060 -1153   -74 -4364 -7244  2729  -656  8432  9709]
       [ 8809  1876  3045 -3542  3356 -3126  -870  5918 -9631  3778]
       [-5345 -2533 -1390   778  5343 -6455  8323 -9691 -6391 -8751]
       [ 9946 -9685  5647    58 -6917 -8293 -2996 -2750 -6316 -3482]]]]
    
    Frame number: 1
    [[[[-1253  9761  6238 -9821  1387  6874  -868  3822 -1616 -5921]
       [-4726 -8688 -2628  2635 -5100 -9442 -2628  5792 -6729 -1501]
       [ 7259  -607  4274  7983  8798  2091  2060 -9672  8567  6648]
       [ 2767  2705  2517  7770 -5285  -622 -8778 -6393  9816  7685]
       [-1871  7310   428 -1829  7096  8685 -9822 -6908  9500  5022]]]]
    
    Frame number: 2
    [[[[ 6683  8590  -806  -701     2 -6832  7351 -7335  6456 -7738]
       [-4767  5214 -9092  9093 -3183  4051 -4525  9185 -5692  2774]
       [ 7472  3384  4274  7456 -3624 -9486 -6718 -5747  8983 -1810]
       [-9976  5840  9276 -7768  3213  4447 -3300  5171  1410 -8409]
       [ 2369  9319  5359 -8501     9  2240  4141  7006  5657  3873]]]]
    
    Frame number: 3
    [[[[ 1869  9865  9101 -4053 -1210  6051 -2587 -4107  5175  4221]
       [ 5282  8801  4959 -5477  5349  5623  8100 -8288  7174 -6669]
       [ 3860  6388 -3374  8572  7730 -1858  3225 -6311  1994 -9195]
       [ 4291  4469 -5639  1853 -5516 -4626  7894  2194  -585 -7488]
       [ 1701 -8787  -873  9719  5926  6615 -6505  8459  5437   842]]]]
       

                
        
    
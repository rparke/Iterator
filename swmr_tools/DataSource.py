import numpy as np
from swmr_tools.KeyFollower import Follower, FrameGrabber




class DataFollower():
    
    def __init__(self, hdf5_file, keypaths, dataset_paths, timeout = 1):
        self.hdf5_file = hdf5_file
        self.dataset_paths = dataset_paths
        self.kf = Follower(hdf5_file, keypaths, timeout)
        
            
        
    def __iter__(self):
        return(self)
    
    
    def __next__(self):
        
            

        if self.kf.is_finished():
            raise StopIteration
        
        else:
            
            current_dataset_index = next(self.kf)
            
            current_dataset_slice = []
            for path in self.dataset_paths:
                fg = FrameGrabber(path, self.hdf5_file)
                current_dataset_slice.append(fg.Grabber(current_dataset_index))
                
            
            #Old method, works but a lot of code
            #current_dataset_slice = self._get_dataset_flattened(current_dataset_index)
            
            #New method, not currently working, gets index using np.unravel_index method
            #current_dataset_slice = self._get_dataset_shaped(current_dataset_index)
            return current_dataset_slice
        
        
    def reset(self):
        self.kf.reset()
        
        

                
                
        
            
            



import numpy as np
import h5py
import os
import time
from multiprocessing import Process
    

class SwmrProcess(Process):
    pass


class Follower():
    def __init__(self,
                 hdf5_file,
                 key_datasets,
                 timeout = 10,
                 termination_conditions = ["timeout"]):
                     self.hdf5_file = hdf5_file
                     self.current_key = -1
                     self.current_max = -1
                     self.timeout = timeout
                     self.key_datasets = key_datasets
                     self.termination_conditions = termination_conditions

                         
                         
    def __iter__(self):
        return(self)
    
    def __next__(self):
        
        self._timer_reset()
        if not self.is_finished():
            while not self._is_next():
                time.sleep(0.2)
                if self.is_finished():
                    raise StopIteration
            
            if self._is_next():
                self.current_key += 1
                x = self.current_key
                self._timer_reset()
                return x
        
        else:
            raise StopIteration
    
        
    
    def reset(self):
        self.current_key = -1
        self.current_max = -1
        
    def _timer_reset(self):
        self.start_time = time.time()
                             
     
        

# =============================================================================
#     def get_current_max(self):
#          current_max = []
#          for key_path in self.key_datasets:
#              for dataset in self.hdf5_file[key_path].values():
#                  dataset.refresh()
#                  current_max.append(np.nonzero(dataset[...].flatten())[0].max())
#          return np.asarray(current_max).min()
#          
# =============================================================================


      
    def _is_next(self):
        
        
        is_next = True
        
        for key_path in self.key_datasets:
            for dataset in self.hdf5_file[key_path].values():
                dataset.refresh()
                #print(dataset.flatten()[self.current_key+1])
                
                try:
                    if dataset[...].flatten()[self.current_key+1] == 0:
                        is_next = False
                    else:
                        pass
                except:
                    is_next = False
        return is_next
                
        
    def _timeout(self):
        if time.time() > self.start_time + self.timeout:
            return True
        else:
            return False
        
        
    def _finish_condition(self):
        conditions = {"timeout": self._timeout(), "always_true" : True}
        
        #Set finish to true if any of the termination conditions are met
        finish = False
        for condition in self.termination_conditions:
            finish = finish or conditions[condition]
        
        
        #return conditions[self.termination_conditions[0]]
        return finish
        
        
    def is_finished(self):
        if (not self._is_next()) and (self._finish_condition()):
            return True
        
        else:
            return False



#Functions that may be needed for the plotters      
        
    def _update_key_dataset_shape(self):
        self.shape_list = []
        for keypath in self.key_datasets:
            dataset = self.hdf5_file[keypath]
            self.shape_list.append(dataset.shape)
            
    def _reshape_flat_dataset(self):
        pass
    

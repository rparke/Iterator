import numpy as npimport h5pyimport osfrom iterator_pkg import KeyFollowerimport timeclass DataFollower(KeyFollower.Follower):        def __init__(self,                 hdf5_file,                 key_datasets,                 data_datasets,                 timeout = 10):        super().__init__(hdf5_file, key_datasets, timeout)        self.data_datasets = data_datasets        self.dataset_indices = np.asarray([0 for i in data_datasets])                         def __iter__(self):        return(self)            def __next__(self):                #Fix for now to ensure we have correctly initialised the dataframe shape        self._get_frame_shape()                            if not self.is_finished():                                    while not self._is_next():                time.sleep(1)                if self._timeout():                    raise StopIteration                        if self._is_next():                x = self._get_dataset_slices()                self._update_dataset_start_index()                self.current_key += 1                self._timer_reset()                return x                else:            raise StopIteration                      #Creates a list of frame shapes           def _get_frame_shape(self):        self.frame_shape_list = []        for dataset in self.data_datasets:            self.frame_shape_list.append((self.hdf5_file[dataset].shape)[-2] * (self.hdf5_file[dataset].shape)[-1])            self.frame_shape_array = np.asarray(self.frame_shape_list)                        #Moves flattened dataset to correct index for all datasets    def _update_dataset_start_index(self):        self.dataset_indices = self.dataset_indices + self.frame_shape_array                    def _get_dataset_slices(self):        return_list = []        for i in range(len(self.data_datasets)):            ds = self.hdf5_file[self.data_datasets[i]]            return_list.append(ds[...].flatten()[self.dataset_indices[i]:self.dataset_indices[i] + self.frame_shape_array[i]])                    return(return_list)                                                                                    
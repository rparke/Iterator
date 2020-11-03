import numpy as npimport h5pyimport pytestimport osfrom nexus_iterator import KeyFollowerdef test_iterates_complete_dataset():                filepath = "hdf5_tests/complete_1.h5"      #filepath = "hdf5_tests/i18-81742.nxs"      key_paths = ["keys/complete"]      with h5py.File(filepath, "r") as f:          #data = f[key_paths[0]][...]           kf = KeyFollower.Follower(f, key_paths, timeout = 1)           current_key = 0           for key in kf:               current_key+= 1                  assert current_key == 2814                          def test_iterates_incomplete_dataset():        filepath = "hdf5_tests/incomplete_1.h5"    key_paths = ["incomplete_2814"]    with h5py.File(filepath, "r") as f:        kf = KeyFollower.Follower(f, key_paths, timeout = 1)        current_key = 0        for key in kf:            current_key+= 1        assert current_key == 2001    def test_iterates_multiple_incomplete_dataset():        filepath = "hdf5_tests/multiple_incomplete_1.h5"    key_paths = ["data/1000", 'data/2000']    with h5py.File(filepath, "r") as f:        kf = KeyFollower.Follower(f, key_paths, timeout = 1)        current_key = 0        for key in kf:            current_key+=1        assert current_key == 1001                                
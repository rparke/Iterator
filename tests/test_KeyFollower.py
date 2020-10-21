import numpy as npimport h5pyimport pytestimport osfrom iterator_pkg import KeyFollower#Test the functionality of the whole class# If all key datasets contain all zeros, return an appropriate resultdef test_all_zeros():        #Generate arrays for testing    test_arr_1 = np.zeros(shape = (20,40, 1))    test_arr_2 = np.zeros(shape = (20,40, 1))    test_arr_3 = np.zeros(shape = (20,40, 1))    test_arr_4 = np.zeros(shape = (20,40, 1))            #Generate dictionary containing test arrays    test_arr_dict = {"arr_1": test_arr_1,                      "arr_2": test_arr_2,                      "arr_3": test_arr_3,                     "arr_4": test_arr_4}            test_follower = KeyFollower.Follower(key_datasets = test_arr_dict)    test_follower.can_start_reading()    assert test_follower.start_reading == False        #If a single key dataset contains all zeros, return an appropriate resultdef test_any_zeros():    test_arr_1 = np.ones(shape = (20,40, 1))    test_arr_2 = np.ones(shape = (20,40, 1))    test_arr_3 = np.ones(shape = (20,40, 1))    test_arr_4 = np.zeros(shape = (20,40, 1))        #Generate dictionary containing test arrays    test_arr_dict = {"arr_1": test_arr_1,                      "arr_2": test_arr_2,                      "arr_3": test_arr_3,                     "arr_4": test_arr_4}        test_follower = KeyFollower.Follower(key_datasets = test_arr_dict)    test_follower.can_start_reading()    assert test_follower.start_reading == False        def test_current_max():        #Generate arrays for testing    test_arr_1 = np.zeros(shape = (20,40, 1))    test_arr_2 = np.zeros(shape = (20,40, 1))    test_arr_3 = np.zeros(shape = (20,40, 1))    test_arr_4 = np.zeros(shape = (20,40, 1))        test_arr_1[:10] = np.ones(shape = (10, 40,1))    test_arr_2[:14] = np.ones(shape = (14, 40,1))    test_arr_3[:13] = np.ones(shape = (13, 40,1))    test_arr_3[13, :10] = np.ones(shape = (10,1))    test_arr_4[:9] = np.ones(shape = (9, 40,1))                    #Generate dictionary containing test arrays    test_arr_dict = {"arr_1": test_arr_1,                      "arr_2": test_arr_2,                      "arr_3": test_arr_3,                     "arr_4": test_arr_4}                test_follower = KeyFollower.Follower(key_datasets = test_arr_dict)    assert test_follower.current_max() == np.max(np.nonzero(test_arr_4.flatten()))  #Check Key Follower follows updates correctlydef test_updated_keys():        test_arr_1 = np.zeros(shape = (20,40, 1))    test_arr_2 = np.zeros(shape = (20,40, 1))    test_arr_3 = np.zeros(shape = (20,40, 1))    test_arr_4 = np.zeros(shape = (20,40, 1))        test_arr_1[:10] = np.ones(shape = (10, 40,1))    test_arr_2[:14] = np.ones(shape = (14, 40,1))    test_arr_3[:13] = np.ones(shape = (13, 40,1))    test_arr_3[13, :10] = np.ones(shape = (10,1))    test_arr_4[:9] = np.ones(shape = (9, 40,1))        test_arr_dict = {"arr_1": test_arr_1,                      "arr_2": test_arr_2,                      "arr_3": test_arr_3,                     "arr_4": test_arr_4}        test_follower = KeyFollower.Follower(key_datasets = test_arr_dict)        initial_max = np.max(np.nonzero(test_arr_4.flatten()))    initial_max_test = test_follower.current_max()            test_arr_1 = np.zeros(shape = (20,40, 1))    test_arr_2 = np.zeros(shape = (20,40, 1))    test_arr_3 = np.zeros(shape = (20,40, 1))    test_arr_4 = np.zeros(shape = (20,40, 1))        test_arr_1[:11] = np.ones(shape = (11, 40,1))    test_arr_2[:15] = np.ones(shape = (15, 40,1))    test_arr_3[:14] = np.ones(shape = (14, 40,1))    test_arr_3[14, :10] = np.ones(shape = (10,1))    test_arr_4[:10] = np.ones(shape = (10, 40,1))        test_arr_dict = {"arr_1": test_arr_1,                      "arr_2": test_arr_2,                      "arr_3": test_arr_3,                     "arr_4": test_arr_4}            test_follower.update_keys(test_arr_dict)    final_max = np.max(np.nonzero(test_arr_4.flatten()))    final_max_test = test_follower.current_max()            assert initial_max == initial_max_test and final_max == final_max_test                                

# coding: utf-8

# In[1]:

import numpy as np
import os

files_ext = {0:'.in', 1:'.out'}
files = {0:'me_at_the_zoo', 1:'videos_worth_spreading', 2:'trending_today', 3:'kittens'} 


# In[11]:

def load_data(id_file_to_load = 0, print_debug = True):
    print('\n***************** Loading *****************')
    # Load file
    file = open(files[id_file_to_load] + files_ext[0], 'r') 

    # Header / Video / Endpoints / request descr. / Cache
    header = file.readline().replace('\n','')
    header = np.fromstring(header, dtype=int, sep=' ')
    header_dict = {   'n_video':header[0], 'n_endpoint':header[1], 
                      'requ_des':header[2], 'n_cache':header[3],
                      'size_cache':header[4]}

    # Video size in MB
    video_size = file.readline().replace('\n','')
    video_size = np.fromstring(video_size, dtype=int, sep=' ')

    # Endpoints locations and connections
    endpoint_cache = np.zeros((header_dict['n_endpoint'], header_dict['n_cache'])) # Latency endpoint to cache
    endpoint_datacenter = np.zeros(header_dict['n_endpoint']) # Latency endpoint to datacenter
    endpoint_video = np.zeros((header_dict['n_endpoint'], header_dict['n_video'])) # Endpoints requests

    # Reding endpoint to cache latency and endpoint to data_center latency
    for id_endpoint in range(header_dict['n_endpoint']):
        endpoint = file.readline().replace('\n','').split(' ')
        endpoint_datacenter[id_endpoint] = int(endpoint[0])
        n_latency = int(endpoint[1])
        for i in range(n_latency):
            lat_cache = file.readline().replace('\n','').split(' ')
            endpoint_cache[id_endpoint, int(lat_cache[0])] = int(lat_cache[1])

    for id_requ_des in range(header_dict['requ_des']):
        requ_des = file.readline().replace('\n','').split(' ')
        endpoint_video[int(requ_des[1]), int(requ_des[0])] += int(requ_des[2])
    file.close()
    
    if print_debug:
        print('File description', '\t', header_dict)
        print('Videos sizes', '\t\tshape=', video_size.shape, ', nnz=', len(np.nonzero(video_size)[0]))
        print('Endpoint to chache', '\tshape=', endpoint_cache.shape, ', nnz=', len(np.nonzero(endpoint_cache)[0]))
        print('Endpoint to video', '\tshape=', endpoint_video.shape, ', max=', np.max(endpoint_video))
    
    return endpoint_cache, endpoint_datacenter, endpoint_video, video_size


def save_file(id_file_to_save = 0, caches_video_lists=None):
    print('\n***************** Saving *****************')
    filename = files[id_file_to_save] + files_ext[1]
    # Delete if existing
    if os.path.isfile(filename):
        os.remove(filename)
    file = open(filename, 'a') 
    
    # Write number caches
    file.write(str(len(caches_video_lists)) + '\n')

    # Write each cache
    for i, caches in enumerate(caches_video_lists):
        # Print chache id
        file.write(str(i) + ' ')
        for j, video in enumerate(caches):
            # Print video ids
            file.write(str(video))
            # Print space only if not last item
            if j != len(caches)-1:
                file.write(' ')
        file.write('\n')
    file.close()
    # Out save file
    print('... saved as \"' + filename + '\"')

# Load data
endpoint_cache, endpoint_datacenter, endpoint_video, video_size = load_data(id_file_to_load=0)

test_out = [[2],[3, 1],[0, 1]]
# Save data
save_file(id_file_to_save=0, caches_video_lists=test_out)


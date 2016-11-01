import time
import numpy as np
import h5py

#OSCAR
# 25 GB
# Create 0.0
# Numpy copy 35.63
# Write 200.77
# Read - Copy 101.92
# Read - Constructor 196.25
# Read - Direct 77.38
#

def format_size(num_bytes):
    """Pretty print a file size."""
    num_bytes = float(num_bytes)
    KiB = 1024
    MiB = KiB * KiB
    GiB = KiB * MiB
    TiB = KiB * GiB
    PiB = KiB * TiB
    EiB = KiB * PiB
    ZiB = KiB * EiB
    YiB = KiB * ZiB
    if num_bytes > YiB:
        output = '%.3g YB' % (num_bytes / YiB)
    elif num_bytes > ZiB:
        output = '%.3g ZB' % (num_bytes / ZiB)
    elif num_bytes > EiB:
        output = '%.3g EB' % (num_bytes / EiB)
    elif num_bytes > PiB:
        output = '%.3g PB' % (num_bytes / PiB)
    elif num_bytes > TiB:
        output = '%.3g TB' % (num_bytes / TiB)
    elif num_bytes > GiB:
        output = '%.3g GB' % (num_bytes / GiB)
    elif num_bytes > MiB:
        output = '%.3g MB' % (num_bytes / MiB)
    elif num_bytes > KiB:
        output = '%.3g KB' % (num_bytes / KiB)
    else:
        output = '%.3g B' % num_bytes
    return output


NUM_GB = 2
NUM_BYTES = 1024*1024*1024*NUM_GB
print format_size(NUM_BYTES)
t = time.clock()
smallarray = np.random.randint(0, 1000000000000, 1024*1024)
smallarray = smallarray.view('int8')
array = np.empty(shape=(NUM_BYTES,), dtype='int8')
for i in xrange(NUM_BYTES/len(smallarray)):
    array[i*len(smallarray):(i*len(smallarray))+len(smallarray)] = smallarray[:]
print 'Create', time.clock() - t
t = time.clock()
array2 = np.array(array)
print 'Numpy copy', time.clock() - t
del array2
t = time.clock()
f = h5py.File('mem', driver='core', backing_store=False, libver='latest')
dset = f.create_dataset('array', array.shape, array.dtype,
                        maxshape=array.shape, compression='gzip',
                        fletcher32=False, shuffle=False)
dset[:] = array
print 'Write', time.clock() - t
del array
t = time.clock()
f_in = h5py.File(f.fid, mode='r', driver='core', backing_store=False, libver='latest')
array_in = f_in['array']
array_in_np = np.empty(array_in.shape, dtype=array_in.dtype)
array_in_np[:] = array_in[:]
print 'Read - Copy', time.clock() - t
del array_in_np
t = time.clock()
f_in2 = h5py.File(f.fid, mode='r', driver='core', backing_store=False, libver='latest')
array_in = f_in['array']
array_in_np = np.array(array_in)
array_in_np[:] = array_in[:]
print 'Read - Constructor', time.clock() - t
del array_in_np
t = time.clock()
f_in3 = h5py.File(f.fid, mode='r', driver='core', backing_store=False, libver='latest')
array_in = f_in['array']
array_in_np = np.empty(array_in.shape, dtype=array_in.dtype)
array_in.read_direct(array_in_np)
print 'Read - Direct', time.clock() - t
del array_in_np




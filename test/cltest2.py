import pyopencl as cl
import numpy as np


SRC = """
__kernel void T(__global const float *a, __global float *result){
    int m = get_global_id(0);
    int n = get_global_id(1);
    int h = get_global_size(0);
    int w = get_global_size(1);
    int index = n*h + m;
    
    result[index] = a[w*m + n];
}
"""

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

kernel = cl.Program(ctx, SRC).build()


input_np = np.arange(6, dtype=np.float32).reshape(3, 2)
in_shape = input_np.shape
result_np = np.empty((in_shape[1], in_shape[0]), dtype=np.float32)

input_cl = cl.Buffer(ctx, mf.READ_ONLY, input_np.nbytes)
result_cl = cl.Buffer(ctx, mf.WRITE_ONLY, result_np.nbytes)

cl.enqueue_copy(queue, input_cl, input_np)

e = kernel.T(queue, in_shape, None, input_cl, result_cl)
e.wait()

cl.enqueue_copy(queue, result_np, result_cl)

print(result_np)

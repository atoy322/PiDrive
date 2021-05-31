import time

import pyopencl as cl
import numpy as np



SRC = """
__kernel void add(__global const float *a, __global float *buf){
    int gid;
    gid = get_global_id(0);
    buf[gid] = a[gid] * a[gid] + a[gid];
}
"""

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

host_a = np.arange(1000000, dtype=np.float32)
host_buf = np.empty_like(host_a)

dev_a = cl.Buffer(ctx, flags=mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=host_a)
dev_buf = cl.Buffer(ctx, flags=mf.WRITE_ONLY, size=host_a.nbytes)

prg = cl.Program(ctx, SRC).build()

t = time.time()
prg.add(queue, host_a.shape, None, dev_a, dev_buf)
gpu_t = time.time() - t
cl.enqueue_copy(queue, host_buf, dev_buf)


t = time.time()
b = host_a*host_a + host_a
cpu_t = time.time() - t


print("GPU:", gpu_t)
print("CPU:", cpu_t)


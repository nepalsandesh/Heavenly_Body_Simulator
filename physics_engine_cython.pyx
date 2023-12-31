# physics_engine_cython.pyx

import numpy as np
cimport numpy as np

cdef double magnitude(double[:] arr):
    return np.sqrt(arr[0]**2 + arr[1]**2 + arr[2]**2)

def unit_vector(double[:] arr):
    cdef double mag = magnitude(arr=arr)
    return arr[0] / mag, arr[1] / mag, arr[2] / mag

def compute_force_vectors_cython(list bodies):
    cdef int num_bodies = len(bodies)
    cdef double[:, :, :] distance_list = np.zeros((num_bodies, num_bodies, 3))
    cdef double[:, :, :] force_list = np.zeros((num_bodies, num_bodies, 3))
    cdef double[:, :] net_force = np.zeros((num_bodies, 3))

    # computing distance vectors
    cdef double[:] distance
    for i in range(num_bodies):
        for j in range(num_bodies):
            distance = bodies[j].position - bodies[i].position
            distance_list[i, j, 0] = distance[0]
            distance_list[i, j, 1] = distance[1]
            distance_list[i, j, 2] = distance[2]

    # computing gravitational force
    cdef double dist_mag, force
    for i in range(num_bodies):
        for j in range(num_bodies):
            dist_mag = magnitude(distance_list[i, j])
            if dist_mag != 0:
                unit_vec = unit_vector(distance_list[i, j])
                force = 6.67e-11 * bodies[i].mass * bodies[j].mass / dist_mag**2
                force_list[i, j, 0] = force * unit_vec[0]
                force_list[i, j, 1] = force * unit_vec[1]
                force_list[i, j, 2] = force * unit_vec[2]

    # computing net force
    for i in range(num_bodies):
        net_force[i, 0] = np.sum(force_list[i, :, 0])
        net_force[i, 1] = np.sum(force_list[i, :, 1])
        net_force[i, 2] = np.sum(force_list[i, :, 2])

    return net_force.tolist()

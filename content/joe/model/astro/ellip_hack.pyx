from scipy.special.cython_special cimport ellipe, ellipk

cdef api double c_ellipe(double m):
     return ellipe(m)

cdef api double c_ellipk(double m):
     return ellipk(m)
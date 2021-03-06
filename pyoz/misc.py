import warnings

try:
    from numba import jit
except ImportError:
    def jit(*args, **kwargs):
        """Dummy decorator that does nothing. """
        def true_decorator(f):
            return f
        return true_decorator
    warnings.warn('Unable to import `numba`. Installing `numba` will '
                  'significantly accelerate your code:\n\n'
                  '"conda install numba"\n\n')
import numpy as np

from pyoz.exceptions import PyozError


def rms_normed(A, B):
    """Compute the squared and normed distance between two arrays.

    distance = sqrt(sum[(A - B)^2] / (n_pts * n_components^2))
    """
    distance = ((A - B)**2).sum() / A.shape[2] * A.shape[0]**2
    return np.sqrt(distance)


@jit(nopython=True)
def solver(A, B):
    """Solve the matrix problem in fourier space. """
    n_components = A.shape[0]
    n_points = A.shape[-1]

    if n_components == 1:
        if (A == 0).any():
            raise PyozError('Singular matrix, cannot invert')
        H_k = B / A
    elif n_components == 2:
        H_k = np.empty_like(A)
        A_det = A[0, 0] * A[1, 1] - A[1, 0] * A[0, 1]
        if (A_det == 0.0).any():
            raise PyozError('Singular matrix, cannot invert')

        for dr in range(n_points):
            A_inv = np.ones(shape=(2, 2,)) / A_det[dr]
            A_inv[0, 0] *= A[1, 1, dr]
            A_inv[0, 1] *= -A[0, 1, dr]
            A_inv[1, 0] *= -A[1, 0, dr]
            A_inv[1, 1] *= A[0, 0, dr]

            # h[:,:,dr] = (mat(a_inv[dr]) * mat(b[:,:,dr])) / dens_factor
            # explicitly - is faster
            H_k[0, 0, dr] = A_inv[0, 0]*B[0, 0, dr] + A_inv[0, 1]*B[1, 0, dr]
            H_k[0, 1, dr] = A_inv[0, 0]*B[0, 1, dr] + A_inv[0, 1]*B[1, 1, dr]
            H_k[1, 0, dr] = A_inv[1, 0]*B[0, 0, dr] + A_inv[1, 1]*B[1, 0, dr]
            H_k[1, 1, dr] = A_inv[1, 0]*B[0, 1, dr] + A_inv[1, 1]*B[1, 1, dr]
    elif A.shape[0] >= 2:
        H_k = np.empty_like(A)
        for dr in range(n_points):
            H_k[:, :, dr] = np.linalg.solve(A[:, :, dr], B[:, :, dr])
    return H_k


def picard_iteration(e_r, e_r_previous, mix):
    return (1 - mix) * e_r_previous + mix * e_r


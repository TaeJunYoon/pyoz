import numpy as np


__all__ = ['mie', 'lennard_jones', 'wca', 'coulomb', 'screened_coulomb', 'dpd',
           'soft_depletion', 'hard_sphere', 'square_well']


def arithmetic(a, b):
    return 0.5 * (a + b)


def geometric(a, b):
    return np.sqrt(a * b)


def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def mie(r, eps, sig, m, n):
    prefactor = (m / (m - n)) * (m / n)**(n / (m - n))
    return prefactor * eps * ((sig / r)**m - (sig / r)**n)


def lennard_jones(r, eps, sig):
    return mie(r, eps, sig, m=12, n=6)


def wca(r, eps, sig, m, n):
    p = 1 / (m - n)
    r_cut = sig * (m / n)**p
    U = lennard_jones(r, eps, sig) + eps
    return np.where(r < r_cut, U, 0)


def coulomb(r, q1, q2, bjerrum_length=1):
    return bjerrum_length * q1 * q2 / r


def screened_coulomb(r, q1, q2, bjerrum_length=1, debye_length=1):
    return coulomb(r, q1, q2, bjerrum_length) * np.exp(-r / debye_length)


def soft_depletion(r, eps, sig_c, sig_d, n, rho_d):
    """
    References
    ----------
    ..[1] "How soft repulsions enhance the depletion mechanism", Rovigatti, Gnan,
    Parola, Zaccarelli: Soft Matter 2015, Equation 2
    
    """
    sig_cd = (sig_c + sig_d) / 2

    y = r - 2 * sig_cd
    q = sig_d / sig_c
    a = 2 * n * q / (1 + q)

    A = 3 / a**2 * sig_cd**2 + 4 / a**3 * sig_cd - 5 / a**4
    B = 4/a**3 - 2/a*sig_cd**2
    C = sig_cd**2 / 2 - sig_cd / a - 1 / a**2

    Bp = sig_cd**2 / a + 4 / a**2 * sig_cd - 1 / a**3
    Cp = sig_cd / a + 1 / (2 * a**2)

    Q1 = A + B * y + C * y**2 + sig_cd / 3 * y**3 + y**4 / 24
    Q2 = A + Bp * y + Cp * y**2 + y**3 / (6 * a)

    depl_short = -2 * np.pi * rho_d / r * Q1
    depl_long = -2 * np.pi * rho_d / r * Q2 * np.exp(-a * r)
    depl = np.where(r < 2 * sig_cd, depl_short, depl_long)

    rep = eps * (sig_c / r)**n
    return rep + depl


def dpd(r, a):
    cutoff = np.abs(r - 1.0).argmin()
    U = np.zeros_like(r)
    U[:cutoff] = 0.5 * a * (1 - r[:cutoff])**2
    return U


def hard_sphere(r, d):
    U = np.zeros_like(r)
    idx, _ = find_nearest(r, d/2)
    U[:idx] = np.inf
    return U


def square_well(r, d, da, e):
    U = np.zeros_like(r)
    d_idx, _ = find_nearest(r, d/2)
    U[:d_idx] = np.inf

    da_idx, _ = find_nearest(r, da/2)
    U[d_idx:da_idx] = -e
    return U

import numpy as np


def hypernetted_chain(U_r, e_r, U_r_erf_real, kT, **kwargs):
    """Apply the hyper-netted chains closure.

    g_r = exp(-U) * exp(e_r)
    h_r = g_r - 1
    c_r = exp(-U) * exp(e_r) - e_r - 1

    """
    # c_r = np.exp(-U_r + U_r_erf_real + e_r) - e_r - 1
    c_r = np.exp(-U_r / kT + e_r) - e_r - 1
    # c_r = np.exp(-U_r + e_r) - e_r - 1
    return c_r


def reference_hypernetted_chain(U_r, e_r, U_r_erf_real, kT, **kwargs):
    """Apply the hyper-netted chains closure.

    g_r = exp(-U) * exp(e_r)
    h_r = g_r - 1
    c_r = exp(-U) * exp(e_r) - e_r - 1

    """
    # TODO: Add Ng-normalization
    g_r_ref, e_r_ref, U_r_ref = kwargs['g_r_ref'], kwargs['e_r_ref'], kwargs['U_r_ref']
    dU = U_r - U_r_ref
    dG = e_r - e_r_ref
    c_r = g_r_ref * np.exp(-dU / kT + dG) - e_r - 1
    # g_r = c_r + e_r + 1
    return c_r


def percus_yevick(U_r, e_r, U_r_erf_real, **kwargs):
    """Apply the Percus-Yevick closure.

    g_r = exp(-U) * (1 + e_r)
    h_r = g_r - 1
    c_r = exp(-U) * (1 + e_r) - e_r - 1

    """
    g_r = np.exp(-U_r) * np.exp(U_r_erf_real) * (1 + e_r)
    c_r = g_r - e_r - 1
    return c_r


def kovalenko_hirata(U_r, e_r, U_r_erf_real, **kwargs):
    g_r_py = np.exp(-U_r) * np.exp(U_r_erf_real) * (1 + e_r)
    g_r_hnc = np.exp(-U_r + U_r_erf_real + e_r)
    g_r = np.where(g_r_hnc < 1)
    c_r = g_r - e_r - 1
    return


def partial_series_expansion_n():
    pass


def duh_henderson():
    "An effective-colloid pair potential for Lennard-Jones colloid–polymer mixtures Orlando Guzmán and Juan J. de Pablo "
    pass

supported_closures = {'HNC': hypernetted_chain,
                      'RHNC': reference_hypernetted_chain,
                      'PY': percus_yevick}

import numpy as np


def hypernetted_chain(U_r, e_r, kT, **kwargs):
    """Apply the hyper-netted chains closure.

    g_r = exp(-U) * exp(e_r)
    c_r = exp(-U) * exp(e_r) - e_r - 1

    """
    c_r = np.exp(-U_r / kT + e_r) - e_r - 1
    return c_r


def reference_hypernetted_chain(U_r, e_r, kT, **kwargs):
    """Apply the hyper-netted chains closure.

    g_r = exp(-U) * exp(e_r)
    c_r = exp(-U) * exp(e_r) - e_r - 1

    """
    ref_system = kwargs['reference_system']
    g_r_ref = ref_system.g_r
    e_r_ref = ref_system.e_r
    U_r_ref = ref_system.U_r

    dU = U_r - U_r_ref
    dG = e_r - e_r_ref
    c_r = g_r_ref * np.exp(-dU / kT + dG) - e_r - 1
    return c_r


def percus_yevick(U_r, e_r, kT, **kwargs):
    """Apply the Percus-Yevick closure.

    g_r = exp(-U) * (1 + e_r)
    c_r = exp(-U) * (1 + e_r) - e_r - 1

    """
    c_r = np.exp(-U_r / kT) * (1 + e_r) - e_r - 1
    return c_r

supported_closures = {'hnc': hypernetted_chain,
                      'hypernetted chain': hypernetted_chain,
                      'hyper-netted chain': hypernetted_chain,
                      'hypernetted-chain': hypernetted_chain,

                      'rhnc': reference_hypernetted_chain,
                      'reference hypernetted chain': reference_hypernetted_chain,
                      'reference hyper-netted chain': reference_hypernetted_chain,
                      'reference hypernetted-chain': reference_hypernetted_chain,

                      'py': percus_yevick,
                      'percus yevick': percus_yevick,
                      'percus-yevick': percus_yevick}
closure_names = supported_closures.keys()


# Currently unimplemented closures on the wishlist.
def kovalenko_hirata(U_r, e_r, kT,  **kwargs):
    pass


def partial_series_expansion_n(U_r, e_r, kT,  **kwargs):
    pass


def duh_henderson(U_r, e_r, kT,  **kwargs):
    """See: An effective-colloid pair potential for Lennard-Jones
    colloid–polymer mixtures Orlando Guzmán and Juan J. de Pablo """
    pass


def scoza(U_r, e_r, kT,  **kwargs):
    pass


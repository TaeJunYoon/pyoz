"""
Module defining functions for interaction potential handling

"""

import itertools as it

import numpy as np
import simtk.unit as u


def arithmetic(a, b):
    return 0.5 * (a + b)


def geometric(a, b):
    return np.sqrt(a * b)

mixing_functions = {'arithmetic': arithmetic,
                    'geometric': geometric}


class Potential(object):
    """Calculate the total U_ij potential.

    Also stores:
    * individual potentials which sum to the total interaction
    * discontinuities of the individual potentials

    Currently supported potentials:
    * lennard-jones

    Parameters
    ----------
    r : np.ndarray, shape=(n_points,), dtype=float
    n_components : int
    potentials : dict

    Attributes
    ----------
    ij : np.ndarray, shape=(n_comps, n_comps, n_points), dtype=float
        The total U_ij potential.
    ij_ind : np.ndarray, shape=(n_pots, n_comps, n_comps, n_points), dtype=float
        The individual contributions to the total potential.

    """
    def __init__(self, r, n_components, potentials):
        n_potentials = len(potentials)
        self.ij = np.zeros(shape=(n_components, n_components, r.shape[0]))
        self.ij_ind = np.zeros(shape=(n_potentials, n_components, n_components, r.shape[0]))

        self.erf_ij_real = np.zeros(shape=(n_components, n_components, r.shape[0]))
        self.erf_ij_fourier = np.zeros(shape=(n_components, n_components, r.shape[0]))

        for n, (pot_type, pot_parms) in enumerate(potentials.items()):
            # TODO: Factor out individual potential classes
            if pot_type == 'lennard-jones':
                sigma = pot_parms['sigmas']
                epsilon = pot_parms['epsilons']
                sigma_ij = np.zeros(shape=(n_components, n_components))
                epsilon_ij = np.zeros(shape=(n_components, n_components))

                mix_sigma = mixing_functions[pot_parms['sigma_rule']]
                mix_epsilon = mixing_functions[pot_parms['epsilon_rule']]
                for i, j in it.product(range(n_components), range(n_components)):
                    s = mix_sigma(sigma[i], sigma[j]).value_in_unit(u.angstroms)
                    e = mix_epsilon(epsilon[i], epsilon[j])
                    sigma_ij[i, j] = s
                    epsilon_ij[i, j] = e
                    u_ij = 4 * e * ((s / r)**12 - (s / r)**6)
                    self.ij_ind[n, i, j, :] = u_ij
                    self.ij[i, j, :] += u_ij  # TODO: Should be np.summable

                pot_parms['sigma_ij'] = sigma_ij
                pot_parms['epsilon_ij'] = epsilon_ij
            else:
                raise ValueError("Unsupported potential: {}".format(pot_type))


class ModMayerF(object):
    def __init__(self, U):
        """calculate exp(-beta U_ij) == Mayer function + 1 according to the discretized potential

           calculate also the contributions of individual potentials to exp(Uij)
           exp(-Uij)=exp(-U1ij-U2ij-U3ij-...)=exp(-U1ij)exp(-U2ij)exp(-U3ij)...
           the order of contributions is the same as the order of potentials in the parm list
           store the contributions in a list; they will be used later (osmotic coefficients)
        """
        # since the potential is in kT units, we just do the exp(-U_ij)
        self.ij = np.exp(-U.ij)
        self.ij_ind = np.exp(-U.ij_ind)

        # evaluate the correction according to Ng
        self.erf_real = np.exp(U.erf_ij_real)
        self.erf_fourier = np.exp(U.erf_ij_fourier)


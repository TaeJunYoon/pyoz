import numpy as np
from scipy.integrate import simps as integrate


def kirkwood_buff_integrals(system):
    """Compute the Kirkwood-Buff integrals.

    G_ij = 4 pi \int_0^\inf [g(r)-1]r^2 dr
    """
    r, g_r = system.r, system.g_r
    return 4.0 * np.pi * integrate.simps(y=(g_r - 1.0) * r**2,
                                         x=r,
                                         even='last')


# TODO: double check kT
def excess_chemical_potential(system):
    """Compute the excess chemical potentials.

    \beta mu_i^{ex} = \sum_i 4 \pi \rho_i  *
                            \int [ h(r) \Gamma(r) / 2 - c^s(r) ] r^2 dr

    Currently only the HNC approximation is supported.

    """
    r, h_r, G_r, cs_r = system.r, system.h_r, system.G_r, system.cs_r

    mu_ex = np.empty(shape=system.n_components)
    for i in range(r.shape[0]):
        mu = 0.0
        for j in range(r.shape[0]):
            rho_j = system.components[j].concentration
            integrand = 0.5 * h_r[i, j] * G_r[i, j] - cs_r[i, j]
            mu += 4.0 * np.pi * rho_j * integrate(y=integrand * r**2,
                                                  x=r,
                                                  even='last')
        mu_ex[i] = mu
    return mu_ex


def activity_coefficient(system):
    """Compute the activity coefficients.

    \gamma_i = exp(\beta \mu^ex)

    """
    # TODO: add mean activity calculation for charged system
    mu_ex = excess_chemical_potential(system)
    return np.exp(mu_ex)


def excess_internal_energy(system):
    """ """
    r, g_r, U_ij = system.r, system.g_r, system.U.ij
    U_ex = 2 * np.pi * rho * integrate(y=g_r * U_ij * r**2,
                                       x=r,
                                       even='last')
    return U_ex


def compressibility(ctrl, syst, const, r, c_sr):
    """
      calculates isothermal compressibility and excess isothermal compressibility
    """

    if (syst['dens']['totnum'] == 0.0):
        # infinite dilution
        chi_ex = 1.0
        chi_ex_r = 1.0
        chi = np.inf
        chi_r = 0.0
        chi_id = np.inf
        chi_id_r = 0.0
    else:
        # calculate the prefactor 4 pi / rho
        prefactor = 4.0 * np.pi / syst['dens']['totnum']
        # reciprocal of the excess compressibility
        # initialize to 1
        chi_ex_r = 1.0
        chi_id = 1.0e-7 / (const.kT * syst['dens']['totnum'])
        chi_id_r = 1.0e7 * const.kT * syst['dens']['totnum']
        # perform the calculation
        # chi_ex_r = 1 - 1/\rho \sum_i \sum_j \rho_i \rho_j \int c_sr 4 \pi r^2 dr
        # 4 \pi / \rho is in the prefactor
        # integrate numerically using simpson rule
        # we could use x = r and skip dx, but the spacing is regular so it's probably better to do it this way
        # simspon requires odd number of samples, what we have; just to be sure, we give the option for the
        # even number of samples - for the first interval the trapezoidal rule is used and then simpson for the rest
        for i in range(syst['ncomponents']):
            for j in range(syst['ncomponents']):
                contrib = prefactor * syst['dens']['num'][i] * \
                          syst['dens']['num'][j] * integrate.simps(
                    c_sr[i, j] * r ** 2, r, dx=ctrl['deltar'], even='last')
                chi_ex_r -= contrib
                # print i,j,contrib

        chi_ex = 1.0 / chi_ex_r

        # 1/chi_ex = chi_id/chi; chi_id = 1/\rho kT
        # chi = chi_id chi_ex
        # 1/chi = 1/(chi_ex * chi_id)
        chi = chi_ex * chi_id
        chi_r = chi_id_r / chi_ex
    # end if (syst['dens']['totnum'] == 0.0)

    print("\tisothermal compressibility (using sr-c(r))")
    print("\t\texcess chi, chi^(-1)\t%f    %f" % (chi_ex, chi_ex_r))
    print("\t\tideal chi, chi^(-1)\t%.5e %f" % (chi_id, chi_id_r))
    print("\t\tabsolute, chi, chi^(-1)\t%.5e %f" % (chi, chi_r))
    print("")

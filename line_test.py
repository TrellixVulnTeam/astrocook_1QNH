from astrocook import *
from astropy import units as u
import matplotlib.pyplot as plt

xunit = u.nm
yunit = u.erg / (u.Angstrom * u.cm**2 * u.s)

def main():

    # Input data
    name = 'J0940_Lya'  # Single Lya line complex
    #name = 'J0940_CIV_1'  # The CIV doublet will be blindly fitted as Ly_a
    #name = 'J0940_Lya_forest_1'  # Whole chunk of Lya forest (time consuming)
    #name = 'J0940_Lya_forest_1'  # Another chunk of Lya forest (time consuming)
    
    # Read the 1D spectrum
    spec = Spec1DReader().uves(name + '_spec.fits')

    # Create a Line object from the spectrum
    line = Line(spec)

    # Find absorption lines in the spectrum
    line.find(kappa=5.0)

    ltot = len(line.t)
    for l in range(ltot):
        print("Line %i of %i..." % (l + 1, ltot), end=" ", flush=True)
    
        # Define the line group around a given wavelength
        group = line.group(line=l)
    
        # Define the spectral chunk around a given wavelength
        chunk = line.chunk(line=l)

        # Guess the unabsorbed continuum
        unabs_guess = line.unabs(group, chunk)

        # Guess the Voigt profile
        voigt_guess = line.voigt(group, chunk)

        # Fit the unabsorbed continuum and the voigt profile
        fit = line.fit(group, chunk, unabs_guess, voigt_guess)
    
        # Plot lines
        print("close graph to continue.")
        line.plot(group, chunk)


if __name__ == '__main__':
    main()

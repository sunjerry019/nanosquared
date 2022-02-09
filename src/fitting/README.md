# Fitting for M²
```
Fitter ┬─> ODRFitter (scipy.odr):                optimizes x and y-error
       ├─> OCFFitter (scipy.optimize.curve_fit): optimizes y-error
       │
    ┌──┴───> MsqODRFitter / MsqOCFFitter: Provides all functionalities
    │                                     and fitting using the selected 
    │                                     fitting method
    │
MsqFitter: Provides functionalities common to all fitting methods
```

On top of the 2 fitting methods there are 3 fitting modes to fit for M²:
1. **M²λ mode**.
In this mode, the function that is fitted combines the M²λ term as these 2 are heavily correlated (this means that that M² and λ cannot be fitted individually as fit parameters). Using Gaussian error propagation methods, the error in the wavelength can then be taken into account. The fit equation is: <p align="center"><img src="https://latex.codecogs.com/svg.image?\bg_white&space;\omega(z)&space;=&space;\omega_0&space;\sqrt{1&space;&plus;&space;(z&space;-&space;z_0)^2\left(\frac{\tilde{M}}{\pi\omega_0^2}\right)^2}" title="\bg_white \omega(z) = \omega_0 \sqrt{1 + (z - z_0)^2\left(\frac{\tilde{M}}{\pi\omega_0^2}\right)^2}" /></p> where <img src="https://latex.codecogs.com/svg.image?\bg_white&space;\tilde{M}&space;=&space;M^2\lambda" title="\bg_white \tilde{M} = M^2\lambda" />.

2. **M² mode**. 
In this mode, a temporary function is created from the original beam equation with the wavelength hard-coded. The data is then fitted to this temporary function. This allows M² to be fitted directly as a fit-parameter. Due to the hard-coded nature of the wavelength, the error in the wavelength cannot be taken into account. The fit equation is: 
<p align="center"><img src="https://latex.codecogs.com/svg.image?\bg_white&space;\omega(z)&space;=&space;\omega_0&space;\sqrt{1&space;&plus;&space;(z&space;-&space;z_0)^2\left(\frac{M^2\lambda}{\pi\omega_0^2}\right)^2}" title="\bg_white \omega(z) = \omega_0 \sqrt{1 + (z - z_0)^2\left(\frac{M^2\lambda}{\pi\omega_0^2}\right)^2}" /></p>

3. **ISO mode**.
In this mode, the fit is done according to the method described in ISO 11146-1:2021 Section 9, and Gaussian error propagation is used to find the error of M². Here we assume that the beam is either stigmatic or simple astigmatic. This method somehow creates really big errors with the data that I have tested on. The fit-equation is: <p align="center"><img src="https://latex.codecogs.com/svg.image?\bg_white&space;\frac{1}{2}\sqrt{a&space;&plus;&space;bz&space;&plus;&space;cz^2}" title="\bg_white \frac{1}{2}\sqrt{a + bz + cz^2}" /></p>
_**Note**_: the ISO standard says that "It is common to perform the fit by minimizing the sum of the squared relative deviations of the diameters." → i.e. only y-error is minimized. 

In the program, the modes are 0-indexed (i.e. Mode 0 is M²λ, etc.). Constants are provided in the class `MsqFitter` that map to each of these modes.

Under [`/tests/`](../../tests) there are parallelized code that runs on the LMU Physics CIP Pool Cluster for parameter-sweep purposes. These jobs are to be sent using the command:
```bash
sbatch slurm_proc.sh
```
In the script, it is important to not use `srun`, as this launches the same script in all the available nodes. Since we are using `mpi` here, we should ask `mpi` to do the distribution to ensure communication.

Outstanding matters:
1. Does the ISO fitting use d4σ-diameter or the d2√2σ-diameter? (Ref: BS EN ISO 11145:2018 or equivalent -- Beam Diameter vs Beam Width)
2. Adding a function to obtain the z_0 and w_0 from the fitted parameters depending on the mode.
3. Testing the ISO Method on more data and compare between all the methods. 
4. Adding a flag to allow for small variation to the start parameters should the fit not converge. In this case, the function `.fit()` should not return until the fit has converged.
5. Ensure that the d4σ determination has background removed to increase its accuracy.

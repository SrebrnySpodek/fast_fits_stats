# fast_fits_stats
Script for star detection for FITS files, and basic statistics calculation.  

## Usage CLI:
`find_stars.py <fits_path> [options]` - cli 

## Arguments:
- `<fits_path>` - Required. The path to the FITS file.

## Options:
   - `gain=<float>`            Detector gain value. Used for noise estimation. Defaults to 1.
   - `rn_noise=<float>`        Detector readout noise. Used for noise estimation. Defaults to 0.
   - `threshold=<float>`       The threshold value for star detection. Defaults to 5. Really, should't be smaller than 3!!!
   - `fwhm=<float>`            FWHM value. Defaults to 2.
   - `kernel_size=<int>`      The size of the Gaussian kernel. Defaults to 9.
   - `method=<str>`         The method used for determining the sigma value. Can be 'rms Poisson','rms','sigma quantile'. Defaults to "sigma quantile".
   - `saturation=<float>`      Saturation level above fwhm calculation will be ignored for a star. Defaults to 65000
   - `radius=<int>`            Radius in which fwhm will be calculated. Defaults to 10
   - `all_stars=<bool>`        If True, fwhm will be calculated for all stars. 
                               If False, only for 100 non saturated brightests. Defaults to False



## Returns: 
  - `Basic statistics` 
  - `.ffs file` - in the directory of <fits_path>, with stars coordinates and coresponding ADU

## Example usage: 
   ``` # ./find_stars.py ./DATA/zb08c_0014_43387.fits threshold=2 kernel_size=15 fwhm=10 ```

# Usage PACKAGE
 `FFS` (Fast Fits Statistics) library for star detection in an image, and basic statistics. 

## Args:
- `image` (numpy.ndarray): The input image.
- `gain` (float, optional): Detector gain value. Used for noise estimation. Defaults to 1.
- `rn_noise` (float, optional): Detector readout noise. Used for noise estimation. Defaults to 0.

## Attributes:
- `all Args`
- `min` (float): The minimum value of the ADU.
- `max` (float): The maximum value of the ADU.
- `mean` (float): The mean value of the ADU.
- `median` (float): The median value of the ADU.
- `rms` (float): The root mean square value of the ADU.
- `sigma_quantile` (float): The sigma value calculated as the quantile 0.5 - 0.159 .
- `noise` (float): The noise calculated as the Poisson noise accounting gain and readout noise.

## Methods:
### find_stars
`find_stars(self,threshold=5.,method="sigma quantile",kernel_size=9,fwhm=2)`: Finds the stars in the image with specified noise calulation method.

#### Args:
- `threshold` (float, optional): The threshold value for star detection. Defaults to 5.
- `method` (str, optional): The method used for determining the sigma value. Can be 'rms Poisson','rms','sigma quantile'. Defaults to "sigma quantile".
- `kernel_size` (int, optional): The size of the Gaussian kernel. Defaults to 9.
- `fwhm` (float, optional): FWHM value. Defaults to 2.

#### Returns:
- `coo` (numpy.ndarray): An sorted array of coordinates representing the positions of stars.
- `adu` (numpy.ndarray): An sorted array of ADU values corresponding to the detected stars.

### fwhm
`fwhm(self,saturation=65000,radius=10,all_stars=False)`: Calculates the average fwhm for stars in the X and Y axis.

#### Args:
- `saturation` (float): Saturation level above fwhm calculation will be ignored for a star. Defaults to 65000
- `radius` (int): Radius in which fwhm will be calculated. Defaults to 10
- `all_stars` (bool): If True, fwhm will be calculated for all stars. 
                      If False, only for 100 non saturated brightests. Defaults to False

#### Returns: 
- `fwhm_x,fwhm_y` (float,float): Median of fwhm for X and Y axis, respectively

#### Attributes:
- `fwhm_xarr` (numpy.ndarray): array of fwhm in X axis for stars, ordered accordingly to star ADU
- `fwhm_yarr` (numpy.ndarray): array of fwhm in Y axis for stars, ordered accordingly to star ADU


## Example usage:
```
stats = FFS(data,threshold=5,kernel_size=9,fwhm=6)
sigma = stats.sigma_quantile
p_noise = stats.noise
coo,adu = stats.find_stars()
fwhm_x,fwhm_u = stats.fwhm(saturation=50000,all_stars=True)
fwhm_xarr = stats.fwhm_xarr
fwhm_yarr = stats.fwhm_yarr
```

# fast_fits_stats
Script for star detection for a FITS files, and basic statistics calculation.  

### Usage CLI:
`find_stars.py <fits_path> [options]` - cli 

### Arguments:
- `<fits_path>` - Required. The path to the FITS file.

### Options:
   - `threshold=<value>`       The threshold value for star detection. Defaults to 5. Really, should't be smaller than 3!!!
   - `fwhm=<value>`            FWHM value. Defaults to 2.
   - `kernel_size=<size>`      The size of the Gaussian kernel. Defaults to 9.
   - `method=<method>`         The method used for determining the sigma value. Can be 'rms Poisson','rms','sigma quantile'. Defaults to "sigma quantile".
   - `gain=<value>`            Detector gain value. Used for noise estimation. Defaults to 1.
   - `rn_noise=<value>`        Detector readout noise. Used for noise estimation. Defaults to 0.


### Returns: 
  - `Basic statistics` 
  - `.ffs file` - in the directory of <fits_path>, with stars coordinates and coresponding ADU

### Example usage: 
   ``` # ./find_stars.py ./DATA/zb08c_0014_43387.fits threshold=2 kernel_size=15 fwhm=10 ```

## Usage PACKAGE
 `FFS` (Fast Fits Statistics) library for star detection in an image, and basic statistics. 

### Args:
- `image` (numpy.ndarray): The input image.
- `threshold` (float, optional): The threshold value for star detection. Defaults to 5.
- `gain` (float, optional): Detector gain value. Used for noise estimation. Defaults to 1.
- `rn_noise` (float, optional): Detector readout noise. Used for noise estimation. Defaults to 0.
- `method` (str, optional): The method used for determining the sigma value. Can be 'rms Poisson','rms','sigma quantile'. Defaults to "sigma quantile".
- `kernel_size` (int, optional): The size of the Gaussian kernel. Defaults to 9.
- `fwhm` (float, optional): FWHM value. Defaults to 2.

### Attributes:
- `all Args`
- `min` (float): The minimum value of the ADU.
- `max` (float): The maximum value of the ADU.
- `mean` (float): The mean value of the ADU.
- `median` (float): The median value of the ADU.
- `rms` (float): The root mean square value of the ADU.
- `sigma_quantile` (float): The sigma value calculated as the quantile 0.5 - 0.159 .
- `noise` (float): The noise calculated as the Poisson noise accounting gain and readout noise.

### Methods:
`find_stars()`: Finds the stars in the image with specified noise calulation method.
    
#### Returns:
- `coo` (numpy.ndarray): An sorted array of coordinates representing the positions of stars.
- `adu` (numpy.ndarray): An sorted array of ADU values corresponding to the detected stars.

### Example usage:
```
stats = FFS(data,threshold=5,kernel_size=9,fwhm=6)
sigma = stats.sigma_quantile
p_noise = stats.noise
coo,adu = stats.find_stars()
```

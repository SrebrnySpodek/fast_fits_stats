#!/usr/bin/env python3


import sys,os, time
from astropy.io import fits
from ffs_lib.ffs import FFS 


"""A script for star detection for a FITS files, and basic statistics calculation.  

Usage:
    find_stars.py <fits_path> [options]

Arguments:
    <fits_path>      Required. The path to the FITS file.

Options:
    gain=<float>            Detector gain value. Used for noise estimation. Defaults to 1.
    rn_noise=<float>        Detector readout noise. Used for noise estimation. Defaults to 0.
    threshold=<float>       The threshold value for star detection. Defaults to 5. Really, should't be smaller than 3!!!
    fwhm=<float>            FWHM value. Defaults to 2.
    kernel_size=<int>       The size of the Gaussian kernel. Defaults to 9.
    method=<str>            The method used for determining the sigma value. Can be 'rms Poisson','rms','sigma quantile'. Defaults to "sigma quantile".
    saturation=<float>      Saturation level above fwhm calculation will be ignored for a star. Defaults to 65000
    radius=<int>:           Radius in which fwhm will be calculated. Defaults to 10
    all_stars=<bool>:       If True, fwhm will be calculated for all stars. 
                            If False, only for 100 non saturated brightests. Defaults to True


Returns: Basic statistics and .ffs file (in the directory of <fits_path>) with stars coordinates and coresponding ADU and fwhm in X and Y

Example usage: 
    ./find_stars.py ./DATA/zb08c_0014_43387.fits threshold=2 kernel_size=15 fwhm=10 saturation=40000


"""  


def main():
    kwargs = {}
    args = []
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = value
        else:
            path = arg   
    ok = False
    try:
        hdu=fits.open(path)
        data = hdu[0].data
        ok = True
    except FileNotFoundError: 
        print(f"File {path} not found")
    except OSError: 
        print(f"File {path} is not a valid FITS file")
        
    if ok:
        FFF_kwargs = {key: kwargs[key] for key in ["gain","rn_noise"] if key in kwargs}
        stats = FFS(data,**FFF_kwargs)
        fs_kwargs = {key: kwargs[key] for key in ["threshold","method","kernel_size","fwhm"] if key in kwargs}
        coo,adu = stats.find_stars(**fs_kwargs)
        fwhm_kwargs = {key: kwargs[key] for key in ["saturation","radius","all_stars"] if key in kwargs}
        fwhm = stats.fwhm(**fwhm_kwargs)
    
        txt = f"stars no.: {len(coo)}\n"
        txt = txt + f"fwhm X: {stats.fwhm_x:.2f}\n"
        txt = txt + f"fwhm Y: {stats.fwhm_y:.2f}\n"
        txt = txt + f"min ADU: {stats.min}\n"
        txt = txt + f"max ADU: {stats.max}\n"
        txt = txt + f"mean: {stats.mean}\n"
        txt = txt + f"median: {stats.median}\n"
        txt = txt + f"rms: {stats.rms}\n"
        txt = txt + f"q(0.5)-q(0.159): {stats.sigma_quantile}\n"
        txt = txt + f"Poisson noise: {stats.noise}\n"
        print(txt)

        txt = f"# stars no.: {len(coo)}\n"
        txt = txt + f"# fwhm X: {stats.fwhm_x}\n"
        txt = txt + f"# fwhm Y: {stats.fwhm_y}\n"        
        txt = txt + f"# min ADU: {stats.min}\n"
        txt = txt + f"# max ADU: {stats.max}\n"
        txt = txt + f"# mean: {stats.mean}\n"
        txt = txt + f"# median: {stats.median}\n"
        txt = txt + f"# rms: {stats.rms}\n"
        txt = txt + f"# q(0.5)-q(0.159): {stats.sigma_quantile}\n"
        txt = txt + f"# Poisson noise: {stats.noise}\n"
        txt = txt + f"# x_coo    y_coo    adu_xy\n\n"
        
        txt="# x_cco  y_coo  ADU  fwhm_x  fwhm_y\n"
        for i,tmp in enumerate(coo):
          txt = txt +str(int(coo[i][0])).ljust(7)+" "+str(int(coo[i][1])).ljust(7) +" "+ str(adu[i]).ljust(7)
          txt = txt +f" {float(stats.fwhm_xarr[i]):.2f}".ljust(7) + " " + f"{float(stats.fwhm_yarr[i]):.2f}".ljust(7) + "\n"
        with open(path.replace(".fits", ".ffs"), mode='w') as plik: plik.write(txt)

if __name__ == "__main__":
    main()












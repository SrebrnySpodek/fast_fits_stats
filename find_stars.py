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
    threshold=<value>       The threshold value for star detection. Defaults to 5. Really, should't be smaller than 3!!!
    fwhm=<value>            FWHM value. Defaults to 2.
    kernel_size=<size>      The size of the Gaussian kernel. Defaults to 9.
    method=<method>         The method used for determining the sigma value. Can be 'rms Poisson','rms','sigma quantile'. Defaults to "sigma quantile".
    gain=<value>            Detector gain value. Used for noise estimation. Defaults to 1.
    rn_noise=<value>        Detector readout noise. Used for noise estimation. Defaults to 0.


Returns: Basic statistics and .ffs file (in the directory of <fits_path>) with stars coordinates and coresponding ADU

Example usage: 
    ./find_stars.py ./DATA/zb08c_0014_43387.fits threshold=2 kernel_size=15 fwhm=10


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
        stats = FFS(data,**kwargs)
        coo,adu = stats.find_stars()
    
        txt = f"stars no.: {len(coo)}\n"
        txt = txt + f"min ADU: {stats.min}\n"
        txt = txt + f"max ADU: {stats.max}\n"
        txt = txt + f"mean: {stats.mean}\n"
        txt = txt + f"median: {stats.median}\n"
        txt = txt + f"rms: {stats.rms}\n"
        txt = txt + f"q(0.5)-q(0.159): {stats.sigma_quantile}\n"
        txt = txt + f"Poisson noise: {stats.noise}\n"
        print(txt)

        txt = f"# stars no.: {len(coo)}\n"
        txt = txt + f"# min ADU: {stats.min}\n"
        txt = txt + f"# max ADU: {stats.max}\n"
        txt = txt + f"# mean: {stats.mean}\n"
        txt = txt + f"# median: {stats.median}\n"
        txt = txt + f"# rms: {stats.rms}\n"
        txt = txt + f"# q(0.5)-q(0.159): {stats.sigma_quantile}\n"
        txt = txt + f"# Poisson noise: {stats.noise}\n"
        txt = txt + f"# x_coo    y_coo    adu_xy\n\n"

        for i,tmp in enumerate(coo):
          txt = txt +str(int(coo[i][0])).ljust(6)+" "+str(int(coo[i][1])).ljust(6) +" "+ str(adu[i])+"\n"
        with open(path.replace(".fits", ".ffs"), mode='w') as plik: plik.write(txt)

if __name__ == "__main__":
    main()












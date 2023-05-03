#!/usr/bin/env python3


import sys,os
from astropy.io import fits
from ffs_lib.ffs import FFS 


def main():
    kwargs = {}
    args = []
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = value
        else:
            path = arg   
    
    hdu=fits.open(path)
    hdr = data = hdu[0].header 
    data = hdu[0].data

    stats = FFS(data,threshold=5)
    stats.find_stars()
    stats.check_distribution()


    coo = stats.coo 


    print("stars no.: ",len(coo))

    txt="\n \n"
    for cooxy in coo:
      txt = txt + "1 "+str(int(cooxy[0])+1)+" "+str(int(cooxy[1])+1)+"\n"
    with open("result.coo", mode='w') as plik: plik.write(txt)


    hdu2 = fits.PrimaryHDU(data)
    hdu2.header = hdr
    hdu2.writeto('result.fits',overwrite=True)


if __name__ == "__main__":
    main()












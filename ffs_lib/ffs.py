#!/usr/bin/env python3

import numpy
from scipy.signal import convolve2d
from scipy.signal import find_peaks
from scipy.ndimage.filters import maximum_filter

import matplotlib.pyplot as plt

class FFS:

    def __init__(self,image,threshold=10.,gain=1.,rn_noise=0.,method="sigma quantile",kernel_type="3x3 Gauss"):
        self.image = numpy.transpose(image)
        self.threshold = threshold
        self.gain = gain
        self.rn_noise = rn_noise
        self.method = method
        self.kernel_type = kernel_type

        self.min = numpy.min(image)
        self.max = numpy.max(image)
        self.mean = numpy.mean(image)
        self.median = numpy.median(image)
        self.rms = numpy.std(image)
        self.sigma_quantile = numpy.median(image)-numpy.quantile(image, 0.159)
        self.noise = (self.median/self.gain+self.rn_noise)**0.5             

    def find_stars(self):

        if self.kernel_type == "3x3 Gauss":
          self.kernel = [
                        [0.077847, 0.123317, 0.077847],
                        [0.123317, 0.195346, 0.123317],
                        [0.077847, 0.123317, 0.077847]
                        ]
        elif self.kernel_type == "5x5 Gauss":
          self.kernel = [
                        [0.003765, 0.015019, 0.023792, 0.015019, 0.003765],
                        [0.015019, 0.059912, 0.094907, 0.059912, 0.015019],
                        [0.023792, 0.094907, 0.150342, 0.094907, 0.023792],
                        [0.015019, 0.059912, 0.094907, 0.059912, 0.015019],
                        [0.003765, 0.015019, 0.023792, 0.015019, 0.003765]
                        ]
        else: raise ValueError(f"Invalid kernel type {self.kernel_type}")   

        if self.method == "rms Poisson":
          self.sigma = self.noise
        elif self.method == "rms":
          self.sigma = self.rms
        elif self.method == "sigma quantile":
          self.sigma = self.sigma_quantile
        else: raise ValueError(f"Invalid method type {self.method}") 

        maska1 = self.image > self.median + self.threshold * self.sigma
        data2 = convolve2d(self.image, self.kernel, mode='same')
        maska2 = (data2 == maximum_filter(data2, 3))
        maska = numpy.logical_and(maska1, maska2) 
        coo = numpy.argwhere(maska)
        self.coo = coo
        x,y=zip(*self.coo)
        val = self.image[x,y]
        sorted_i = numpy.argsort(val.astype(float))[::-1]
        sorted_coo = self.coo[sorted_i]
        sorted_val = val[sorted_i]
        self.coo = sorted_coo
        self.adu = sorted_val

    def check_distribution(self):
      xl,yl = zip(*self.coo)
      distances = []
      for i,tmp in self.coo:
        if i < 100:
          x = self.coo[i][0]
          y = self.coo[i][1]
          dx = x - xl
          dy = y - yl
          distances = numpy.append(distances, dx)
          distances = numpy.append(distances, dy)

 
      plt.hist(distances, bins=50)
      plt.show()

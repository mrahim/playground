# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 14:59:11 2014

@author: mehdi
"""

import numpy as np
from scipy import io as spio
from scipy import misc
from scipy import linalg
from scipy import fftpack
from scipy import stats
import pylab as pl

original_image = pl.imread('moonlanding.png')

fft_image = fftpack.fft2(original_image)
fft_magnitude = np.abs(fft_image)

image_center = np.array([ fft_image.shape[0]/2, fft_image.shape[1]/2])

step = 200
fft_image[0:step,0:step]=0


new_image= fftpack.ifft2(fft_image).real

pl.close('all')
pl.figure()
pl.imshow(original_image, cmap='gray')
pl.colorbar()


pl.figure()
pl.imshow(new_image, cmap='gray')
pl.colorbar()


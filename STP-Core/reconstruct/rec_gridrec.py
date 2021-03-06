﻿# #########################################################################
# (C) 2016 Elettra - Sincrotrone Trieste S.C.p.A.. All rights reserved.   #
#                                                                         #
# Copyright 2016. Elettra - Sincrotrone Trieste S.C.p.A. THE COMPANY      #
# ELETTRA - SINCROTRONE TRIESTE S.C.P.A. IS NOT REPONSIBLE FOR THE USE    #
# OF THIS SOFTWARE. If software is modified to produce derivative works,  #
# such modified software should be clearly marked, so as not to confuse   #
# it with the version available from Elettra Sincrotrone Trieste S.C.p.A. #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of Elettra - Sincotrone Trieste S.C.p.A nor      #
#       the names of its contributors may be used to endorse or promote   #
#       products derived from this software without specific prior        #
#       written permission.                                               #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY ELETTRA - SINCROTRONE TRIESTE S.C.P.A. AND #
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,  #
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND       #
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL      #
# ELETTRA - SINCROTRONE TRIESTE S.C.P.A. OR CONTRIBUTORS BE LIABLE FOR    #
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL  #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE       #
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS           #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER    #
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR         #
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF  #
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                              #
# #########################################################################

#
# Author: Francesco Brun
# Last modified: April, 4th 2016
#

from numpy import rot90, float32, copy, linspace 
from scipy.misc import imresize #scipy 0.12

from _gridrec import paralrecon

def recon_gridrec(im1, im2, angles, oversampling):
	"""Reconstruct two sinograms (of the same CT scan) with direct Fourier algorithm.

	Parameters
	----------
	im1 : array_like
		Sinogram image data as numpy array.

	im2 : array_like
		Sinogram image data as numpy array.

	angles : double
		Value in radians representing the number of angles of the input sinogram.

	oversampling : double
		Input sinogram is rescaled to increase the sampling of the Fourier space and
		avoid artifacts. Suggested value in the range [1.2,1.6]. 
	
	"""
	v_angles = linspace(0, angles, im1.shape[0], False).astype(float32)

	# Call C-code for gridrec with oversampling:
	[out1, out2] = paralrecon(im1, im2, v_angles, float(oversampling))  

	# Rescale output (if oversampling used):
	out1 = imresize(out1, (im1.shape[1],im1.shape[1]), interp='bicubic', mode='F')
	out2 = imresize(out2, (im2.shape[1],im2.shape[1]), interp='bicubic', mode='F')

	# Rotate images 90 degrees towards the left:
	out1 = rot90(out1)
	out2 = rot90(out2)

	# Return output:  
	return [out1.astype(float32), out2.astype(float32)]
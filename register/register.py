import numpy as np
from orb.core import HDFCube

class Offset:

    def __init__(self,hdf5_cube_path,ref_image_index=0):

        self.ref_image_index = ref_image_index
        self.hdf5_cube_path = hdf5_cube_path
        self.cube = HDFCube(self.hdf5_cube_path)
        self.ref_image = self.cube[:,:,ref_image_index]
        self.f_ref_image = np.fft.fft2(self.ref_image)


    def compute_fft_offset(self,image_index):

        '''

        :param image_index: index of image in cube to compare to the reference image
        :return: a rough estimate (\pm 1 pixel) of the positional offset between the two images
        '''

        image = self.cube[:,:,image_index]
        fimage = np.fft.fft2(image)

        # Compute phase correlation
        nf2 = (fimage * fimage.conj()).real
        nf1 = (self.f_ref_image * self.f_ref_image.conj()).real

        fcross = self.f_ref_image * fimage.conj() / np.sqrt(nf1 * nf2)
        cross = np.fft.ifft2(fcross)

        imax = np.argmax(cross.real)
        (dx,dy) = np.unravel_index(imax,cross.shape)
        (nx,ny) = cross.shape

        if (dx > nx/2):
            dx -= nx

        if (dy > ny/2):
            dy -= ny

        return cross

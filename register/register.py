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

    def compute_offset_phase(self,(dx,dy)):
        '''
        :param (dx,dy): tuple of offset values (float)
        :return: phase term corresponding to a translation by dx,dy (in pixel units)
        '''

        (nx,ny) = self.f_ref_image.shape
        x_freq = np.fft.fftfreq(nx)
        y_freq = np.fft.fftfreq(ny)
        x_phase = np.exp(-1j * 2*np.pi * dx * x_freq)
        y_phase = np.exp(-1j * 2*np.pi * dy * y_freq)

        return np.outer(x_phase,y_phase)

    def compute_d_offset_phase(self,(dx,dy),(i,j)):
        '''
        :param (dx,dy): tuple of offset values(float)
        :param (i,j): tuple of partial derivative indices
        :return: partial derivative of phase term at reference translation dx,dy
        '''

        phi = self.compute_offset_phase((dx,dy))
        nx,ny = self.f_ref_image.shape
        x_freq = np.fft.fftfreq(nx)
        y_freq = np.fft.fftfreq(ny)
        A = np.diag((1j * 2*np.pi* x_freq)**i)
        B = np.diag((1j * 2*np.pi *y_freq)**j)
        return np.dot(A,np.dot(phi,B))

    def compute_cross(self,fimA,fimB,(dx,dy)):
        '''
        Translated image is the first one
        :param fimA: Translated image 2D Fourier transform
        :param fimB: Reference image 2D Fourier transform
        :return: phase correlation at given offset dx,dy.
                 Should be maximal when dx,dy corresponds to translation.
        '''
        nfa = np.sum(fimA*fimA.conj())
        nfb = np.sum(fimB*fimB.conj())
        phi = self.compute_offset_phase((-dx,-dy))
        return np.sum(fimA*fimB.conj()*phi).real / np.sqrt((nfa*nfb).real)




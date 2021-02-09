import numpy as np
import healpy as hp
import lsst.sims.maf.metrics as metrics

from lsst.sims.photUtils import Sed, Bandpass


class Phot_properties(object):
    """Object to hold handy values mostly calculated in sys-eng throughputs
    """
    def __init__(self, R_v=3.1):
        # Calculate dust extinction values
        waveMins = {'u': 330., 'g': 403., 'r': 552., 'i': 691., 'z': 818., 'y': 950.}
        waveMaxes = {'u': 403., 'g': 552., 'r': 691., 'i': 818., 'z': 922., 'y': 1070.}
        self.Ax1 = {}
        for filtername in waveMins:
            wavelen_min = waveMins[filtername]
            wavelen_max = waveMaxes[filtername]
            testsed = Sed()
            testsed.setFlatSED(wavelen_min=wavelen_min, wavelen_max=wavelen_max, wavelen_step=1.0)
            testbandpass = Bandpass(wavelen_min=wavelen_min, wavelen_max=wavelen_max, wavelen_step=1.0)
            testbandpass.setBandpass(wavelen=testsed.wavelen,
                                     sb=np.ones(len(testsed.wavelen)))
            self.ref_ebv = 1.0
            # Calculate non-dust-extincted magnitude
            flatmag = testsed.calcMag(testbandpass)
            # Add dust
            a, b = testsed.setupCCM_ab()
            testsed.addDust(a, b, ebv=self.ref_ebv, R_v=R_v)
            # Calculate difference due to dust when EBV=1.0 (m_dust = m_nodust - Ax, Ax > 0)
            self.Ax1[filtername] = testsed.calcMag(testbandpass) - flatmag

        # Telescope zeropoint for 30s exposure
        self.zp = {'u': 27.03, 'g': 28.38, 'r': 28.15, 'i': 27.86, 'z': 27.46, 'y': 26.68}
        # Atmospheric extinction coefficents
        self.kAtm = {'u': 0.502, 'g': 0.214, 'r': 0.126, 'i': 0.096, 'z': 0.069, 'y': 0.169}
        self.exptime = 30.
        self.pixscale = 0.2


class Size_precision_metric(metrics.BaseMetric):
    """Calculate the precision a 1D shape could be measured given observations.

    Parameters
    ----------
    pixscale : float (0.2)
        The pixelscale of the CCD, arsec/pix (0.2).
    fwhm_object : float (3.)
        The FWHM of the fiducial object who's shape is being measured, arcseconds (3.).
    mu_0_object : dict-like
        Dictionary with keys of filternames and values of the central surface brightness of an object in
        mags/sq arcsec
    phot_parameters : object (None)
        An object with properties of the telescope (like photometric zeropoints in each filter). Default of None will
        load values from sims_utils.

    stellar_density_limit : float (None)
        XXX--to add, put in a limit where if the stellar density is too high, returns weight of 0.

    """

    def __init__(self, seeingCol='seeingFwhmGeom', metricName='SizePrecision',
                 fwhm_object=3., mu_0_object={'g': 19., 'r': 19., 'i': 19.},
                 stellar_density_limit=None,
                 filterCol='filter', stellar_ref_peak={'g': 5000., 'r': 5000., 'i': 5000.},
                 m5Col='fiveSigmaDepth', exptimeCol='visitExposureTime',
                 skyCol='skyBrightness', airmassCol='airmass',
                 maps=['StellarDensityMap', 'DustMap'],
                 return_weights=False, phot_parameters=None, **kwargs):
        self.seeingCol = seeingCol
        self.m5Col = m5Col
        self.fwhm_object = fwhm_object
        self.mu_0_object = mu_0_object
        self.filterCol = filterCol
        self.exptimeCol = exptimeCol
        self.return_weights = return_weights
        self.stellar_ref_peak = stellar_ref_peak
        self.skyCol = skyCol
        self.airmassCol = airmassCol
        self.cols = [seeingCol, m5Col, filterCol, exptimeCol, skyCol, airmassCol]
        self.maps = maps
        units = 'SNR'
        super().__init__(col=self.cols, maps=self.maps, units=units, metricName=metricName, **kwargs)
        if phot_parameters is None:
            self.phot_parameters = Phot_properties()
        else:
            self.phot_parameters = phot_parameters
        # XXX--could declare a stellar density limit and mask out healpixels where things get too crowded

    def run(self, dataSlice, slicePoint=None):
        # Number of counts in the peak pixel from the object
        peak_counts = dataSlice[self.seeingCol]*0
        # Noise in the peak pixel
        noise_at_peak = dataSlice[self.seeingCol]*0+1e6
        # Size of the reference star
        star_fwhm = dataSlice[self.seeingCol]
        # Uncertainty in size of reference star
        sigma_fwhm_refstar = dataSlice[self.seeingCol]*0
        for filtername in self.mu_0_object:
            in_filt = np.where(dataSlice[self.filterCol] == filtername)
            #  Apply dust extinction to the peak flux
            A_x = self.phot_parameters.Ax1[filtername] * slicePoint['ebv']
            mu_0 = self.mu_0_object[filtername] + A_x
            # Scale mu_0 by exposure time
            mu_0 += 1.25*np.log(dataSlice[self.exptimeCol][in_filt]/self.phot_parameters.exptime)
            # Apply airmass extinction to the peak fluxes
            mu_0 += self.phot_parameters.kAtm[filtername]*(dataSlice[self.airmassCol][in_filt] - 1.0)
            # XXX--apply seeing correction to peak fluxes

            # convert central surface brightness to counts
            peak_counts_sqdeg = 10.**(0.4*(self.phot_parameters.zp[filtername] - mu_0))
            peak_counts[in_filt] = peak_counts_sqdeg * self.phot_parameters.pixscale**2
            # Convert sky brightness to counts
            sky_counts_sqdeg = 10.**(0.4*(self.phot_parameters.zp[filtername] - dataSlice[self.skyCol][in_filt]))
            sky_counts = sky_counts_sqdeg * self.phot_parameters.pixscale**2
            # Assuming sky or source dominating the noise. XXX--do I need a gain term in here maybe?
            noise_at_peak[in_filt] = (sky_counts + peak_counts[in_filt])**0.5

            # compute the uncertainty in the shape of a psf from a star on the image. Not
            # going to bother with dust and airamss on this, just assume you could use a brighter star.
            sigma_fwhm_refstar[in_filt] = 1.4*star_fwhm[in_filt]*(self.phot_parameters.pixscale/star_fwhm[in_filt])**0.5*noise_at_peak[in_filt]/self.stellar_ref_peak[filtername]

        # Let's use the simple equation from: http://articles.adsabs.harvard.edu//full/1992PASP..104.1104L/0001105.000.html
        # to say what the uncertainty in the shape we measure is.
        # the observed FWHM is convolved with the seeing.
        fwhm_observed = np.sqrt(self.fwhm_object**2 + dataSlice[self.seeingCol]**2)
        # uncertainty in the observed object size
        sigma_fwhm_object_predeconv = 1.4*fwhm_observed*(self.phot_parameters.pixscale/fwhm_observed)**0.5*noise_at_peak/peak_counts

        # Uncertainty in reference star PSF can dominate
        sigma_fwhm_object = (sigma_fwhm_object_predeconv**2 + sigma_fwhm_refstar**2)**0.5
        if self.return_weights:
            return 1./sigma_fwhm_object**2
        else:
            result = self.fwhm_object/np.sum(1./sigma_fwhm_object**2)**-0.5
            return result


class Systematic_angle_metric(metrics.BaseMetric):
    """Compute how strongly systematics are canceled in a series of shape observations

    Parameters
    ----------
    angleCol : str ('rotTelPos')
        The angle to check for systematics, typically rotTelPos or rotSkyPos
    systematic_level : float (0.1)
        The fractional level of systematic to assume one is trying to average out.
    nphase : int (30)
        The number of phases to check (default 30)
    """

    def __init__(self, angleCol='rotTelPos', systematic_level=0.1, mod=180., shape_metric=None,
                 nphase=30, units='Systematics Remaining (0 to 1)', metricName='AngularSystematics', **kwargs):
        if shape_metric is None:
            self.shape_metric = Size_precision_metric(return_weights=True, **kwargs)

        self.mod = np.radians(mod)
        self.angleCol = angleCol
        self.systematic_level = systematic_level
        self.phases = np.linspace(0, 2*np.pi, num=nphase).reshape(nphase, 1)
        cols = self.shape_metric.cols + [angleCol]
        maps = self.shape_metric.maps
        super().__init__(col=cols, maps=maps, units=units, metricName=metricName, **kwargs)

    def run(self, dataSlice, slicePoint=None):
        weights = self.shape_metric.run(dataSlice, slicePoint=slicePoint)
        angles = dataSlice[self.angleCol] % self.mod
        # Could maybe broadcast with a phase vector
        # Suppose I have a galaxy with major axis a along the x-axis, and minor axis b along y axis
        # when angle=0. If there is a distortion along the x-axis, no shape distortion when angle=45 deg.
        a_stretch = np.abs(np.cos(angles*self.phases))
        b_stretch = np.abs(np.sin(angles*self.phases))
        # Compute the weighted mean. This should broadcast over the full range of phases
        numerator = (1.+self.systematic_level*a_stretch)
        denominator = (1.+self.systematic_level*b_stretch)
        shape_wmean = np.sum(numerator/denominator*weights, axis=1)/np.sum(weights)
        # Average over all the phases tested
        mean_residual = np.mean(np.abs(1.-shape_wmean))

        # systematic remaining in shape measurement. 0 means perfectly canceled, 1 means
        # no systematic was removed.
        # XXX--maybe this should be divided by self.systematic_level? Then the result is the level
        # to which systematics average out I think?
        return mean_residual

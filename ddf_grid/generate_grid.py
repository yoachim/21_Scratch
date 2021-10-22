import numpy as np
import healpy as hp
from rubin_sim.utils import ddf_locations
import rubin_sim.skybrightness as sb
from rubin_sim.utils import m5_flat_sed
from rubin_sim.site_models.seeingModel import SeeingModel
import sys

if __name__ == "__main__":

    dds = ddf_locations()
    mjd0 = 60218.
    delta_t = 15./60./24.  # to days
    survey_length = 10.*365.25
    sun_limit = np.radians(-12.)  # degrees

    nominal_seeing = 0.7  #  arcsec

    filtername = 'g'

    seeing_model = SeeingModel()

    seeing_indx = 1

    mjds = np.arange(mjd0, mjd0+survey_length, delta_t)

    names = ['mjd', 'sun_alt']
    for survey_name in dds.keys():
        names.append(survey_name+'_airmass')
        names.append(survey_name+'_sky_g')
        names.append(survey_name+'_m5_g')

    types = [float]*len(names)
    result = np.zeros(mjds.size, dtype=list(zip(names, types)))
    result['mjd'] = mjds

    # pretty sure these are radians
    ras = np.radians(np.array([dds[survey][0] for survey in dds]))
    decs = np.radians(np.array([dds[survey][1] for survey in dds]))

    sm = sb.SkyModel(mags=True)
    mags = []
    airmasses = []
    sun_alts = []

    maxi = mjds.size
    for i, mjd in enumerate(mjds):
        progress = i/maxi*100
        text = "\rprogress = %0.1f%%" % progress
        sys.stdout.write(text)
        sys.stdout.flush()

        sm.setRaDecMjd(ras, decs, mjd, degrees=False)
        if sm.sunAlt > sun_limit:
            mags.append(sm.returnMags()['g']*0)
            airmasses.append(sm.airmass*0)
        else:
            mags.append(sm.returnMags()['g'])
            airmasses.append(sm.airmass)
        sun_alts.append(sm.sunAlt)

    mags = np.array(mags)
    airmasses = np.array(airmasses)
    result['sun_alt'] = sun_alts
    for i, survey_name in enumerate(dds.keys()):
        result[survey_name+'_airmass'] = airmasses[:, i]
        result[survey_name+'_sky_g'] = mags[:, i]

        # now to compute the expected seeing if the zenith is nominal
        FWHMeff = seeing_model(nominal_seeing, airmasses[:, i])['fwhmEff'][seeing_indx, :]
        result[survey_name+'_m5_g'] = m5_flat_sed('g', mags[:, i], FWHMeff, 30.,
                                                  airmasses[:, i], nexp=1)


    np.savez('ddf_grid.npz', ddf_grid=result)

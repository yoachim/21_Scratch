import numpy as np
import healpy as hp
from lsst.sims.featureScheduler.surveys import generate_dd_surveys
import lsst.sims.skybrightness as sb
from lsst.sims.utils import m5_flat_sed
from lsst.sims.seeingModel import SeeingModel
import sys

if __name__ == "__main__":

    dds = generate_dd_surveys()
    mjd0 = 59853.5
    delta_t = 15./60./24.  # to days
    survey_length = 10.*365.25
    sun_limit = np.radians(-12.)  # degrees

    nominal_seeing = 0.7  #  arcsec

    filtername = 'g'


    seeing_model = SeeingModel()

    seeing_indx = 1 #np.where(seeing_model.filter_list == filtername)[0]

    # result

    mjds = np.arange(mjd0, mjd0+survey_length, delta_t)

    # XXX Temp
    #mjds = mjds[0:100]

    names = ['mjd', 'sun_alt']
    for survey in dds:
        names.append(survey.survey_name+'_airmass')
        names.append(survey.survey_name+'_sky_g')
        names.append(survey.survey_name+'_m5_g')

    types = [float]*len(names)
    result = np.zeros(mjds.size, dtype=list(zip(names, types)))
    result['mjd'] = mjds

    # pretty sure these are radians
    ras = np.array([survey.ra for survey in dds])
    decs = np.array([survey.dec for survey in dds])

    sm = sb.SkyModel(observatory='LSST', mags=True)
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
    for i, survey in enumerate(dds):
        result[survey.survey_name+'_airmass'] = airmasses[:, i]
        result[survey.survey_name+'_sky_g'] = mags[:, i]

        # now to compute the expected seeing if the zenith is nominal
        FWHMeff = seeing_model(nominal_seeing, airmasses[:, i])['fwhmEff'][seeing_indx, :]
        result[survey.survey_name+'_m5_g'] = m5_flat_sed('g', mags[:, i], FWHMeff, 30., airmasses[:, i], nexp=1)


    np.savez('ddf_grid.npz', ddf_grid=result)

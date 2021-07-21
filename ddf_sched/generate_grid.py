import numpy as np
import healpy as hp
from rubin_sim.scheduler.surveys import generate_dd_surveys
import rubin_sim.skybrightness as sb
from rubin_sim.utils import m5_flat_sed
from rubin_sim.site_models import SeeingModel
import sys

if __name__ == "__main__":

    dds = generate_dd_surveys()
    mjd0 = 60218.
    delta_t = 15./60./24.  # to days
    survey_length = 10.*365.25
    sun_limit = np.radians(-12.)  # degrees

    nominal_seeing = 0.7  #  arcsec

    seeing_model = SeeingModel()

    seeing_indx = 1 #np.where(seeing_model.filter_list == filtername)[0]

    # result

    mjds = np.arange(mjd0, mjd0+survey_length, delta_t)

    mjds=mjds[0:20]

    names = ['mjd', 'sun_alt']
    for survey in dds:
        names.append(survey.survey_name+'_airmass')
        names.append(survey.survey_name+'_sky_u')
        names.append(survey.survey_name+'_sky_g')
        names.append(survey.survey_name+'_sky_r')
        names.append(survey.survey_name+'_sky_i')
        names.append(survey.survey_name+'_sky_z')
        names.append(survey.survey_name+'_sky_y')
        names.append(survey.survey_name+'_m5_g')

    types = [float]*len(names)
    result = np.zeros(mjds.size, dtype=list(zip(names, types)))
    result['mjd'] = mjds

    # pretty sure these are radians
    ras = []
    decs = []
    for survey in dds:
        if np.size(survey.ra) > 1:
            ras.append(survey.ra[0])
            decs.append(survey.dec[0])
        else:
            ras.append(survey.ra)
            decs.append(survey.dec)
    sm = sb.SkyModel(mags=True)
    mags_u = []
    mags_g = []
    mags_r = []
    mags_i = []
    mags_z = []
    mags_y = []
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
            mags = sm.returnMags()
            mags_u.append(mags['u']*0)
            mags_g.append(mags['g']*0)
            mags_r.append(mags['r']*0)
            mags_i.append(mags['i']*0)
            mags_z.append(mags['z']*0)
            mags_y.append(mags['y']*0)
            airmasses.append(sm.airmass*0)
        else:
            mags = sm.returnMags()
            mags_u.append(mags['u'])
            mags_g.append(mags['g'])
            mags_r.append(mags['r'])
            mags_i.append(mags['i'])
            mags_z.append(mags['z'])
            mags_y.append(mags['y'])
            airmasses.append(sm.airmass)
        sun_alts.append(sm.sunAlt)

    mags_u = np.array(mags_u)
    mags_g = np.array(mags_g)
    mags_r = np.array(mags_r)
    mags_i = np.array(mags_i)
    mags_z = np.array(mags_z)
    mags_y = np.array(mags_y)
    

    airmasses = np.array(airmasses)
    result['sun_alt'] = sun_alts
    for i, survey in enumerate(dds):
        result[survey.survey_name+'_airmass'] = airmasses[:, i]
        result[survey.survey_name+'_sky_u'] = mags_u[:, i]
        result[survey.survey_name+'_sky_g'] = mags_g[:, i]
        result[survey.survey_name+'_sky_r'] = mags_r[:, i]
        result[survey.survey_name+'_sky_i'] = mags_i[:, i]
        result[survey.survey_name+'_sky_z'] = mags_z[:, i]
        result[survey.survey_name+'_sky_y'] = mags_y[:, i]
        

        # now to compute the expected seeing if the zenith is nominal
        FWHMeff = seeing_model(nominal_seeing, airmasses[:, i])['fwhmEff'][seeing_indx, :]
        result[survey.survey_name+'_m5_g'] = m5_flat_sed('g', mags_g[:, i], FWHMeff, 30., airmasses[:, i], nexp=1)


    np.savez('ddf_grid.npz', ddf_grid=result, ra=ras, dec=decs, names=[survey.survey_name for survey in dds])

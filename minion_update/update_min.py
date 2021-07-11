import numpy as np
import pandas as pd
import sqlite3
from rubin_sim.scheduler.modelObservatory import Model_observatory
from rubin_sim.scheduler.utils import empty_observation, run_info_table, schema_converter
import sys
from astropy.time import Time



def update_minion(outfile='minion_1016_update.db'):
    """Let's update the minion_1016 runs to have the current sky, weather downtime, and throughputs.
    """

    conn = sqlite3.connect('minion_1016_sqlite.db')
    query = 'select fieldRA, fieldDec, filter, expMJD, night, visitExpTime, visitTime, airmass, rotSkyPos, rotTelPos, altitude, azimuth, slewTime from Summary group by expMJD order by expMJD'
    df = pd.read_sql(query, conn)

    num_obs = df['fieldRA'].size

    mo = Model_observatory(mjd_start=df['expMJD'].min())
    blank = empty_observation()

    observations = np.zeros(num_obs, dtype=blank.dtype)
    observations['RA'] = df['fieldRA']
    observations['dec'] = df['fieldDec']
    observations['mjd'] = df['expMJD']
    observations['filter'] = df['filter']
    observations['exptime'] = df['visitExpTime']
    observations['nexp'] = 2
    observations['slewtime'] = df['slewTime']
    observations['alt'] = df['altitude']
    observations['az'] = df['azimuth']
    observations['rotSkyPos'] = df['rotSkyPos']
    observations['rotTelPos'] = df['rotTelPos']
    observations['visittime'] = df['visitTime']

    obs_good = np.zeros(num_obs, dtype=bool)

    for i, obs in enumerate(observations):

        obs_good[i] = True #mo.check_up(obs['mjd'])
        clouds = mo.cloud_data(Time(obs['mjd'], format='mjd'))
        if clouds > mo.cloud_limit:
            obs_good[i] = False

        if obs_good[i]:
            mo.mjd = obs['mjd']

            observations[i] = mo.observation_add_data(obs)

            progress = i/num_obs*100
            text = "\rprogress=%.3f%%, %i of %i" % (progress, i, num_obs)
            sys.stdout.write(text)
            sys.stdout.flush()
        
    
    observations = observations[np.where(obs_good == True)[0]]
    if outfile is not None:
        info = run_info_table(mo)
        converter = schema_converter()
        converter.obs2opsim(observations, filename=outfile, info=info, delete_past=True)


if __name__ == '__main__':
    update_minion()

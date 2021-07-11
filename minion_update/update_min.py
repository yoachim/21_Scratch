import numpy as np
import pandas as pd
import sqlite3
from rubin_sim.scheduler.modelObservatory import Model_observatory
from rubin_sim.scheduler.utils import empty_observation, run_info_table, schema_converter
import sys



def update_minion(outfile='minion_1016_update.db'):
    """Let's update the minion_1016 runs to have the current sky, weather downtime, and throughputs.
    """

    conn = sqlite3.connect('minion_1016_sqlite.db')
    query = 'select fieldRA, fieldDec, filter, expMJD, night, visitExpTime, airmass, rotSkyPos, rotTelPos, altitude, azimuth, slewTime from Summary group by expMJD'
    df = pd.read_sql(query, conn)

    num_obs = df.size

    mo = Model_observatory(mjd_start=df['expMJD'].min())
    obs_list = []

    for index, line in df.iterrows():
        obs = empty_observation()
        obs['RA'] = line['fieldRA']
        obs['dec'] = line['fieldDec']
        obs['filter'] = line['filter']
        obs['exptime'] = line['visitExpTime']
        obs['nexp'] = 2
        obs['slewtime'] = line['slewTime']
        obs['alt'] = line['altitude']
        obs['rotSkyPos'] = line['rotSkyPos']
        obs['rotTelPos'] = line['rotTelPos']

        mo.mjd = line['expMJD']


        progress = index/num_obs*100
        text = "\rprogress=%.3f%%" % progress
        sys.stdout.write(text)
        sys.stdout.flush()

        if mo.check_mjd(mo.mjd):
            obs = mo.observation_add_data(obs)
            obs_list.append(obs)
        
            
    observations = np.array(obs_list)[:, 0]
    if outfile is not None:
        info = run_info_table(mo)
        converter = schema_converter()
        converter.obs2opsim(observations, filename=outfile, info=info, delete_past=True)


if __name__ == '__main__':
    update_minion()

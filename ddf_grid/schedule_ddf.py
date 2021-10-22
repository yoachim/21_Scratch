import numpy as np
import gurobipy as gp
from gurobipy import GRB
from rubin_sim.utils import ddf_locations
#from rubin_sim.utils import calcSeason


def calcSeason(ra, time):
    """Calculate the 'season' in the survey for a series of ra/dec/time values of an observation.
    Based only on the RA of the point on the sky, it calculates the 'season' based on when this
    point would be overhead .. the season is considered +/- 0.5 years around this time.

    Parameters
    ----------
    ra : float
        The RA (in degrees) of the point on the sky
    time : np.ndarray
        The times of the observations, in MJD

    Returns
    -------
    np.ndarray
        The season values
    """
    # Reference RA and equinox to anchor ra/season reference - RA = 0 is overhead at autumnal equinox
    # autumn equinox 2014 happened on september 23 --> equinox MJD
    Equinox = 2456923.5 - 2400000.5
    # convert ra into 'days'
    dayRA = ra / 360 * 365.25
    firstSeasonBegan = Equinox + dayRA - 0.5 * 365.25
    seasons = (time - firstSeasonBegan) / 365.25
    # Set first season to 0
    seasons = seasons - np.floor(np.min(seasons))
    return seasons



def sched_ddf(ddf_name, sun_limit=-18., airmass_limit=2.1, sky_limit=22.,
              zeropoint=25.0, n_wanted=400, season_frac=0.2, time_limit=200):
    """Schedule a single DDF by finding the distribution of nights. 
    Doesn't optimize for within a night
    """

    ddf_data = np.load('ddf_grid.npz')
    ddf_grid = ddf_data['ddf_grid'].copy()

    # XXX-- double check that I got this right
    ack = ddf_grid['sun_alt'][0:-1] * ddf_grid['sun_alt'][1:]
    night = np.zeros(ddf_grid.size, dtype=int)
    night[np.where((ddf_grid['sun_alt'][1:] >=0) & (ack < 0))] += 1
    night = np.cumsum(night)

    season = calcSeason(9.45, ddf_grid['mjd'])
    season % 1 # Can set things to be 0 when out of season, and 1 in season. Then do a cumsum, normalize, maybe round.

    m = gp.Model("try_sched")

    ngrid = ddf_grid['mjd'].size
    sun_limit = np.radians(-18.)
    airmass_limit = 2.1  
    sky_limit = 22. #20. #21.5 #22.
    zeropoint = 25.0  # mags
    sequence_limit = 400 #230
    pause_time = 13/24.  # days
    RA = 9.45  # RA of the DDF
    delta_t = ddf_grid['mjd'][1] - ddf_grid['mjd'][0]

    # Let's try scheduling just one for now
    schedule = m.addMVar(ngrid, vtype=GRB.BINARY, name="pointing_1")

    # set a sun mask
    sun_mask = np.zeros(ngrid, dtype=bool)
    sun_mask[np.where(ddf_grid['sun_alt'] >= sun_limit)] = 1

    airmass_mask = np.zeros(ngrid, dtype=bool)
    airmass_mask[np.where(ddf_grid['DD:ELAISS1_airmass'] >= airmass_limit)] = 1

    sky_mask = np.zeros(ngrid, dtype=bool)
    sky_mask[np.where(ddf_grid['DD:ELAISS1_sky_g'] <= sky_limit)] = 1
    sky_mask[np.where(np.isnan(ddf_grid['DD:ELAISS1_sky_g']) == True)] = 1

    # Let's add the constraints
    m.addConstr(schedule @ sun_mask == 0)
    m.addConstr(schedule @ airmass_mask == 0)
    m.addConstr(schedule @ sky_mask == 0)

    # limit the total number of ddf sequences
    # HA! Need to set an exact number I think. Or maybe a range.
    m.addConstr(schedule.sum() == sequence_limit)


    # prevent a repeat sequence in a night
    unights, indx = np.unique(night, return_index=True)
    night_mjd = ddf_grid['mjd'][indx]
    # The season of each night
    night_season = calcSeason(RA, night_mjd)
    sched_night = m.addMVar(unights.size, vtype=GRB.INTEGER)
    for i,n in enumerate(unights):
        in_night = np.where(night == n)[0]
        m.addConstr(schedule[in_night]@schedule[in_night] <= 1)
        m.addConstr(sched_night[i] == schedule[in_night].sum())


    raw_obs = np.ones(unights.size)
    # take out the ones that are out of season
    season_mod = night_season % 1
    # 7.2 month observing season if season_frac = 0.2
    season_frac = 0.2
    out_season = np.where((season_mod < season_frac) | (season_mod > (1.-season_frac)))
    raw_obs[out_season] = 0
    cumulative_desired = np.cumsum(raw_obs)
    cumulative_desired = cumulative_desired/cumulative_desired.max()*sequence_limit

    # Makes it go blazing fast agian, that's for sure!
    cumulative_desired = np.round(cumulative_desired)

    # Cumulative number of scheduled events (by night, to avoid huge loop)
    cumulative_sched = m.addMVar(unights.size, vtype=GRB.INTEGER)
    cumulative_diff = m.addMVar(unights.size, vtype=GRB.INTEGER, lb=-sequence_limit, ub=sequence_limit)

    cumulative_dmax = m.addMVar(unights.size, vtype=GRB.INTEGER)


    m.addConstr(cumulative_sched[0] == sched_night[0])

    #linear_cumulative = np.arange(unights.size)
    #linear_cumulative = linear_cumulative/np.max(linear_cumulative) * sequence_limit
    #m.addConstr(cumulative_diff[0] == cumulative_sched[0] - linear_cumulative[0])
    m.addConstr(cumulative_diff[0] == cumulative_sched[0] - cumulative_desired[0])

    for i in np.arange(1,unights.size):
        m.addConstr(cumulative_sched[i] == cumulative_sched[i-1]+sched_night[i])
        m.addConstr(cumulative_diff[i] == cumulative_sched[i] - cumulative_desired[i])
        
    m.setObjective(cumulative_diff@cumulative_diff, GRB.MINIMIZE)
    m.Params.TimeLimit = 200
    m.optimize()

    return ddf_grid, schedule.X

def sched_ddf_first(ddf_name, sun_limit=-18., airmass_limit=2.1, sky_limit=22.,
              zeropoint=25.0, n_wanted=400, season_frac=0.2, time_limit=200):
    """Schedule a single DDF by finding the distribution of nights. 
    Doesn't optimize for within a night
    """

    locations = ddf_locations()
    RA = locations[ddf_name][0]
    ddf_data = np.load('ddf_grid.npz')
    ddf_grid = ddf_data['ddf_grid'].copy()
    ngrid = ddf_grid['mjd'].size

    # Compute a night for each MJD
    ack = ddf_grid['sun_alt'][0:-1] * ddf_grid['sun_alt'][1:]
    night = np.zeros(ddf_grid.size, dtype=int)
    night[np.where((ddf_grid['sun_alt'][1:] >= 0) & (ack < 0))] += 1
    night = np.cumsum(night)

    m = gp.Model("DDF_schedule")
    # Let's try scheduling just one for now
    schedule = m.addMVar(ngrid, vtype=GRB.BINARY, name="pointing")

    # set a sun mask
    sun_mask = np.zeros(ngrid, dtype=bool)
    sun_mask[np.where(ddf_grid['sun_alt'] >= sun_limit)] = 1

    airmass_mask = np.zeros(ngrid, dtype=bool)
    airmass_mask[np.where(ddf_grid['DD:%s_airmass' % ddf_name] >= airmass_limit)] = 1

    sky_mask = np.zeros(ngrid, dtype=bool)
    sky_mask[np.where(ddf_grid['DD:%s_sky_g' % ddf_name] <= sky_limit)] = 1
    sky_mask[np.where(np.isnan(ddf_grid['DD:%s_sky_g' % ddf_name]) == True)] = 1

    # Let's add the constraints
    m.addConstr(schedule @ sun_mask == 0)
    m.addConstr(schedule @ airmass_mask == 0)
    m.addConstr(schedule @ sky_mask == 0)

    # limit the total number of ddf sequences
    # HA! Need to set an exact number I think. Or maybe a range.
    m.addConstr(schedule.sum() == n_wanted)

    # prevent a repeat sequence in a night
    unights, indx = np.unique(night, return_index=True)
    night_mjd = ddf_grid['mjd'][indx]
    # The season of each night
    night_season = calcSeason(RA, night_mjd)
    sched_night = m.addMVar(unights.size, vtype=GRB.INTEGER)
    for i, n in enumerate(unights):
        in_night = np.where(night == n)[0]
        m.addConstr(schedule[in_night]@schedule[in_night] <= 1)
        m.addConstr(sched_night[i] == schedule[in_night].sum())

    raw_obs = np.ones(unights.size)
    # take out the ones that are out of season
    season_mod = night_season % 1
    # 7.2 month observing season if season_frac = 0.2
    season_frac = 0.2
    out_season = np.where((season_mod < season_frac) | (season_mod > (1.-season_frac)))
    raw_obs[out_season] = 0
    cumulative_desired = np.cumsum(raw_obs)
    cumulative_desired = cumulative_desired/cumulative_desired.max()*n_wanted

    # Makes it go blazing fast agian, that's for sure!
    cumulative_desired = np.round(cumulative_desired)

    # Cumulative number of scheduled events (by night, to avoid huge loop)
    cumulative_sched = m.addMVar(unights.size, vtype=GRB.INTEGER)
    cumulative_diff = m.addMVar(unights.size, vtype=GRB.INTEGER,
                                lb=-n_wanted, ub=n_wanted)

    m.addConstr(cumulative_sched[0] == sched_night[0])


    import pdb ; pdb.set_trace()
    # Makes it go blazing fast agian, that's for sure!
    cumulative_desired = np.round(cumulative_desired)

    m.addConstr(cumulative_diff[0] == cumulative_sched[0] - cumulative_desired[0])

    for i in np.arange(1, unights.size):
        m.addConstr(cumulative_sched[i] == cumulative_sched[i-1]+sched_night[i])
        m.addConstr(cumulative_diff[i] == cumulative_sched[i] - cumulative_desired[i])

    m.setObjective(cumulative_diff @ cumulative_diff, GRB.MINIMIZE)
    m.Params.TimeLimit = time_limit
    m.optimize()

    return ddf_grid, schedule.X

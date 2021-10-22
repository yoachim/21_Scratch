import numpy as np
import gurobipy as gp
from gurobipy import GRB
from rubin_sim.utils import ddf_locations
from rubin_sim.utils import calcSeason


class SchedDDF(object): 
    """Schedule a single DDF by finding the distribution of nights. 
        Doesn't optimize for within a night
        # 7.2 month observing season if season_frac = 0.2

        Parameters
        ----------

        """
    def __init__(self):

        ddf_data = np.load('ddf_grid.npz')
        self.ddf_grid = ddf_data['ddf_grid'].copy()
        self.ngrid = self.ddf_grid['mjd'].size
        self.locations = ddf_locations()

    def night_season(self, RA):
        """
        Parameters
        ----------
        RA : float
            RA in degrees
        """
        # XXX-- double check that I got this right
        ack = self.ddf_grid['sun_alt'][0:-1] * self.ddf_grid['sun_alt'][1:]
        night = np.zeros(self.ddf_grid.size, dtype=int)
        night[np.where((self.ddf_grid['sun_alt'][1:] >= 0) & (ack < 0))] += 1
        night = np.cumsum(night)

        unights, indx = np.unique(night, return_index=True)
        night_mjd = self.ddf_grid['mjd'][indx]
        # The season of each night
        night_season = calcSeason(RA, night_mjd)

        return night, night_mjd, night_season

    def optimize_within_night(self, schedule, mjd, night, m5):
        """if we have things scheduled per night, optimize within night
        """

        out_sched = schedule*0

        sched_indx = np.where(schedule == 1)[0]

        for indx in sched_indx:
            in_night = np.where((night == night[indx]) & (np.isfinite(m5)))[0]
            best_depth = np.min(np.where(m5[in_night] == np.nanmax(m5[in_night]))[0])
            out_sched[in_night[best_depth]] += 1

        return out_sched


    def best_night(self, ddf_name, n_wanted=400, time_limit=200, season_frac=0.2,
                   cumulative_desired=None, sun_limit=-18., airmass_limit=2.1, sky_limit=20.):
        RA = self.locations[ddf_name][0]
        sun_limit = np.radians(sun_limit)

        night, night_mjd, night_season = self.night_season(RA)
        unights = np.unique(night)

        m = gp.Model("try_sched")
        schedule = m.addMVar(self.ngrid, vtype=GRB.BINARY, name="pointing_1")

        # set a sun mask
        sun_mask = np.zeros(self.ngrid, dtype=bool)
        sun_mask[np.where(self.ddf_grid['sun_alt'] >= sun_limit)] = 1

        airmass_mask = np.zeros(self.ngrid, dtype=bool)
        airmass_mask[np.where(self.ddf_grid['%s_airmass' % ddf_name] >= airmass_limit)] = 1

        sky_mask = np.zeros(self.ngrid, dtype=bool)
        sky_mask[np.where(self.ddf_grid['%s_sky_g' % ddf_name] <= sky_limit)] = 1
        sky_mask[np.where(np.isnan(self.ddf_grid['%s_sky_g' % ddf_name]) == True)] = 1

        # Add the constraints
        m.addConstr(schedule @ sun_mask == 0)
        m.addConstr(schedule @ airmass_mask == 0)
        m.addConstr(schedule @ sky_mask == 0)

        # limit the total number of ddf sequences. 
        # HA! Need to set an exact number I think. Or maybe a range.
        m.addConstr(schedule.sum() == n_wanted)

        # Prevent a repeat sequence in a night
        sched_night = m.addMVar(unights.size, vtype=GRB.INTEGER)
        for i, n in enumerate(unights):
            in_night = np.where(night == n)[0]
            m.addConstr(schedule[in_night] @ schedule[in_night] <= 1)
            m.addConstr(sched_night[i] == schedule[in_night].sum())

        if cumulative_desired is None:
            raw_obs = np.ones(unights.size)
            # take out the ones that are out of season
            season_mod = night_season % 1
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

        m.addConstr(cumulative_diff[0] == cumulative_sched[0] - cumulative_desired[0])

        for i in np.arange(1, unights.size):
            m.addConstr(cumulative_sched[i] == cumulative_sched[i-1]+sched_night[i])
            m.addConstr(cumulative_diff[i] == cumulative_sched[i] - cumulative_desired[i])

        m.setObjective(cumulative_diff @ cumulative_diff, GRB.MINIMIZE)
        m.Params.TimeLimit = time_limit
        m.optimize()

        out_sched = self.optimize_within_night(schedule.X, self.ddf_grid['mjd'],
                                               night, self.ddf_grid['%s_m5_g' % ddf_name])

        return out_sched

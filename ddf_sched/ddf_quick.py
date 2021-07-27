import numpy as np
from astropy.time import Time
from rubin_sim.site_models import (ScheduledDowntimeData, UnscheduledDowntimeData,
                                   SeeingData, SeeingModel, CloudData, Almanac)
from rubin_sim.utils import Site, m5_flat_sed
import astropy.units as u
from astropy.coordinates import SkyCoord, AltAz, EarthLocation


class Fast_ddf_sim(object):
    """Class for quickly simulating DDF observations.

    Parameters
    ----------
    delta_t_min : float (36)
        The minimum time required between observations (seconds)
    pre_computed_blob : dict-like
        The data blob that has all the sky brightness and airmass values pre-computed
    """
    def __init__(self, delta_t_min=36., mjd_start=60218., cloud_limit=0.3, filter_change_time=120.,
                 pre_computed_blob=None):

        self.cloud_limit = cloud_limit
        self.delta_t_min = delta_t_min/3600./24.  # to days
        self.filter_change_time = filter_change_time/3600./24.

        self.data_blob = pre_computed_blob

        self.almanac = Almanac(mjd_start=mjd_start)

        mjd_start_time = Time(mjd_start, format='mjd')

        # Create an astropy location
        self.site = Site('LSST')
        self.location = EarthLocation(lat=self.site.latitude, lon=self.site.longitude,
                                      height=self.site.height)
        # Downtime
        sched_downtime_data = ScheduledDowntimeData(mjd_start_time)
        unsched_downtime_data = UnscheduledDowntimeData(mjd_start_time)

        sched_downtimes = sched_downtime_data()
        unsched_downtimes = unsched_downtime_data()

        down_starts = []
        down_ends = []
        for dt in sched_downtimes:
            down_starts.append(dt['start'].mjd)
            down_ends.append(dt['end'].mjd)
        for dt in unsched_downtimes:
            down_starts.append(dt['start'].mjd)
            down_ends.append(dt['end'].mjd)

        downtimes = np.array(list(zip(down_starts, down_ends)), dtype=list(zip(['start', 'end'], [float, float])))
        downtimes.sort(order='start')

        # Make sure there aren't any overlapping downtimes
        diff = downtimes['start'][1:] - downtimes['end'][0:-1]
        while np.min(diff) < 0:
            # Should be able to do this wihtout a loop, but this works
            for i, dt in enumerate(downtimes[0:-1]):
                if downtimes['start'][i+1] < dt['end']:
                    new_end = np.max([dt['end'], downtimes['end'][i+1]])
                    downtimes[i]['end'] = new_end
                    downtimes[i+1]['end'] = new_end

            good = np.where(downtimes['end'] - np.roll(downtimes['end'], 1) != 0)
            downtimes = downtimes[good]
            diff = downtimes['start'][1:] - downtimes['end'][0:-1]
        self.downtimes = downtimes

        self.seeing_data = SeeingData(mjd_start_time, seeing_db=None)
        self.seeing_model = SeeingModel()
        self.seeing_indx_dict = {}
        for i, filtername in enumerate(self.seeing_model.filter_list):
            self.seeing_indx_dict[filtername] = i

        self.cloud_data = CloudData(mjd_start_time, offset_year=0)

    def observe(self, observations_in):
        observations_out = observations_in.copy()

        observations_out = self.space_observations(observations_out)
        observations_out = self.remove_downtimes(observations_out)
        observations_out = self.remove_cloudy(self.observations_out)

        observations_out = self.add_details(observations_out)

        return observations_out

    def space_observations(self, observations):
        for i in np.arange(1, observations.size):
            diff = observations['mjd'][i] - observations['mjd'][i-1]
            if observations['filter'][i] != observations['filter'][i-1]:
                delta_t = self.filter_change_time
            else:
                delta_t = self.delta_t_min
            if diff <= delta_t:
                observations['mjd'][i] = observations['mjd'][i-1] + delta_t
        return observations

    def remove_downtimes(self, observations):
        # Remove observations where the telescope is in downtime
        indx = np.searchsorted(self.downtimes['start'], observations['mjd'])
        diff = observations['mjd'] - self.downtimes['end'][indx-1]
        telescope_up = np.where(diff > 0)[0]

        return observations[telescope_up]

    def remove_cloudy(self, observations):
        # Remove observations that were clouded out
        times = Time(observations['mjd'], format='mjd')
        cloud_vals = self.cloud_data(times)
        good_clouds = np.where(cloud_vals < self.cloud_limit)[0]

        return observations[good_clouds]

    def add_details(self, observations):
        """Add in the rest of the relevant details for the observations
        """

        filternames = np.unique(observations['filter'])
        ddf_names = np.unique(observations['note'])

        for filtername in filternames:
            for ddf_name in ddf_names:
                in_filt = np.where((observations['filter'] == filtername) & (observations['note'] == ddf_name))
                observations['skybrightness'][in_filt] = np.interp(observations['mjd'][in_filt],
                                                                   self.data_blob['ddf_grid']['mjd'],
                                                                   self.data_blob['ddf_grid'][ddf_name+'_sky_'+filtername])

        # RA, dec, mjd to altaz
        sc = SkyCoord(observations['RA']*u.rad, observations['dec']*u.rad)
        times = Time(observations['mjd'], format='mjd')
        aa = AltAz(location=self.location, obstime=times)
        temp_coords = sc.transform_to(aa)
        observations['alt'] = temp_coords.alt.rad
        observations['az'] = temp_coords.az.rad
        observations['airmass'] = 1./np.cos(np.pi/2. - observations['alt'])

        # seeing values
        for filtername in filternames:
            in_filt = np.where(observations['filter'] == filtername)
            FWHM_500 = self.seeing_data(Time(observations['mjd'][in_filt], format='mjd'))
            observations['FWHM_500'][in_filt] = FWHM_500
            seeing_dict = self.seeing_model(FWHM_500, observations['airmass'][in_filt])
            observations['FWHMeff'][in_filt] = seeing_dict['fwhmEff'][self.seeing_indx_dict[filtername]]
            observations['FWHM_geometric'][in_filt] = seeing_dict['fwhmGeom'][self.seeing_indx_dict[filtername]]

            observations['fivesigmadepth'][in_filt] = m5_flat_sed(filtername, observations['skybrightness'][in_filt],
                                                                  observations['FWHMeff'][in_filt],
                                                                  observations['exptime'][in_filt]/observations['nexp'][in_filt],
                                                                  observations['airmass'][in_filt],
                                                                  nexp=np.max(observations['nexp']))

        # Fill in the actual night
        indx = self.almanac.mjd_indx(observations['mjd'])
        observations['night'] = self.almanac.sunsets['night'][indx]
        

        return observations

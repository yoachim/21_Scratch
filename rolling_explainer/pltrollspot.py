import numpy as np
import matplotlib.pylab as plt
import healpy as hp

import lsst.sims.maf.db as db
import lsst.sims.maf.utils as utils
import lsst.sims.maf.metrics as metrics
import lsst.sims.maf.slicers as slicers
import lsst.sims.maf.stackers as stackers
import lsst.sims.maf.metricBundles as metricBundles
import lsst.sims.maf.plots as plots
from scipy.stats import binned_statistic, mode


def gap_stats(inarr, bins):
    inarr = np.sort(inarr)

    count, _b1, _b2 = binned_statistic(inarr, inarr, bins=bins, statistic=np.size)
    unight = np.unique(inarr)
    di = np.diff(unight)
    good = np.where(di < 50.)[0]
    med, _b1, _b2 = binned_statistic(unight[1:][good], di[good], bins=bins, statistic=np.median)
    un, _b1, _b2 = binned_statistic(unight[1:][good], di[good], bins=bins, statistic=np.size)

    return count, med, un

# Grabbed from MAF
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


def season_breaks(in_mjd, ra):
    """in_nights should be pre-sorted
    """

    season = np.floor(calcSeason(ra, in_mjd))


    di = np.diff(season)
    break_indx = np.where(di > 0)[0]
    #breaks = (in_mjd[break_indx] + in_mjd[break_indx+1])/2.

    return break_indx


def spot_inspect(filename, ra, dec, year_max=8.5, outDir='temp', season_pad=80):

    resultsDb = db.ResultsDb(outDir=outDir)

    f2c = {'u': 'purple', 'g': 'blue', 'r': 'green',
           'i': 'cyan', 'z': 'orange', 'y': 'red'}

    name = filename.replace('_v1.7_10yrs.db', '')

    conn = db.OpsimDatabase(filename)
    bundleList = []
    sql = '' #'night > 250 and night < %i' % (365*year_max)
    metric = metrics.PassMetric(['filter', 'observationStartMJD', 'fiveSigmaDepth', 'night'])
    slicer = slicers.UserPointsSlicer(ra=ra, dec=dec)
    summaryStats = []
    plotDict = {}
    bundleList.append(metricBundles.MetricBundle(metric, slicer, sql,
                                                 plotDict=plotDict,
                                                 summaryMetrics=summaryStats,
                                                 runName=name))
    bd = metricBundles.makeBundlesDictFromList(bundleList)
    bg = metricBundles.MetricBundleGroup(bd, conn, outDir=outDir, resultsDb=resultsDb)
    bg.runAll()
    #bg.plotAll(closefigs=False)
    mv = bundleList[0].metricValues[0]
    mv.sort(order='observationStartMJD')

    all_mjd = np.arange(mv['observationStartMJD'].min()-1, mv['observationStartMJD'].max()+2, 1)

    breaks_indx = season_breaks(all_mjd, ra)
    breaks1 = all_mjd[breaks_indx] - all_mjd.min() + mv['night'].min()
    breaks = [mv['night'].min()-1]
    breaks.extend(breaks1.tolist())
    breaks.append(mv['night'].max()+3)


    #breaks = np.array([mv['night'].min()-season_pad] + breaks.tolist() + [mv['night'].max()+season_pad])

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    di = np.diff(breaks)
    mps = breaks[0:-1] + di/2
    counts, med_gaps, unights = gap_stats(mv['night'], bins=breaks)

    for fn in f2c:
        in_filt = np.where(mv['filter'] == fn)[0]
        ax1.plot(mv['night'][in_filt],
                 mv['fiveSigmaDepth'][in_filt], 'o',
                 color=f2c[fn], label=fn, alpha=0.5)
    ax1.set_xlabel('Night')
    ax1.set_ylabel(r'5$\sigma$ depth (mags)')

    for i in np.arange(mps.size):
        plt.annotate('%i\n %.1f \n %i' % (counts[i], med_gaps[i], unights[i]), [mps[i], 20])

    #plt.legend(loc=(1.04,0))
    for br in breaks:
        ax1.axvline(br)
    ax1.set_ylim([19.5, 25.5])
    #plt.xlim([1340, 1560])
    ax1.set_title(name+'\nra=%.2f, dec=%.2f' % (ra, dec))

    return fig, ax1

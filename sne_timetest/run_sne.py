import lsst.sims.maf.metricBundles as metricBundles
import lsst.sims.maf.slicers as slicers
import lsst.sims.maf.db as db
import lsst.sims.maf.utils as utils
import sqlite3
import numpy as np
from lsst.sims.maf.metrics.snNSNMetric import SNNSNMetric
import healpy as hp


# to profile
# python -m cProfile -o profiler.out run_sne.py

def load_and_run():
    dbFile = 'baseline_nexp2_v1.7_10yrs.db'
    opsimdb = db.OpsimDatabase(dbFile)
    runName = dbFile.replace('.db', '')

    nside = 64
    slicer = slicers.HealpixSlicer(nside=nside)

    metric = SNNSNMetric(verbose=False)  #, zlim_coeff=0.98)

    bundleList = []

    #sql = ''
    sql = '(note = "%s")' %('DD:COSMOS')

    bundleList.append(metricBundles.MetricBundle(metric, slicer, sql, runName=runName))

    outDir = 'temp'
    resultsDb = db.ResultsDb(outDir=outDir)
    bundleDict = metricBundles.makeBundlesDictFromList(bundleList)
    bgroup = metricBundles.MetricBundleGroup(bundleDict, opsimdb, outDir=outDir, resultsDb=resultsDb)
    bgroup.runAll()
    bgroup.plotAll()


if __name__ == '__main__':

    load_and_run()

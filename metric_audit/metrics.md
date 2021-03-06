
Here's a list of metrics


<!---
----------------  Things we run standard ----------------
-->


## Science Metrics being run currently ##

ExgalM5_with_cuts : This is a DESC metric that looks at the coadded depth in i-band for unextincted area in years 1, 3, 6, and 10. I'm not a huge fan of this one since the dust cut is a magic number, but DESC like it. This outputs a 3x2pt FoM and Effective Area summary stats. Since this is i-band only, should not be used when trying to determine filter distributions on survey footprint! Ugh, and there's an extra hidden arbitrary magnitude cut, this metric has got to go.

DepthLimitedNumGalaxies : A DESC LSS metric. Returns the number of galaxies in i-band for unextincted area. Again, should not be used when trying to determine filter distributions on survey footprint!

WeakLensingNvisits : DESC WL metric. should not be used when trying to determine filter distributions on survey footprint!

SNIa : The fraction of injected SNe that meet various detection criteria. Should replace with the DESC SNe metric that comptues number of SNe and mean redshift. Note the DESC metric is a bit more computationally intensive, so we should veryify that it is accurate enough at low resolution, or plan to run on it's own (like Solar System metrics). Maybe need to add dust extinction to DESC metric as well.

Kuiper rotSkyPos and rotTelPos : Used to check that camera rotator angle is uniform. Not the most useful, but a good Q/A check to make sure things haven't changed wrt rotational dithering I suppose. Should probably be replaced with my simple systematics metric:  https://github.com/yoachim/21_Scratch/tree/main/shape_metric


DDF SNe : Same as SNIa above, but run on each DDF. Again, should probably replace with DESC SNIa metric. 

DDF median depth : Median depth in each filter in each DDF.

GalaxyCounts : Number of galaxies in i-band. Should not be used when trying to determine filter distributions on survey footprint!

Nstars : Number of MW stars predicted in each filter, with and without crowding corrections. Probably not useful for SCOC. Might be kinda useful for DM, but once we've run it once, not sure we need to continue running it.

FO metrics:  Related to the SRD, checking what area reaches 825 visits, and the median number of visits in the top 18,000 square degrees. The 

SRD parallax and proper motion : Not sure why we have the regular and the normalized in here. And why are the parallax and proper motion magnitudes different (22.4 & 24.0 vs 20.5 & 24)? Not sure we need parallax coverage metric in here. Need to add what is critical value for parallaz-DCR degeneracy to caption. Should also add SRD critical values to the captions.

NumberOfQuickRevisits : How useful is this one? I guess if the RapidRevisit is failing below, this one is ilustrative as to why. Is it actually in the SRD? Need to update caption, we don't have proposals.

RapidRevisits : Shows area on the sky that meets the rapid revisit requirement.  

YearCoverage : shows, per filter, how many unique years points on the sky are observed. Relevant for image differencing tempalte generation. Probably not a true "science" metric.


KN_* metrics:  Uses a lightcurve from PLASTICC challenge to check various detection criteria. I think this one has an update from the community we should probably adopt. Would also be good to check that the number of events we are simulating is adequate (only 17% are detected at all, so the relative metric value can jump around a lot while the absolute number of events changes little).


Microlesning : Metric from the community looking at fast and slow microlensing events. Slow microlensing seems pretty uninformative (we always find the slow ones). Fast microlensing gives a strong arguemnt for bulge and MC coverage. Might be updates from the community.

PeriodDetection : Metric for how well we recover periods of stars. This metric is a little suspect at the moment (a scipy update changed it's behaviour and I don't understand why). I would hope we could replace this some more sophisticated metrics from the community, e.g., the volume we can measure RR Lyrae periods to. 

TDE : Metric from the community simulating TDE events. Similar to KN metric, we may need to increase the sample size of simulated events to lower shot noise. 


### Solar System Metrics ###

Breaking these out because the solar system metrics are more computationally intensive to run, so they don't always get run right away on new simulations, but will be part of the standard set when we report things to the SCOC.

Population completeness for:

* Near Earth Asteroids (NEO)
* Potentially hazerdous Asteroids (PHA)
* Main Belt Asteroids (MBA)
* TNOs
* Trojans
* Oort
* Have something called SDO that's been commented out?
* Sounds like maybe add comets

Should double check which brightnesses are most interesting. (Right now doing differential completeness 3 pairs in 15 nights). 



<!---
----------------  In Development Metrics ----------------
-->

## Potential Science Metrics ##

### Brown Dwarf Volume ###

PY working with John Gizis. https://github.com/yoachim/LSST-BD-Cadence

Status:  Looks good, gives results consistent with earlier published calcs. Just need to decide on which stellar type to set as the default and merge to MAF repo. Should publisize and see if other groups want to run it in a different configuration (e.g., volume where we can see WD or NS). Could also update to optionally include dust and maybe get the volume where we can measure parallax on giants in the halo.


### Galaxy Shape Precision ###

PY working with Husni Almoubayyed and Rachel Mandelbaum. Started in https://github.com/yoachim/21_Scratch/tree/main/shape_metric

Status:  Actively working on defining how to best use SNR weighting.

### Stellar Parameter Uncertianty ###

PY working with Leo Girardi.

Status:  Brainstormed idea, need to start writing some code

Some other folks are looking at stellar metallicity with a focus on u-band as well.


### Magellenic Clouds ###

Knut Olson has plans for LMC/SMC metric.


### TDE metric ###

Metric for Tidal Disruption Events.  Being written up as a AAS Research Note bye Katja Bricman. 

Status:  Should double check that the output is reasonable. Just added dust extinction.


### AGN metric ###

Should try to get Yu et al metric on structure function for AGN. Looks like a handy metric we would want to run.

### Novel Discovery Metric ###

Fed et al are writing something up on this.


### KNe Metric ###

Have a metric from Christian Setzer:  https://github.com/LSST-nonproject/sims_maf_contrib/blob/master/mafContrib/GW170817DetMetric.py

Need to double check, then should be ready to promote to regular.

Michael Coughlin et al have made a quick KNe metric: https://github.com/LSST-nonproject/sims_maf_contrib/blob/master/science/Transients/KNeSlicer.ipynb

Great! We can run them both, make sure they are consistent, then pick one to run on the regular.

Maybe also have one based on plasticc light curves?


### Photometric Redshift ###

Melissa Graham has done some work on this. John Franklin has some potentially useful code as well. 


### Strongly Lensed SNe Ia ###

Working with Simon Huber et al.  This is in MAF, have updated to include dust. Just need to make sure it's still reasonable. OK--now we have dust. Had to update to run it per season rather than average all seasons together. Need to check that is still legit.

https://github.com/lsst/sims_maf/blob/master/python/lsst/sims/maf/metrics/snSLMetric.py

### Type Ia SNe number and redshift ###

From Philippe Gris et al.  Find the expected number and median redshift of SNe. 

Status:  I'd like to add dust extinction. This metric is fairly computationally expensive, so we need to check that it works to run at lower spatial resolution.

### Microlensing ###

written with Natasha Abrams et al.  

Status:  I think this one is good to go. 

### Periodic Stars ###

Have an initial metric here:  https://github.com/LSST-nonproject/sims_maf_contrib/blob/master/mafContrib/periodicStarMetric.py

Status:  I think a scipy update may have changed things on this. 

Marcella Di Criscienzo is using this and adding in some Lomb-Scargle

### Star Density Metric ###

A metric that can be used to get the total number of stars:  https://github.com/lsst/sims_maf/blob/master/python/lsst/sims/maf/metrics/starDensity.py

Currently runs in only a single filter, so a very limited metric, probably should not be promoted in current state

### Number of galaxies metric ###

Probably should cut because this is also single filter.


### Time Delay Metric ###

LJ and others:  https://github.com/lsst/sims_maf/blob/master/python/lsst/sims/maf/metrics/seasonMetrics.py

Currently uses proxies rather than SNR. Takes some means and medians, so might not perform properly on rolling cadence sims.

### XXX ###

Stuff from Mike Lund

### Variability Depth ###

From Keaton Bell:  https://github.com/LSST-nonproject/sims_maf_contrib/blob/master/science/variabilityDepth/variabilityDepth.ipynb

Status:  Looks pretty good and like it fell through the cracks earlier.


### Star Forming Regions ###

Being worked on by Sara Bonito et al

Also with Loredana Prisinzano.  Hacked up a start at:  https://github.com/yoachim/21_Scratch/blob/main/star_forming_vol/star_forming_volume.ipynb

I think we need a 3-D model of star forming regions and dust to make this work all the way.

Made some progress. May want to also add confusion uncertainties.


### Blazar Metric ###

Talked with Claudia Maria Raiteri. Sounds like the TDE metric is a good start for them.  Helped them get started:  https://github.com/yoachim/21_Scratch/blob/main/blazar_metric/blazar_saturation_metric.ipynb



### Updated 3x2 figure of merit emulator ###

By Husni Almoubayyed in sims_maf_contrib. Does this need to get merged still?--ok, looks like it got merged. 

### Crowding Metric ###

Probably a good metric that can be used as a base for other metrics, but not to helpful in itself? There were some questions about it being consistent with DES data, but it looks like things might be OK.


### DDF metrics ###

We are currently running the plasticc SNe Ia on the DDFs.  What else? Something from AGN?
Should clean up the code a tiny bit to consolidate the euclid fields maybe. Should probably do a set where we turn the focal plane on to test the different dithering strategies. Updated the example notebook in sims_maf_contrib tutorials.


<!---
----------------  Additional Metrics ----------------
-->

## Additional Science Metrics ##

Here are some metrics that we have, but are not necissarily running on all new simulations.


### DCR metric ###

Described in this AAS Research Note:  https://iopscience.iop.org/article/10.3847/2515-5172/abd6e2

The general conclusion is that while we can alter the survey strategy to increase the SNR on DCR measurments, the gain is not particularly impressive. Should confirm this with the latest cadence notes.


### Spatial Dithering ###

Lots of earlier work from Humna Awan (https://ui.adsabs.harvard.edu/abs/2016ApJ...829...50A/abstract). 

I think we have concluded that our default spatial dithering scheme is adequate and should not artificially create power around 1 degree scales. 


### Follow up Observatories ###

I like this one. No need to run it on everything, but a good reminder that we should make sure the alert stream is spread over a large range of declinations to spread out the follow-up load.




# Simulations to run as v2.0

Here are a list of simulations we should consider running as part of 2.0 to help finalize the survey strategy

## Baseline 2.0

A new baseline survey with new changes of

* Pairs in twilight
* New footprint? -- update so bulge is a circle rather than box selection.
* pairs spaced by 33 min
* u-band is 1x30s
* Probably put more weight on the footprint.


Baseline-like variations:
 
* 1-snap for all visits
* baseline-like, but classic footprint
* classic-style baseline and classic footprint. 

maybe also a run with the old footprint, and the old footprint/old style, so folks can say if there is any major losses from the old baseline style.

## u-band
1x50s with same number of visits
1x50 with fewer visits.

##


## Rolling

Could try rolling for both WFD and DDFs. 

## Big planets

* Turn off the mask around Jupyter
* no mask around any bright planets


## DDFs

Could try adding a calibration field near the south pole. Just do it at the start of morning twilight. Survey object for each filter. (but make sure connected to WFD, don't want it floating on it's own.)

## footprints

Could try chopping off the SCP, no one seems to have a metric that wants it.


---------------------

From google doc before edits:
New Baseline:
U band as 1x30, all other filters 2x15s
Non-twilight, take pairs aiming for 33 min separation
Twilight time, pairs with 15 min separation
New baseline footprint.  
Extragalactic WFD with extended Dec limits and dust extinction (let’s set the dec limits to give the extragalactic WFD area about 17000 sq deg). Standard current filter balance. 2-band rolling cadence in extragalactic WFD. Smooth dust limits /edges.
GP coverage - bulge rectangle (with expanded area) and the entire remainder of the plane as defined within latitude cuts - including through the SCP. No bridge. Add LMC/SMC. Use filter balance requested by TVS/SLWMV (need to check on this). Cover bulge at 825 visits per pointing level, and remainder at ~300 visits/pp level (check). Cut off GP at max dec of extragalactic WFD.
NES coverage on the order of 400-450 visits pp, griz. 
Cover remainder of SCP not within GP footprint at 6x10x4 = 240 visits pp. 
5 DD pointings (4 previous fields plus euclid - add links)
Probably update the footprint basis function weight to be a bit stronger


Retro:
A few runs to make it easier to throw away previous sims and make sure we didn’t break anything with the new baseline.
Retro footprint:  Same as new baseline, but use our classic retro footprint. (?)
Retro classic: retro footprint and v1.7 settings  (what’s the difference with v1.7 settings? vs. v1.7.1 or v1.5?)

Rolling:
In theory, rolling in the WFD and GP can be done independently. So we can run a variety of rolling and then see if we need to split them apart.
2, 3, and 6 band rolling 
I think the extragalactic WFD is going to need to be 2-band rolling. We should do 2-band in the baseline and non-rolling in an option. 
6-band rolling in the GP bridge is very interesting. 
Maybe 2 rolling strengths? 50% and 90%?

Longer u:
Set u to 1x50s, same relative number of visits
Set u to 1x50s, decrease number of visits to be similar amount of total time in u. 

NES sweep:
We should do a sweep of NES strength on the footprint (from 200 visits per pointing to 500 visits per pointing ), just to see how that changes solar system metrics. We could even vary the filter distribution too. g=0, .1,.2,.4 r=0, .23, 0.46, 0.8, 1 i=0, 0.23, 0.46, 0.8, 1, z=0,0.2, 0.4, 0.6, 0.9. Don’t vary filters now, ~3 sims varying strength. 

GP sweep: 
Vary GP low-priority region strength (from 160-300? Visits per pointing) to look at effect on GP metrics. 2 simulations.

Presto Color:
Add observations so there are observations at 90-120 min interval. Vary the amount of survey time dedicated to observing triplets. 
One simulation with all-sky presto color in the first year
Two-three simulations with some fraction of the sky in presto-color the whole time (10%, 20%, 30%? We can run more sims to decide what looks practical)
XXX--is that interval from the first in the pair, or the second? (the second I think)
XXX--do we want to include their desire to have broader filter spacing? Let’s try it with both - wider filter spacing and our standard filter spacing. These are specialized simulations to answer this very specific question, and worth trying both.

Long Gaps:
Try to get some observations in the 2-14 hour range. Vary the amount of time dedicated to trying to get long gaps.
After 5 years, vary the time spacing between pairs (how do we decide the spacing?)

Deep Drilling:
Oof. I made a good start at revamping the DDF scheduling, but it needs some more concerted effort. And, as always, we need some DDF specific metrics. Maybe the rigorous DDF upgrade waits for v2.1, and here we could do something like vary the DDF fraction of time (say, 2, 5, 7, 10% of visits for DDFs)?
maybe let’s vary 5% and 8% .. I doubt 10% will be viable, but 7% might not be super noticeable .. 8% seems like a split between these two. 2% seems like too little, given that the cadence is already on the low end for these DD fields.
Given the problem with updating the DDF scheduling - does that mean we can’t do rolling DD fields now? (this would be the hot ticket I suspect .. concentrated cadence in one year, lower cadence the next, etc.)
Goal: make people make DD metrics

Micro surveys: 
see Jay’s email for reference — this seems likely to add ~13? additional simulations (the trailed star visits is not one I would simulate at this time .. I don’t know how to do this within the current scheduler, to be honest — does this indicate a missing functionality? or is it just a problem with our current simulation framework?) .. plus one where we do all of the microsurveys, so 14 total. 
Arbitrarily define ToOs at 2% of time
We should add a simulation where we add some % of time as DD (there should obviously be some DD time .. which could be simulated as essentially blank blocks — how long? a preferential time of night? what fraction? 
Given that often the microsurveys are pushed into “well, this could be done in DD time”, it seems that it’s assumed DD time exists. I don’t know its definition, but perhaps some simulations would help put this into the right ballpark. 





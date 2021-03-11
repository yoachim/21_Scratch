
Here's a list of metrics


<!---
----------------  Things we run standard ----------------
-->

## Standard Metrics ##

### fO metric ###

For checking the area where we reach 825 visits over all filters.

Can be interpreted as how much contingency we have remaining at the end of the survey (if it is at 1.0, we have spent all the contingency)

XXX--I think we've adopted fONv median number of visits.

Note, this follows the letter of the SRD, but can fail for footprints designed to circumvent it (e.g., exploiting the fact there is a median to go deeper on part of the sky and shallow on another). Presumably, some science cases that desire survey uniformity would catch this.


### Parallax and Proper Motion ###

XXX--should look up the SRD requirements

### Rapid Revisit  ###

XXX--Do we meet the rapid revisit requirements.


### Solar System Metrics ###

Breaking these out because the solar system metrics are more computationally intensive to run, so they don't always get run right away on new simulations, but will be part of the standard set when we report things to the SCOC.

Population completeness for:

* Near Earth Asteroids (NEO)
* Potentially hazerdous Asteroids (PHA)
* Main Belt Asteroids (MBA)
* TNOs
* Trojans
* Oort
* Have something called SDO that's been commented out.

Should double check which brightnesses are most interesting. (Right now doing differential completeness 3 pairs in 15 nights)

XXX--any populations to add? 


<!---
----------------  In Development Metrics ----------------
-->

## Potential Science Metrics ##

### Brown Dwarf Volume ###

PY working with John Gizis. https://github.com/yoachim/LSST-BD-Cadence

Status:  Looks good, gives results consistent with earlier published calcs. Just need to decide on which stellar type to set as the default and merge to MAF repo. Should publisize and see if other groups want to run it in a different configuration (e.g., volume where we can see WD or NS). Could also update to optionally include dust and maybe get the volume where we can measure parallax on giants in the halo.


### Galaxy Shape Precision ###

PY working with Husni and Rachel Mandelbaum. Started in https://github.com/yoachim/21_Scratch/tree/main/shape_metric

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

Pretty sure AGN group is working on something.

### Novel Discovery Metric ###

Fed et al are writing something up on this.


### KNe Metric ###

Have a metric from Christian Setzer:  https://github.com/LSST-nonproject/sims_maf_contrib/blob/master/mafContrib/GW170817DetMetric.py

Need to double check, then should be ready to promote to regular.

Michael Coughlin et al also might have made a quick KNe metric:  https://github.com/mcoughlin/sims_maf_contrib/tree/KNe

Great! We can run them both, make sure they are consistent, then pick one to run on the regular.


### Photometric Redshift ###

Melissa Graham has done some work on this. John Franklin has some potentially useful code as well. 


### Strongly Lensed SNe Ia ###

Working with Simon Huber et al.  This is in MAF, have updated to include dust. Just need to make sure it's still reasonable.

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


### Updated 3x2 figure of merit emulator ###

By Husni Almoubayyed in sims_maf_contrib. Does this need to get merged still?

### Crowding Metric ###

Probably a good metric that can be used as a base for other metrics, but not to helpful in itself? There were some questions about it, but it looks like things might be OK.


### DDF metrics ###

I have code somewhere to define a circle of points around a DDF. Can run the SNe Ia on it. What else? Something from AGN?


<!---
----------------  Additional Metrics ----------------
-->

## Additional Science Metrics ##

Here are some metrics that we have, but are not necissarily running on all new simulations.


### DCR metric ###

Described in this AAS Research Note:  https://iopscience.iop.org/article/10.3847/2515-5172/abd6e2

The general conclusion is that while we can alter the survey strategy to increase the SNR on DCR measurments, the gain is not particularly impressive.


### Spatial Dithering ###

Lots of earlier work from Humna Awan (https://ui.adsabs.harvard.edu/abs/2016ApJ...829...50A/abstract). 

I think we have concluded that our default spatial dithering scheme is adequate and should not artificially create power around 1 degree scales.


### Follow up Observatories ###

I like this one. No need to run it on everything, but a good reminder that we should make sure the alert stream is spread over a large range of declinations to spread out the follow-up load.



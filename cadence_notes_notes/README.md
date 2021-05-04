## Notes on the Cadence Notes


Prisinzano:  Young stars in the thing disk. Not clear how they handle filters? Probably in the code, I think it was gri maybe.

Bonito et at:  Variability of young stellar objects.  Not a super well defined metric, but they make a case for doing some work on hours timescale. I think there will be more like this. Might be able to use the AGN structure function metric for YSOs? Does that make sense?  This is one where It would make sense to also observe the LMC/SMC at the same time.

Raireri et al:  Blazar variability.  They seem to be worried about saturation. Fig 2 seems to show that saturation is not an issue. And even if it was, we can probably still alert on it, right? 

Clarkson et at:  Bulge stellar pops. They want deep u-band, and good seeing observations on crowded areas (but no metric to judge that). They have a u-i metallicity figure of merit for red clump giants. Then RR Lyrae stars to some uncertainty. Not sure why we only care towards the bulge? Seems like this one has a very strong preference for a different filter distribution towards the bulge, so we should make sure we grab the metrics that capture that.

Clarkson et al.: Saturation of bright objects. Twilight time for parallax? huh? Computes volume where things saturate. Do we care about saturation. Keep in mind, there are chip gaps, so you need to dither if you actually want to cover the whole sky at short exposure time.

Brandt et al: AGN DDF. grizy every other night on a long (7-8.5 month) season is their main goal. (note the z band is not always loaded, so this is impossible). They essentially propose a rolling DDF scenario. This would be kinda cool. I think we are close to having the tooling to do it now. Sounds like they have some simulations in prep, maybe we can get them.

Yu et al:  Have a nice DDF structure function metric. They really like having long u-band exposures.

Tisanic et al:  Lomb-Scargle for stellar periods. They did some cool Monte Carlo stuff. Doesn't look like they ran over many of the sims though, and no metric we can use.

van Velzen et al:  TDE stuff. They like the metric with u-band observations. I think we have this one and can run it at will if we want to. Need to check that we have enough events that it's statistically well sampled and not too noisy. I love radar plots!

Bachelet et al:  microlensing events. They want to look at the Roman RGES field every 30 minutes for 2-4 hours per night during the Roman observing season.  Looks like it's a pretty tiny field? No metric provided. 

Schwamb et al: Solar system collab.  I think we have all these metrics. Which ones should we run and show to the SCOC standard? We've been doing discovery for 2-3 pops, but could expand to color and rotation or more pops.

Assef et al:  Quasar photo-z.  Looks like this is just another strong vote for not taking pairs in the same filter.

Assef et al: Quasar counts:  They have a metric for number of quasars in i-band. Could be a useful metric to have I suppose.

Assef et al: photo-z of type 1 quasars. Something about computing a color-excess. 

Musella et al: Classical variable stars. They have a repo full of notebooks. They have a lot of plots. It kinda seems to me like things get observed a whole lot, so for most variable stars we aren't that sensitive to survey cadence. Not sure there's anything here we would want to run all the time. Maybe we could lift some of their light curves, so a volume we reach RR Lyrae to or something.

Olsen et al:  dwarf sats and substructure around magellenic clouds:  Has a nice plot. Not sure if there's code available for it. 

Jaimes et al: MW globular clusters:  Globulars are neat. They are trying to use the periodDetect metric. They advocate doing extra observations on some selected GCs.  That wouldn't be tough to do, just pencil it in as a DDF and do it when convienent in the night, as long as there aren't too many filters. Similar strategy has been proposed for some sort of calibraiton field. 

Abrams et al:  Microlensing discovery and characterization:  They really want the bulge and magellenic clouds covered. We have metrics from this group already. Not sure what's up with the Besancon model. Note the different timescales are very very correlated--so this is all being driven by footprint coverage at the moment. 

Carlin et al: Resolved census of dwarf satellites around Local Volume galaxies:  They really like more g-band depth. I think there was a similar white paper by Bell et al that also advocated more g-band depth around nearby galaxies. 

Blaineau et al:  Microlensing towards MCs.  Sounds like they want very long baseline coverage of LMC/SMC. We could make a metric for this I suppose--very long timescale variables. 

Graham et al:  SNe. Lots of text. Claims they like rolling cadence. Not sure there's much in here that matters.

Graham et al: Photo-z note.  They grab median coadded depth in low extinction WFD area. Pass that to a CMNN estimator. Ah, deeper things were worse because they incuded fainter and higher z things. A PZ metric for maf still in the works. Could set the grid points to be the range of depths we want to probe I suppose. We could even just compute the depths ahead of time, then find the N 6-D points that cover the volume the best. There should be some correlations, like when the footprint gets bigger, all filters get fainter. Does look much improved.

Ferguson et al:  Galaxies. What do they mean "full depth" of one DDF? Is that even possible? Want to add the Virgo cluster, at dec+13, that's a good idea.

Hundertmark et al:  Galactic Plane transients.  Microlensing stuff.  Looks similar to a plot in another note? They do really like 6-stripe and bulge roll. Note again that this is very correlated. They have a notebook, so it would be nice to grab these metrics.

Street et al:  Survey footprint for galactic plane and MCs.  They really want all WFD in the southern sky. So there are a bunch of maps. There is a list of star forming regions and globulars. I guess we could try and use that to help make a metric. 

Frohmaier et al: 4MOST doing spectroscopic followup.  They do some SNe Ia simulations, seeing when 4MOST can get spectra, so they want the object classified early enough. Really hate the same filter sim. 

Cuillandre et al:  They like the better dithering on the euclid DDF. I think they are advocating for the northern stripe so we can chase ToOs to any dec?  

Yu et al:  DCR.  OK, they come out and say we don't need to worry too much about DCR. Could double check to make sure we have their latest metric in MAF.

Bellm et al: They use TgapsMetric. There does sound like a case to be made for 2-14 hour gaps. They claim little improvement with the third_obs, but they don't plot them. 

Lochner et al:  DESC cadence note.  They want a replication of altSched (ugh, unhelpful guys). They like small dithers in the DDFs. Should make sure we can replicate that one.

Kovacevic et al:  AGN variability observables. They submitted a paper on this, cool. Looks nifty, lots of math. Not sure I understand their plots.

Moniez et al:  interstellar scintillation with high frequency LMC/SMC:  This is just a pitch to use LSST in movie mode for a few night on the LMC and SMC. That would be cool, but not really survey optimization. Do this in a night of commissioning.

Anguita et al:  Strong Lensing:  They want good seeing in g. Not sure there are any metric in here--but maybe a case to again incorporate the runs that try to get good seeing images in some filters every year.

Gizis et al:  Brown Dwarf astrometry.  Love these metrics (because I wrote them).  This could be a nice metric for helping with deciding filter balance. Need something to push blue now.

D'Orazio et al: Double AGN. Sounds like similar enough to SNe that we can just use that as a proxie?

Li et al:  Anomaly detection:  I love radar plots. 

Androni et al:  Kilanovae. They have a ZTFReST discovery algo. Is this in contrib--ah, it's hung up on a PR. 

Buckley et al: CVs. Very cool looking metric outputs!

Yu et al:  Non-parametric strcture function for AGN.  Looks like it'll work for the DDFs and main survey.

## Metrics we should try to get

* The number of young stars in thin disk from Prisinzano et al. I helped with this one, so should be easy to find. Looks like they updated with 3d dust! 
* distance to red clump giants and RR Lyrae from Clarkson et al.
* AGN reverberation mapping recovery from Brandt et al.
* Graham's new photo-z stuff
* Is there a good euclid overlap metric to be had?
* Some sort of Virgo Cluster metric
* Microlensing metrics from Hundertmark et al.
* maybe a Tgaps where we check the 2-14 hour pair area.
* Make sure we can do the number of SNe metric for DDFs the right way.
* At least some of the AGN structure function stuff
* Brown Dwarf volume metric
* the KNe metrics from Androni et al--currently on a PR.
* Need to get the CV metric from Buckley et al.



## New runs to try out:

* Even more presto color type sims. Want pairs in the 2-14 hour gap range.
* DDF with acourdian and rolling styles.
* Add Virgo Cluster to the footprint maker? Only 8 degrees across. 


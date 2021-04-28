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


## Metrics we should try to get

* The number of young stars in thin disk from Prisinzano et al. I helped with this one, so should be easy to find. Looks like they updated with 3d dust! 

* distance to red clump giants and RR Lyrae from Clarkson et al.

* AGN reverberation mapping recovery from Brandt et al.

## New runs to try out:

* Even more presto color type sims
* DDF with acourdian and rolling styles.

## Notes on the Cadence Notes


Prisinzano:  Young stars in the thing disk. Not clear how they handle filters? Probably in the code, I think it was gri maybe.

Bonito et at:  Variability of young stellar objects.  Not a super well defined metric, but they make a case for doing some work on hours timescale. I think there will be more like this. Might be able to use the AGN structure function metric for YSOs? Does that make sense?  This is one where It would make sense to also observe the LMC/SMC at the same time.

Raireri et al:  Blazar variability.  They seem to be worried about saturation. Fig 2 seems to show that saturation is not an issue. And even if it was, we can probably still alert on it, right? 

Clarkson et at:  Bulge stellar pops. They want deep u-band, and good seeing observations on crowded areas (but no metric to judge that). They have a u-i metallicity figure of merit for red clump giants. Then RR Lyrae stars to some uncertainty. Not sure why we only care towards the bulge? Seems like this one has a very strong preference for a different filter distribution towards the bulge, so we should make sure we grab the metrics that capture that.

Clarkson et al.: Saturation of bright objects. Twilight time for parallax? huh? Computes volume where things saturate. Do we care about saturation. Keep in mind, there are chip gaps, so you need to dither if you actually want to cover the whole sky at short exposure time.

Brandt et al: AGN DDF. grizy every other night on a long (7-8.5 month) season is their main goal. (note the z band is not always loaded, so this is impossible). They essentially propose a rolling DDF scenario. This would be kinda cool. I think we are close to having the tooling to do it now. Sounds like they have some simulations in prep, maybe we can get them.

## Metrics we should try to get

* The number of young stars in thin disk from Prisinzano et al. I helped with this one, so should be easy to find. Looks like they updated with 3d dust! 

* distance to red clump giants and RR Lyrae from Clarkson et al.

* AGN reverberation mapping recovery from Brandt et al.

## New runs to try out:

* Even more presto color type sims
* DDF with acourdian and rolling styles.

How to pre-schedule a bunch of DDF fields

First, we use `generate_grid.py` to compute the airmass, sky brightness in g, and 5sigma limiting depth in g (assuming 0.7" zenith seeing), and sun altitude for all the fields. Using 15 minutes time steps.

Then with that grid, we can construct an MIP problem to optimize the scheduling of the fields.

The schedule is 1 or 0 for each timeslot (in the case of scheduling 1 field). Also construct a count of observations per night, since that's smaller and faster. Also compute an array of season lables.



set limits on:
 
* sun alitude
* airmass
* sky brightness
* total number of sequences scheduled
* number of sequences in a night
* Possibly also demand a number of possible slots in a night (e.g., do not schedule if there's only 1 15-min slot)


Then we minimize chi-square of the desired and scheduled cumulative distribution function. Can also try to maximize the effective exposure time. 

# Cell Sorting Simulation Prepared for future AI analysis #

----------

## Simulation region and starting condition ##

The simulated area is a 256x256 pixel lattice.

Cells are initialized in a circle of radius 112 centered at the center of the area. The initial cell population
is 50% light 50% dark. They start as squares with a side length equal to 
<a href="https://www.codecogs.com/eqnedit.php?latex=\sqrt{V_{tg}}" target="_blank">
<img src="https://latex.codecogs.com/gif.latex?\sqrt{V_{tg}}" title="\sqrt{V_{tg}}" /></a>, where V<sub>tg</sub> is the 
bigger of the two target volumes.

## Contact energy inequalities ##

For cell sorting contact energies must obey:

* J(L,M) = J(d,M)

* J(L,M) > J(l,l)  => J(l,m) = 2 J(l,l)

* J(l,l) > J(d,l)

* J(d,l) > 0.5 * [ J(d,d)+J(l,l) ] 

* 0.5 * [ J(d,d)+J(l,l) ] > J (d,d)  

* J (d,d) > 0 [ not necessary (if I recall correctly)]

For this I am using:

- J(l,l) = J0 + &Delta;
- J(l,d) = J0 + &delta;
- J(d,d) = J0 - &Delta;
- J(L,M) = 2 J(l,l)

with

- &Delta; > 0; 
- -&Delta; < &delta; <  &Delta;

## Interaction range ##

For this simulations the flip-copy-attempt range is equal to 
the contact energy interaction range.

## Parameters ##

Cells have a target volume and a &lambda; associated.

The parameters I'm varying are:

- V<sub>tg</sub>(l) [for now V<sub>tg</sub>(d) = 
V<sub>tg</sub>(l) ]
- &lambda;(l)
- &lambda;(d)
- &Delta;
- &delta;
- J0
- Interaction range

## Outputs ##

Outputs are generated every 10 time steps. 

- Population number (for low &lambda; cells may and will 
disappear, i.e. die)
- Contact areas: L-L, L-D, D-D. Both totals and means (with error)
- A triplet of: cell ID, cell type, cell center of mass

In addition, every 100 time steps the lattice configuration is saved. 
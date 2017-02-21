#!/usr/bin/python

from rfsim.models import Lineup
from rfsim.parts.generic import (Amplifier, Attenuator, Switch)

# create the lineup object
lineup = Lineup()

# add a bypassable amplifier
bypass1 = Switch(1, 2, (1, 1))
curve_inline = bypass1.create_curve(0.5)
curve_isolation = bypass1.create_curve(40)
bypass1.set_path_insertion_loss((1, 1), [ (1, 1) ], curve_inline)
bypass1.set_path_insertion_loss((1, 1), [ (1, 2) ], curve_isolation)
bypass1.set_path_insertion_loss((1, 2), [ (1, 1) ], curve_isolation)
bypass1.set_path_insertion_loss((1, 2), [ (1, 2) ], curve_inline)
lineup.add(bypass1)
lineup.add(Amplifier(15, 2.5))
bypass2 = Switch(1, 2, (1, 2))
bypass2.set_path_insertion_loss((1, 1), [ (1, 1) ], curve_inline)
bypass2.set_path_insertion_loss((1, 1), [ (1, 2) ], curve_isolation)
bypass2.set_path_insertion_loss((1, 2), [ (1, 1) ], curve_isolation)
bypass2.set_path_insertion_loss((1, 2), [ (1, 2) ], curve_inline)
lineup.add(bypass2)

# add a 3dB attenuator
lineup.add(Attenuator(3))

# add a 6 dB attenuator that loses attenuation at upper frequencies
points = [ (0, 6), (1e9, 5.9), (8e9, 5.7), (9e9, 5), (10e9, 3) ]
lineup.add(Attenuator(points))


# set switch inline
print "Selecting RFC -> RF1"
bypass1.select_path(1, 1)
bypass2.select_path(1, 2)

# print out the gain of the entire lineup
print "gain = %0.2f dB" % lineup.gain(900e6)
print "Noise Figure = %0.2f dB" % lineup.noisefigure(900e6)

# set isolation path
print "Selecting RFC -> RF2"
bypass1.select_path(1, 2)
bypass2.select_path(1, 1)

# print out the gain of the entire lineup
print "gain = %0.2f dB" % lineup.gain(900e6)
print "Noise Figure = %0.2f dB" % lineup.noisefigure(900e6)


#!/usr/bin/python

from rfsim.models import Lineup
from rfsim.parts.generic import (Amplifier, Attenuator)

# create the lineup object
lineup = Lineup()

# add an amplifier
tmp = Amplifier(15, 2.5)
lineup.add(tmp)

# add a 3dB attenuator
lineup.add(Attenuator(3))

# add a 6 dB attenuator that loses attenuation at upper frequencies
points = [ (0, 6), (1e9, 5.9), (8e9, 5.7), (9e9, 5), (10e9, 3) ]
lineup.add(Attenuator(points))

# print out the gain of the entire lineup
print "gain = %0.2f dB" % lineup.gain(900e6)
print "Noise Figure = %0.2f dB" % lineup.noisefigure(900e6)

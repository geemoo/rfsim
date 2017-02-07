#!/usr/bin/python

from rfsim import Lineup
from rfsim.parts.generic import (Amplifier, Attenuator)

# create the lineup object
lineup = Lineup()

# add an amplifier
tmp = Amplifier(15, 1.5)
lineup.add(tmp)

# add a 3dB attenuator
lineup.add(Attenuator(3))

# add a 6 dB attenuator
lineup.add(Attenuator(6))

# print out the gain of the entire lineup
print "gain = %0.2f dBm" % lineup.gain()
#print "Noise Figure = %0.2f" % lineup.noisefigure()


###
# a class that represents the lineup of the rf devices
#
class Lineup(object):

    ###
    # object creator
    #
    def __init__(self):
        self._lineup = [ ]


    ###
    # add a device to the rf lineup
    #
    def add(self, device):
        self._lineup.append(device)


    ###
    # return the total gain of the lineup
    #
    def gain(self, freq):
        total_gain = 0
        for dev in self._lineup:
            total_gain = total_gain + dev.gain(freq) - dev.insertion_loss(freq)

        return total_gain


    ###
    # return the total noisefigure of the lineup
    # - noise figure is a cascaded calculation
    # - F = F1 + (F2 - 1)/G1 + (F3 - 1)/G1G2 + (F4 - 1)/G1G2G3
    #
    def noisefigure(self, freq):
        # test for empty lineup
        if not len(self._lineup):
            return 0

        # remember total gain (in linear, not dB)
        totalgain = 1

        # start with a noise of 1, so that on our first item, when we subtract 1, it works out
        totalnoise = 1

        # loop across all devices in lineup
        for dev in self._lineup:
            # add the noise of thise stage to our total
            totalnoise = totalnoise + ((dev.noisefigure(freq) - 1) / totalgain)

            # add the gain of this device to our total so we can use it next stage
            totalgain = totalgain * dev.linear_gain(freq)

        return totalnoise

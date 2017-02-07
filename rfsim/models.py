
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
            total_gain = total_gain + dev.gain(freq)

        return total_gain

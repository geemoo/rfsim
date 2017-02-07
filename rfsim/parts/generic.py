from rfsim.rfdevice import RFDevice


###
# attenuator class
#
class Amplifier(RFDevice):

    ###
    # constructor
    #
    def __init__(self, gain = None, noisefigure = None):

        # call the constructor
        super(RFDevice, self).__init__()

        # set the gain value if given
        if not (gain is None):
            self._gain = gain

        # set the noisefigure value if given
        if not (noisefigure is None):
            self._noisefigure = noisefigure


    ###
    # return the gain of the object
    #
    def gain(self):
        return self._gain


###
# attenuator class
#
class Attenuator(RFDevice):

    ###
    # constructor
    #
    def __init__(self, atten = None):

        # call the constructor
        super(RFDevice, self).__init__()

        # set the atten value if given
        if not (atten is None):
            self._gain = -atten


    ###
    # return the gain of the object
    #
    def gain(self):
        return self._gain

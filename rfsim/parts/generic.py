import numpy
from scipy.interpolate import interp1d


###
# an abstract class to represent an RF device
#
class RFDevice(object):
    
    ###
    # object creator
    #
    def __init__(self):

        # use None for a default so unset values can be caught and corrected
        self._gain = None
        self._insertion_loss = None
        self._noisefigure = None


    ###
    # create an interpolation object, based off a single value, or a list of values
    #
    # @param values - a single scalar, or a list of (x, y) tuples
    #
    def create_curve(self, values):
        if isinstance(values, list):
            return self._create_curve_from_list(values)
        else:
            return self._create_curve_from_scalar(values)


    ###
    # create an interpolation object, based off a list of values
    #
    # @param values - a list of (x, y) tuples
    #
    def _create_curve_from_list(self, values):
        xlist = [ ]
        ylist = [ ]
        for (x, y) in values:
            xlist.append(x)
            ylist.append(y)

        # interpolate the lists
        return interp1d(xlist, ylist, kind='linear')

    
    ###
    # create an lambda function that returns an np.array of the value
    #
    # @param values - a scalar value
    #
    def _create_curve_from_scalar(self, value):
        return lambda x: numpy.array(value)


    ###
    # set gain method
    # 
    # @param gains - a single scalar value for flat gain curves, or a list of (freq,gain) tuples
    #
    def set_gain(self, gains):
        
        # interpolate the lists
        self._gain = self.create_curve(gains)


    ###
    # return the gain of the object
    #
    # @param freq - the frequency to test at
    # @returns - the interpolated gain value at the frequency specified
    #
    def gain(self, freq):
        return self._gain(freq).item()


    ###
    # returns the gain as a linear value instead of a dB value
    #
    # @param freq - the frequency to test at
    # @returns - the interpolated gain value at the frequency specified
    #
    def linear_gain(self, freq):
        gain = self.gain(freq)

        return pow(10, gain / 10.0)


    ###
    # set the insertion loss of the device
    # 
    # @param iloss - a single scalar value for flat loss curves, or a list of (freq,loss) tuples
    #
    def set_insertion_loss(self, iloss):
        
        # interpolate the lists
        self._insertion_loss = self.create_curve(iloss)


    ###
    # return the insertion loss of the object
    #
    # @param freq - the frequency to test at
    # @returns - the interpolated loss value at the frequency specified
    #
    def insertion_loss(self, freq):
        return self._insertion_loss(freq).item()


    ###
    # returns the noise figure of the device
    # - for devices that don't have gain, the noise figure is the amount of insertion loss
    #
    # @freq - the frequency to test at
    # @returns - the interpolated noisefigure value at the frequency specified
    #
    def noisefigure(self, freq):
        return self.insertion_loss(freq)


###
# Amplifier class
#
class Amplifier(RFDevice):

    ###
    # constructor
    #
    def __init__(self, gain = None, noisefigure = None):

        # call the constructor
        super(Amplifier, self).__init__()
    
        # amplifiers aren't lossy
        self.set_insertion_loss(0)

        if not (gain is None):
            self.set_gain(gain)

        if not (noisefigure is None):
            self.set_noisefigure(noisefigure)
        
    
    ###
    # set noisefigure method
    # 
    # @param noise figure - the noise figure value
    #
    def set_noisefigure(self, noisefigure):

        self._noisefigure = self.create_curve(noisefigure)


    ###
    # returns the noise figure of the device
    # - for devices that have gain, the noise figure curve is specified when the device is created
    #
    # @freq - the frequency to test at
    # @returns - the interpolated noisefigure value at the frequency specified
    #
    def noisefigure(self, freq):
        return self._noisefigure(freq).item()


###
# attenuator class
#
class Attenuator(RFDevice):

    ###
    # constructor
    #
    def __init__(self, atten = None):

        # call the constructor
        super(Attenuator, self).__init__()

        # attenuators don't have gain
        self.set_gain(0)

        # set attens if provided
        if not (atten is None):
            self.set_attenuation(atten)


    ###
    # method to set attenuator curve
    #
    # @param atten - a single attenuation for flat atten curves, or a list of (freq, atten) tuples
    #
    def set_attenuation(self, atten):
        self.set_insertion_loss(atten)


    ###
    # return the attenuation at a frequency
    #
    def attenuation(self, freq):
        return self.insertion_loss(freq)


###
# DC Block class
#
class DCBlock(Attenuator):

    ###
    # constructor
    #
    def __init__(self, inloss = None):

        # call the constructor
        super(DCBlock, self).__init__(inloss)


###
# Switch class
#
class Switch(Attenuator):

    ###
    # constructor
    #
    def __init__(self, mode = None):

        # call the constructor
        super(Switch, self).__init__()

        # record switch mode (in, out, isolation)
        if mode is None:
            self._mode = 'in'
        else:
            self._mode = mode



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
    # @freq - the frequency to test at
    # @returns - the interpolated gain value at the frequency specified
    #
    def gain(self, freq):
        return self._gain(freq).item()


###
# attenuator class
#
class Amplifier(RFDevice):

    ###
    # constructor
    #
    def __init__(self, gain = None, noisefigure = None):

        # call the constructor
        super(Amplifier, self).__init__()
    
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
    # return the noisefigure of the object
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
    def __init__(self, attens = None):

        # call the constructor
        super(Attenuator, self).__init__()

        # set attens if provided
        if not (attens is None):
            self.set_attenuation(attens)


    ###
    # method to set attenuator curve
    #
    # @param atten - a single attenuation for flat atten curves, or a list of (freq, atten) tuples
    #
    def set_attenuation(self, atten):
        # if atten is a scalar, negate the value
        if not isinstance(atten, list):
            gains = -atten
        # if atten is a list, negate all the values
        else:
            gains = [ ]
            for (f, a) in atten:
                gains.append((f, -a))
            
        # now create the curve
        self.set_gain(gains)


    ###
    # return the attenuation at a frequency
    #
    def attenuation(self, freq):
        # return the gain, negated
        return -(self._gain(freq).item())


    ###
    # noise figure of an attenuator is just the attenuation value
    #
    # @freq - the frequency to test at
    # @returns - the interpolated noisefigure value at the frequency specified
    #
    def noisefigure(self, freq):
        return self.attenuation(freq).item()


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



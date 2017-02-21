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
    # @param inports - number of ports going into the switch, 1 or greater
    # @param outports - number of ports going out of the switch, 1 or greater
    # @param path_used - the path that is considered inline
    #
    def __init__(self, inports, outports, path_used = (1, 1)):

        # call the constructor
        super(Switch, self).__init__()

        # record port counts
        if inports < 1:
            raise Error("inports must be 1 or greater")
        self._inports = inports
        if outports < 1:
            raise Error("outports must be 1 or greater")
        self._outports = outports

        # initialize the attribute dictionaries
        self._insertion_loss = { }

        # record path used
        self.set_used_path(path_used[0], path_used[1])
    
        # select path 1, 1 by default
        self.select_path(1, 1)


    ###
    # set the path that is considered to be inline in the lineup
    #
    # @param inport - the port on the input side
    # @param outport - the port on the output side
    #
    def set_used_path(self, inport, outport):
        # make sure inport and outport are valid
        if (inport < 1) or (inport > self._inports):
            raise Error("invalid inport value: %s" % inport)
        if (outport < 1) or (outport > self._outports):
            raise Error("invalid outport value: %s" % outport)

        # record the path
        self._used_path = (inport, outport)

    
    ###
    # return the path currently used
    #
    # @returns - (inport, outport) as a tuple
    def used_path(self):
        return self._used_path


    ###
    # set the currently selected path in the switch from inports to outports
    #
    # @param inport - the port on the input side
    # @param outport - the port on the output side
    #
    def select_path(self, inport, outport):
        # make sure inport and outport are valid
        if (inport < 1) or (inport > self._inports):
            raise Error("invalid inport value: %s" % inport)
        if (outport < 1) or (outport > self._outports):
            raise Error("invalid outport value: %s" % outport)

        # record the path
        self._selected_path = (inport, outport)


    ###
    # set a insertion loss curve for the specified path
    # 
    # @param selected - what (in,out) path must be selected to use this curve
    # @param paths - list of (in,out) paths to use this curve for
    # @param curve - the loss curve to use
    #
    def set_path_insertion_loss(self, selected, paths, curve):
        # initialize the dictionary if it hasn't been set
        if not (selected in self._insertion_loss):
            self._insertion_loss[selected] = { }

        # set the curve for each path
        for p in paths:
            self._insertion_loss[selected][p] = curve


    ###
    # return the gain of the switch
    #
    # @param freq - the freq to return the gain at
    # @returns - the gain at the frequency
    #
    def gain(self, freq):
        return 0


    ###
    # return the insertion loss of the switch
    #
    # @param freq - the freq to return the gain at
    # @returns - the insertion loss at the frequency
    #
    def insertion_loss(self, freq):
        # get the curve
        curve = self._insertion_loss[self._selected_path][self._used_path]

        # return the value
        return curve(freq)


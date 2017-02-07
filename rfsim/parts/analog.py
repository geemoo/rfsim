from parts.generic import (Switch)


class HMC1118(Switch):

    ###
    # constructor for hmc1118 class
    #
    # @param mode - the mode to configure the switch in, can be one of 'in', 'out', or 'isolation'
    #
    def __init__(self, mode = None):
        super(HMC1118, self).__init__(mode)
    
        # init curves for all modes
        self.init_modes()

        # setup curves for current mode
        self.set_mode(mode)
    

    ###
    # setup the characteristic curves for the mode specified
    #
    # @param mode - the mode to configure the switch in, can be one of 'in', 'out', or 'isolation'
    #
    def setup_mode(self, mode):
        self._gain = self._gain_modes[mode]


    ###
    # initialize all our curves for each mode
    #
    def init_modes(self):
        # init dictionary
        self._gain_modes = { }

        # initialize in mode
        freqlist = range(0, int(14e9), int(1e9))
        attenlist = [ 0.4, 0.5, 0.52, 0.54, 0.56, 0.58, 0.60, 0.6, 0.6, 0.65, 0.7, 1.2, 1.4, 1.3, 1.4 ] 
        self._gain_modes['in'] = scipy.interp1d(freqlist, attenlist)

        # initialize out mode
        attenlist = [ 78, 56, 52, 49, 48, 47, 48, 52, 57, 42, 36, 31, 27, 24, 22 ]
        self._gain_modes['out'] = scipy.interp1d(freqlist, attenlist)

        # initialize isolation mode
        attenlist = [ 81, 67, 60, 55, 50, 45, 43, 39, 36, 32, 29, 25, 23, 20, 19 ]
        self._gain_modes['isolation'] = scipy.interp1d(freqlist, attenlist)


from rfsim.parts.generic import Switch


class HMC1118(Switch):

    def __init__(self):
        
        # create an SPDT switch
        super(Switch, self).__init__(1, 2)

        # create the insertion loss curve, each list item is a (freq, loss) point
        loss_curve = self.create_curve([ (0e9, 0.5), (8e9, 0.5), (9e9, 0.6), (10e9, 0.7), (11e9, 1.2), (12e9, 1.4), (13e9, 1.3), (14e9, 1.4) ])

        # set that curve for the selected paths
        self.set_path_insertion_loss((1, 1), [ (1, 1) ], loss_curve)
        self.set_path_insertion_loss((1, 2), [ (1, 2) ], loss_curve)
    
        # create the isolation curve
        loss_curve = self.create_curve([ (0e9, 80), (1e9, 57), (2e9, 52), (3e9, 50), (4e9, 47), (5e9, 46), (6e9, 47), (7e9, 51), (8e9, 57), (9e9, 40), (10e9, 36), (11e9, 30), (12e9, 28), (13e9, 23), (14e9, 21) ])

        # set that curve for isolation paths
        self.set_path_insertion_loss((1, 1), [ (1, 2) ], loss_curve)
        self.set_path_insertion_loss((1, 2), [ (1, 1) ], loss_curve)

        # select path RFC->RF1 by default
        self.select_path(1, 1)

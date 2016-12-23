import numpy.random as npr
import sys

from SwingyMonkey import SwingyMonkey


class plan:

    def __init__(self,j_at=-1):
        self.jumps={};
        self.jumpStrengh=npr.poisson(15);

        #print "init";


    def action_callback(self, game):
        state=game.get_state();
        if state['time'] in self.jumps:
            return self.jumps[state['time']]
        else:
            return 0

    def reward_callback(self, state):
        return;



    

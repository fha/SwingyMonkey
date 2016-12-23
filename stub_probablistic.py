import numpy.random as npr
import sys

from SwingyMonkey import SwingyMonkey
from inference import inference

class Learner:

    def __init__(self):
        self.game=None
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.qvalues={}        
        self.learning_rate = 0.2
        self.discount_factor = 0.9
        self.jumps={0:0};

        #print "init";

    @staticmethod
    def binned_state(state):
        
        #[not needed _ gap is always 200 ] gap = (state['tree']['top']-state['tree']['bot'])/50 
        
        #vertical position of the monkey relative to the tree --> captures the position of the monkey relative to the gap location where it needs to go through
        rel_pos= (state['tree']['top']-state['monkey']['top'])/100
        
        #horizental distance between monkey and the tree --> captures the distance of the monkey to the tree into the state
        distance_from_tree=(state['tree']['dist'])/100
        
        #vertical velocity of the Monkey --> captures the speed of the monkey and its vertical direction
        vel=state['monkey']['vel']/20       
        
        #Postion of the top of the monkey --> captures top and bottom boundaries into the state
        heads_up=state['tree']['top']/100;
                
        #[score is useless to add in the state] score=state['score']

        #return the coupling of the calculated values as a key to the Q-Value dictionary
        a= tuple([ heads_up,rel_pos,vel,distance_from_tree])
        return a; 

    def reset(self):
        
        #print "Epoch {0} score {1} | the number of states: {2}".format(ii,self.last_state['score'],len(self.qvalues));
        
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def infer(self):
        inf_tool=inference(self.game);
        print 'time is ',self.game.time_tick;
        self.jumps=inf_tool.get_action();



    def action_callback(self, game):
        state=game.get_state();
        print 'score', state['score']
        #print self.jumps;
        if state['time'] in self.jumps:
            #print "i will ", self.jumps[state['time']]
            return self.jumps[state['time']];




    def reward_callback(self, state):
        return;
iters = 1
learner = Learner()
for ii in xrange(iters):

    # Make a new monkey object.
    learner.game = SwingyMonkey(display=True,
                         sound=True,            # Don't play sounds.
                         text="Epoch %d" % (ii), # Display the epoch on screen.
                         tick_length=0,          # Make game ticks super fast.
                         action_callback=learner.action_callback,
                         reward_callback=learner.reward_callback)
    
    
    # Loop until you hit something.
    continu=True;
    while continu:
        learner.infer();
        continu=learner.game.game_loop();
        

    # Reset the state of the learner.
    #learner.reset()



    

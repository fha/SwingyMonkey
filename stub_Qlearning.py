import numpy.random as npr
import sys

from SwingyMonkey import SwingyMonkey

class Learner:

    def __init__(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.qvalues={}        
        self.learning_rate = 0.3
        self.discount_factor = 0.9

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
        
        print "Epoch {0} score {1} | the number of states: {2}".format(ii,self.last_state['score'],len(self.qvalues));
        
        self.last_state  = None
        self.last_action = None
        self.last_reward = None


    def action_callback(self, state):
        '''Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.'''

        # You might do some learning here based on the current state and the last state.

        # You'll need to take an action, too, and return it.
        # Return 0 to swing and 1 to jump.

        #task1 ---> UPDATE Q VALUES

        #set a random (jump/no jump) if this is the first time step
        if(self.last_state==None):
            new_action = npr.rand() < 0.1
            self.last_action = new_action
            self.last_state  = state
            return new_action;

        #get the keys of the previous and current states as well as rward
        L_state=Learner.binned_state(self.last_state);
        C_state=self.binned_state(state);
        reward=self.last_reward;
        last_Q_index=L_state+(self.last_action,)        
        current_Q_index_0=C_state+(False,)
        current_Q_index_1=C_state+(True,)

        #getting max next action Q-Value value
        current_Q_0=self.qvalues.get(current_Q_index_0);
        if(current_Q_0==None):            
            current_Q_0=0;
            
        current_Q_1=self.qvalues.get(current_Q_index_1);
        if(current_Q_1==None):
            current_Q_1=0;

        if(current_Q_0>current_Q_1): 
            state_max_Q=current_Q_0;
        else:
            state_max_Q=current_Q_1;


        #getting the Q-value of the last state
        old_q = self.qvalues.get(last_Q_index)
        if(old_q==None):
            old_q=0;
        #calculateing and updating previus state/action Qvalue 
        
        #Formula for updating Q-VALUES
        
        newQ=old_q +  (self.learning_rate * (reward + (self.discount_factor * state_max_Q )- old_q ));

        self.qvalues[last_Q_index] = newQ ; 

        #pick action with largest Q-value
        if(current_Q_0>current_Q_1):
            new_action= False;
        elif(current_Q_0<current_Q_1):
            new_action= True;
        else: #if both Q-values are the same -->pick a random action
            new_action = npr.rand() < 0.1

        #keeping the state in memory for the next state
        self.last_action = new_action
        self.last_state  = state

        if(newQ > 10e10):
            print "Caution: very large Q-Value";

        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''
        self.last_reward = reward


iters = 10000
learner = Learner()

for ii in xrange(iters):

    # Make a new monkey object.
    swing = SwingyMonkey(sound=False,            # Don't play sounds.
                         text="Epoch %d" % (ii), # Display the epoch on screen.
                         tick_length=1,          # Make game ticks super fast.
                         action_callback=learner.action_callback,
                         reward_callback=learner.reward_callback)

    # Loop until you hit something.
    while swing.game_loop():
        pass

    # Reset the state of the learner.
    learner.reset()



    

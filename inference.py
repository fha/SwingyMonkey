from SwingyMonkey import SwingyMonkey
import numpy as np
import math
import sys
import pygame as pg
import numpy.random as npr
import copy
from plan import plan 
import operator

class inference:

    def __init__(self,game,start_game=None,start_state=None):
        
        self.start_point= SwingyMonkey(tick_length=0);
        self.start_point.copy(game);
        #self.dream.game_loop();




    def no_action_tdeath(self):
    	i=1;
    	dream=SwingyMonkey(tick_length=0,display=False);
    	dream.copy(self.start_point);

    	#print dream.get_state()
    	while dream.game_loop_no_render(0) and dream.get_state()['tree']['dist']>0:
        	i+=1;
        	#print dream.get_state()
        #print i;
        
        return i;


    def simulate_plan(self,it,plan):
    	dream=SwingyMonkey(tick_length=0,action_callback=plan.action_callback,display=False);
    	dream.copy(self.start_point)
    	alive=False;

    	for i in range(0,it):

			dream.game_loop_no_render(plan.jumpStrengh);
			if not dream.alive:
				return 0;

    	if dream.alive:
    		return 1;
    	else:
    		return 0;


    def model(self,iteration,samples,last_result):
		simulation_horizon=self.no_action_tdeath();
		simulation_horizon=10;
		action_horizon=5;

		#make a plan
		p=self.get_sample('MCMC',action_horizon,iteration,samples,last_result)
		#simulate

		a=self.simulate_plan(simulation_horizon,p)
		#print [p.jumps,a]
		return [p.jumps,a];
		
    	

    def get_action(self):
    	
    		
    	if self.start_point.time_tick==0:

    		return {0:0};
    	
    	else:
    		simulation_horizon=self.no_action_tdeath();
    		
    		ct=self.start_point.get_state()['time'];
    		if(simulation_horizon>5):
    			return {ct:0};
    		else:
	
				pdf={};
				samples=[];
				i=0;
				last_result=0;
				while True:
					result=self.model(i,pdf,last_result);
					sample=tuple([t[1] for t in sorted(result[0].items(), key=operator.itemgetter(0))]);
					if sample in pdf:
						pdf[sample][result[1]]+=1;
					else:
						pdf[sample]=[0,0]; 
						pdf[sample][result[1]]+=1; 
					
					samples.append(sample);
					last_result=[sample,result[1]];
					if(pdf[sample][1]>=5) or i>100:
						return self.returned_plan(pdf,self.start_point.get_state()['time']);
					i+=1;

    def returned_plan(self,pdf,ct):
		max_p=0;
		max_plan=[];
		#marginalize over the future
		marginal=np.zeros([2,2]);

		for i in pdf:
			print i,pdf[i]
			marginal[i[0],0]+=pdf[i][0];
			marginal[i[0],1]+=pdf[i][1];

		marginal[1,:]=marginal[1,:]/np.sum(marginal[1,:]);
		marginal[0,:]=marginal[0,:]/np.sum(marginal[0,:]);
		marginal=np.nan_to_num(marginal);
		#print marginal;
		arg_max=np.argmax(marginal,axis=0)

		return {ct:arg_max[1]};

    def get_sample(self,type_,horizon,iteration,samples,last_result):
		ct=self.start_point.get_state()['time'];
		p=plan();
		p.jumpStrengh=npr.poisson(15)
		if type_=="rejection":	
			for i in range(0,horizon):
				j=np.random.binomial(1,0.4)
				p.jumps[ct+i]=j;
			return p;
		elif type_=="enumerate":
			for i in range(0,horizon):
				it_bin=bin(int(iteration%math.pow(2,horizon)))[2:].zfill(horizon)
				p.jumps[ct+i]=int(it_bin[i]);
			return p;
		elif type_=="enumerate-one":
			for i in range(0,horizon):
				it_bin=math.pow(2,iteration%horizon);
				p_bin=bin(int(it_bin))[2:].zfill(horizon);
				p.jumps[ct+i]=int(p_bin[i]);
			return p;
		elif type_=="MCMC":
			if len(samples)==0:
				for i in range(0,horizon):
					p.jumps[ct+i]=0;
				return p;
			else:
				last_arr=np.array(last_result[0]);
				if  last_result[1]==0:
					#add or remove a jump
					new_sample=list(last_arr[1:])+list([1-last_arr[0]]);
					#print last_arr,'-->',new_sample
					#print 'to this many jumps',no_jumps
					for i in range(0,horizon):			
						p.jumps[ct+i]=new_sample[i];
					return p;
				else:
					for i in range(0,horizon):
						p.jumps[ct+i]=last_arr[i];
					return p;





#need a enumerate sampler, if MCMC and rejection that would be great
if __name__ == '__main__':
    
    print 'dont call inference directly';

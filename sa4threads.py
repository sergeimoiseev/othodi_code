import random
import math
import logging
logger = logging.getLogger(__name__)

def P(prev_score,next_score,temperature):
    if next_score > prev_score:
        return 1.0
    else:
        return math.exp( -abs(next_score-prev_score)/temperature )

class ObjectiveFunction:
    '''class to wrap an objective function and 
    keep track of the best solution evaluated'''
    def __init__(self,objective_function):
        self.objective_function=objective_function
        self.best=None
        self.best_score=None
    
    def __call__(self,solution):
        score=self.objective_function(solution)
        if self.best is None or score > self.best_score:
            self.best_score=score
            self.best=solution
            logger.info('new best score: %f',self.best_score)
        return score

def kirkpatrick_cooling(start_temp,alpha):
    T=start_temp
    while True:
        yield T
        T=alpha*T

def anneal(init_function,move_operator,objective_function,max_evaluations,start_temp,alpha):
        
    # LOG_FNAME = 'tsp_log_%s_%s_%s.log' % (max_evaluations,start_temp,alpha)
    # with open('last_log_file_name.txt','w') as log_fname_file:
    #     log_fname_file.write(LOG_FNAME)
    # with open(LOG_FNAME,'w') as logf:
    #     pass

    # wrap the objective function (so we record the best)
    objective_function=ObjectiveFunction(objective_function)
    
    current=init_function()
    current_score=objective_function(current)
    num_evaluations=1
    
    # cooling_schedule=myexp_cooling(start_temp,alpha)
    cooling_schedule=kirkpatrick_cooling(start_temp,alpha)
    
    logger.info('anneal started: t =%.4f, score=%f' % (start_temp,current_score))
    # logger.info('range(1,max_evaluations,max_evaluations//10) >>> %s',str(range(1,max_evaluations,max_evaluations//10)))
    
    for temperature in cooling_schedule:
        done = False
        # examine moves around our current position
        for next_ in move_operator(current):
            if num_evaluations >= max_evaluations:
                done=True
                break
            
            next_score=objective_function(next_)
            num_evaluations+=1
            
            # probablistically accept this solution
            # always accepting better solutions
            p=P(current_score,next_score,temperature)
            if random.random() < p:
                current=next_
                current_score=next_score
                break
            if num_evaluations in range(1,max_evaluations,max_evaluations//10):
                logger.debug("step %d: t =%.4f;curr score = %.4f\n"%(num_evaluations,temperature,current_score))
        # see if completely finished
        if done: break
        # see if temp is 0 - restart anneal from current state
        if temperature<0.01: break
    
    best_score=objective_function.best_score
    best=objective_function.best
    logger.info('final temperature: %f',temperature)
    logger.info('anneal finished: num_evaluations=%d, best_score=%f',num_evaluations,best_score)
    return (num_evaluations,best_score,best)
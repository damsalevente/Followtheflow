from epynet import Network
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import logging


class NetworkAgent:

    def __init__(self, filename='anytown_master.inp'): 

        # load network
        self.network = Network(filename)
        self.network.solve()

        # for control
        self.speed_limit = (0.7, 1.2)

        # danger zone 
        self.junction_threshold = (15, 120)
        self.state = None

        # function to get the effeciency of the pump(s) 
        self.eff = None

        # speed increase/decrease resolution 
        self.stepsize = 0.1
        self.network.solve()
        self._calc_effeciency('E1')


    def _calc_effeciency(self, curve_id):
        curve = None
        for x in self.network.curves:
            if curve_id in x.uid:
                flow = [ value[0] for value  in x.values] 
                y = [value[1] for value in  x.values]
                curve = np.poly1d(np.polyfit(flow,y,4))
        if not curve:
            logging.info('no curve found with id{}'.format(curve_id))
        self.eff = curve



    def reset(self):
        # epynet has its own reset function
        # self._calc_effeciency('E1')
        #optimize  
        from scipy.optimize import minimize
        # initial guess is 0.8 thats the speed
        self.res = minimize(self.find_opt,1.2, method='Nelder-Mead', options={'disp':True}, bounds = self.speed_limit)
        print(self.res.x)
        self.network.reset()

    def find_opt(self, x):
        """
        x : pump's speed
        returns: effeciency
        """
        # change speed 
        self.network.pumps['78'].speed = x 
        self.network.solve()
        eff = self.calc_eff()
        # - sign because we need the maximum value 
        return - eff


    def step(self):
        x = self.network.solve()
        print('solve function returns: {}'.format(x))

    
    def calc_eff(self):

        # get only one pump with id 78
        # complicated networks will be harder than this
        flow  = self.network.pumps['78'].flow
        print('flow is: {}'.format(flow))

        speed = self.network.pumps['78'].speed

        true_flow = float(flow/speed)

        return self.eff(true_flow)


    def junction_head(self):
        return list(self.network.junctions.head)


    def junction_demand(self):
        return list(self.network.junctions.demand)


    def junction_pressure(self):
        return list(self.network.junctions.pressure)


    def _action_increase_speed(self):
        # check if it's within the limits
        if self.network.pumps['78'].speed + self.stepsize > self.speed_limit[1]:
            return
        self.network.pumps['78'].speed += self.stepsize


    def _action_decrease_speed(self):
        if self.network.pumps['78'].speed - self.stepsize < self.speed_limit[1]:
            return
        self.network.pumps['78'].speed -= self.stepsize



if __name__ == '__main__':
    na  = NetworkAgent('anytown_master.inp')
    na.reset()
    junctions = [] 
    demands = [] 

    press = na.junction_pressure()
    print(press)

    for i in range(10):
        """ step and increase speed """
        na._action_increase_speed()
        print('junction head')
        junction = na.junction_head()
        print('junction demand')
        jd = na.junction_demand()
        junctions.append(junction)
        demands.append(jd)
        na.step()

    for i in range(10):
        """ step and increase speed """
        na._action_decrease_speed()
        junction = na.junction_head()
        jd = na.junction_demand()
        junctions.append(junction)
        demands.append(jd)
        na.step()

    na.reset()

    print(junctions[0]) 
    print(demands[0])
    print(junctions[1])

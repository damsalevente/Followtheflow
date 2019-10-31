import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
import networkagent
import logging

class ControlEnv(gym.Env):
  metadata = {'render.modes': ['human']}
  """ 
  Actions: 
    Type: Dicrete(2)
    NUM Action
    0   forward
    1   backward

  State: 
    22 junction head

  Reward:
    Effeciency of the pump(s)
  """

  def __init__(self):

      # increase/decrease speed 
      self.action_space = spaces.Discrete(2)

      # solve it for 10 times 
      self.steps_available = 10

      self.network = networkagent.NetworkAgent()
      self.network._calc_effeciency('E1')
      logging.info('effeciency curves set')

      
      self.n = len(self.network.junction_head())
      # space will be 1 * 22
      self.min = self.network.junction_threshold[0]
      self.max = self.network.junction_threshold[1]

      # 22 junctions head
      self.low = np.array([self.min for i in range(self.n)])
      self.high = np.array([self.max for i in range(self.n)])

      self.observation_space = spaces.Box(low=self.low,high=self.high)
      self.action_space = spaces.Discrete(2)


      self.done = False

      self.viewer= None



  def step(self, action):
      """ 
      agent did something
      next timestamp 
      returns observation, reward, done, info 
      """
      info = {}
      info['is_success'] = False
      self.steps_available -= 1 

      reward = 0

      # make the move
      if (action == 0):
          self.network._action_increase_speed()  
          info['action'] = 'speed '
      else:
          self.network._action_decrease_speed()
          info['action'] = 'slow' 

      self.network.step()
    
      reward = self.network.calc_eff()

      if self.steps_available == 0:
          self.done = True

      state = self.network.junction_head()
         
      return  state, reward, self.done, info


  def reset(self):
      """
      returns observation and resets env state
      """
      self.steps_available = 10
      self.done = False
      
      self.network.reset()

      state = self.network.junction_head()

      return state

  def render(self, mode='human', close=False):
      raise NotImplementedError
      


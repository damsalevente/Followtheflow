import gym
from time import sleep


from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN


env = gym.make('gym_control:control-v0')

model = DQN(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10)


obs = env.reset()

for _ in range(10):
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action) 
    print('---') 
    print('observation:  {}\nreward: {}\n info: {}'.format(obs, reward, info)) 
    if done:
        print('END ')
        env.reset()

env.close()

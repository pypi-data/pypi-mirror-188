import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

class Moral_HazardEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    # low 参数表示该维度的最低值，high 参数表示该维度的最高值。每个维度都可以有不同的含义，例如：
    # 第1维 - 私人收益
    # 第2维 - 项目成功概率
    # action_space :
    #0 - 不努力
    #1 - 努力
    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,))
        self.action_space = spaces.Discrete(2)
        self.additional_info = None
        self.state = 0.5
    def transition(self):
        pass
    def reward(self, x, a, y):
        pass
    def step(self, action):
        info = {}
        truncated = False
        terminated = False
        if action == 1:
            # If the agent takes the risky action, there's a 0.5 chance of a positive outcome
            reward = random.choices([-1, 1], weights=[0.5, 0.5])[0]
        else:
            reward = 0
        self.state = random.uniform(0, 1)
        return  self.state,reward, terminated, truncated, info
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        observation = 0
        info = {}
        #print(observation)
        return observation,info  # reward, done, info can't be included
    def render(self, mode="human"):
        pass
    def close(self):
        pass
if __name__ == '__main__':
    env = Moral_HazardEnv()

# Reset the environment to get the initial state
    obs,_= env.reset()

# Take 10 steps in the environment
    for i in range(10):
        action = env.action_space.sample() # select a random action
        obs, reward, done,_,info = env.step(action) # take a step in the environment
        print("Observation at step {}: {}".format(i, obs))
        print("Reward at step {}: {}".format(i, reward))
        
        if done:
            print("Episode finished after {} steps".format(i+1))
            break
import gymnasium as gym
from gymnasium import spaces
import numpy as np
class Moral_HazardEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    # low 参数表示该维度的最低值，high 参数表示该维度的最高值。每个维度都可以有不同的含义，例如：
    # 第1维 - 私人收益
    # 第2维 - 就业率
    # 第3维 - 通货膨胀率
    # action_space :
    #0 - 不努力
    #1 - 努力
    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=100, shape=(3,))
        self.action_space = spaces.Discrete(2)
        self.reward_range = (-1, 1)
        self.additional_info = None
    def transition(self):
        pass
    def reward(self, x, a, y):
        pass
    def step(self, action):
        observation = self.observation_space.sample()
        reward = 1.0
        terminated = True
        info = {}
        truncated = False
        return observation, reward, terminated, truncated, info
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        observation = self.observation_space.sample()
        info = {}
        #print(observation)
        return observation,info  # reward, done, info can't be included
    def render(self, mode="human"):
        pass
    def close(self):
        pass
if __name__ == '__main__':
    a=Moral_HazardEnv()
    print(a.observation_space.shape[0])
    print(a.action_space)
import gymnasium as gym
from gymnasium import spaces
import numpy as np
class Moral_HazardEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    # low 参数表示该维度的最低值，high 参数表示该维度的最高值。每个维度都可以有不同的含义，例如：
    # 第1维 - 私人收益
    # 第2维 - 项目成功概率
    # action_space :
    #0 - 不努力
    #1 - 努力
    def __init__(self):
        self.observation_space = spaces.Box(low=np.array([0, 0]), high=np.array([1, 1]), dtype=np.float32, shape=(2,))
        self.action_space = spaces.Discrete(2)
        self.additional_info = None
    def transition(self):
        pass
    def reward(self, x, a, y):
        pass
    def step(self, action):
        if action == 0: # 努力
            private_profit = np.random.normal(0.5, 0.1) # 私人收益在 0.5 左右波动
            project_success = np.random.normal(0.8, 0.1) # 项目成功概率在 0.8 左右波动
        else: # 卸责
            private_profit = np.random.normal(0.7, 0.1) # 私人收益在 0.7 左右波动
            project_success = np.random.normal(0.6, 0.1) # 项目成功概率在 0.6 左右波动
        reward = private_profit + project_success # 计算总回报
        done = False # 环境不结束
        info = {}
        truncated = False
        terminated = False
        return np.array([private_profit, project_success]),reward, terminated, truncated, info
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
    n_observations = a.observation_space.shape[0]
    n_actions = a.action_space.n    
    print(a.action_space)
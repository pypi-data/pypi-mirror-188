import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import namedtuple, deque
import random
import math
import matplotlib
import matplotlib.pyplot as plt
from itertools import count
from cpagym.envs.moral_hazard_env import *
class MoralHazardEnv(gym.Env):
    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,))
        self.action_space = spaces.Discrete(2)
        self.state = 0.5

    def step(self, action):
        if action == 1:
            # If the agent takes the risky action, there's a 0.5 chance of a positive outcome
            reward = random.choices([-1, 1], weights=[0.5, 0.5])[0]
        else:
            reward = 0
        self.state = random.uniform(0, 1)
        done = False
        return self.state, reward, done, {}

class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
def train_dqn(env, model, optimizer, num_episodes, epsilon_decay):
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            # Choose an action using epsilon-greedy exploration
            if random.random() < epsilon_decay:
                action = env.action_space.sample()
            else:
                state_tensor = torch.tensor([state], dtype=torch.float32)
                q_values = model(state_tensor)
                action = q_values.argmax().item()
            next_state, reward, done,_, _ = env.step(action)
            # Update the model using the Bellman equation
            next_state_tensor = torch.tensor([next_state], dtype=torch.float32)
            q_values_next = model(next_state_tensor)
            q_target = reward + 0.99 * q_values_next.max()
            q_values[0, action] = q_target
            loss = ((q_values - q_values_next) ** 2).mean()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            state = next_state

def main():
    env = Moral_HazardEnv()
    model = DQN(1, 128, 2)
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    num_episodes = 1000
    epsilon_decay = 1.0
    epsilon_min = 0.01
    for episode in range(num_episodes):
        epsilon_decay = max(epsilon_min, epsilon_decay * 0.999)
        train_dqn(env, model, optimizer, 1, epsilon_decay)
    epsilon_decay = 0
    total_reward = 0
    for episode in range(100):
        state = env.reset()
        done = False
        while not done:
            state_tensor = torch.tensor([state], dtype=torch.float32)
            q_values = model(state_tensor)
            action = q_values.argmax().item()
            next_state, reward, done,_, _ = env.step(action)

            total_reward += reward
            state = next_state
    
    # Print the average reward over 100 episodes
    print(f"Average reward: {total_reward / 100}")
if __name__ == '__main__':
    main()
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
class Moral_HazardEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
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
import random
import numpy as np
import gym
import torch
import torch.nn as nn
import torch.optim as optim

# Define the neural network for the Q-network
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        x = self.fc(x)
        return x

# Choose the device to run the model on (GPU if available)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Define the hyperparameters
num_episodes = 50
max_timesteps = 50
learning_rate = 0.001
discount_factor = 0.97
# Initialize the environment
env = Moral_HazardEnv()

# Get the state and action dimensions
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
# Initialize the Q-network
q_network = DQN(state_dim, action_dim).to(device)
# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(q_network.parameters(), lr=learning_rate)
# Initialize the memory to store transitions
memory = []
# Train the Q-network
for episode in range(num_episodes):
    state,info = env.reset()
    total_reward = 0
    state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
    for timestep in range(max_timesteps):
        # Convert the state to a tensor and add a batch dimension

        # Get the Q-values for each action
        q_values = q_network(state)

        # Choose an action based on an epsilon-greedy policy
        epsilon = 0.1
        if random.uniform(0, 1) > epsilon:
            action = torch.argmax(q_values).item()
        else:
            action = random.choice(list(range(action_dim)))
        # Take a step in the environment
        next_state, reward, done, _, _ = env.step(action)
        total_reward += reward
        # Store the transition in memory
        memory.append((state, action, reward, next_state, done))
        state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0).to(device)
        # Update the Q-network
        if len(memory) > 1000:
            # Sample a random batch of transitions from memory
            batch_indexes = np.random.choice(len(memory), size=32)
            batch = [memory[i] for i in batch_indexes]

            # Extract the states, actions, rewards, next states, and done flags
            states = torch.tensor([b[0] for b in batch], dtype=torch.float32).to(device)
            actions = torch.tensor([b[1] for b in batch], dtype=torch.float32).to(device)
            rewards = torch.tensor([b[2] for b in batch], dtype=torch.float32).to(device)
            next_states = torch.tensor([b[3] for b in batch], dtype=torch.float32).to(device)
            dones = torch.tensor([b[4] for b in batch], dtype=torch.float32).to(device)
            done_mask = (1.0 - dones.float())
            
# Compute the Q-values for the next states
            next_q_values = q_network(next_states)

            # Select the Q-value for the selected action
            selected_next_q_values = next_q_values.gather(1, actions.unsqueeze(-1)).squeeze(-1)

            # Compute the target Q-value
            target_q_values = rewards + discount_factor * selected_next_q_values * done_mask

            # Compute the current Q-value
            current_q_values = q_values.gather(1, actions.unsqueeze(-1)).squeeze(-1)

            # Compute the loss
            loss = criterion(current_q_values, target_q_values)

            # Backpropagate the error and update the model's parameters
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()            
            
            
         
         
         
         
         
         
         
         
         
         
         
         
    print("Episode: {}, Total reward: {}".format(episode, total_reward))





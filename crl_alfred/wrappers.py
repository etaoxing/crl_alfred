import gym
import numpy as np

class ChannelConcatGoal(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
    
        obs_shape = env.observation_space['frame'].shape
        obs_shape = (obs_shape[0], obs_shape[1], int(obs_shape[2] * 2))
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=obs_shape, dtype=np.uint8)


    def observation(self, obs):
        return np.concatenate([obs['frame'], obs['goal_frame']], axis=-1)

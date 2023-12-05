
"""
what's gym? providing a standard API to communicate between learning algorithms and environments

use pip install gym[all] to install all dependencies.

@see https://github.com/openai/gym
@since 2023年12月5日16:59:35
"""

import gym
# Initializing environments is very easy in Gym and can be done via:
# 报错 AttributeError: module 'gym.envs.box2d' has no attribute 'LunarLander'  pip install Box2D
env = gym.make("LunarLander-v2")
env.reset()

done = False
while not done:
    action = env.action_space.sample()
    observation, reward, done, _ = env.step(action)
    env.render()

env.close()

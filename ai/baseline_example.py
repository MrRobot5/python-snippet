
"""
quickstart

Here is a quick example of how to train and run PPO2 on a cartpole environment
https://stable-baselines.readthedocs.io/en/master/guide/quickstart.html


Python 3.6.1
    版本问题. 如果 Python 版本过高，需要降级 或者 使用 Anaconda
    https://www.python.org/downloads/release/python-361/

Baselines
    pip install stable-baselines==2.10.0

    Baselines requires python3 (>=3.5) with the development headers.
    Stable-Baselines supports Tensorflow versions from 1.8.0 to 1.15.0, and does not work on Tensorflow versions 2.0.0 and above.5

    可能会遇到 opencv-python 级联安装错误，单独安装 opencv-python， 再尝试安装 stable-baselines

gym
    pip install gym==0.17.1

tensorflow
    pip install tensorflow-gpu==1.15.2

    如果使用 3.6.1 内置的pip, 会提示警告如下， 终止安装，需要升级pip (python -m pip install --upgrade pip)
    protobuf requires Python '>=3.7' but the running Python is 3.6.1
    You are using pip version 9.0.1, however version 23.3.1 is available.

No module named 'tensorflow'
    pip list

如果有 requirements.txt
    pip install -r requirements.txt

@since 2023年12月5日16:59:52
"""

import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

env = gym.make('CartPole-v1')
# Optional: PPO2 requires a vectorized environment to run
# the env is now wrapped automatically when passing it to the constructor
# env = DummyVecEnv([lambda: env])

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10000)

obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()

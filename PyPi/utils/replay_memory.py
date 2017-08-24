import numpy as np

from PyPi.utils.dataset import parse_dataset


class ReplayMemory(object):
    def __init__(self, max_size):
        self._max_size = max_size
        self._idx = 0
        self._full = False

    def initialize(self, mdp_info):
        observation_space = mdp_info['observation_space']
        action_space = mdp_info['action_space']

        observation_shape = tuple([self._max_size]) + observation_space.shape
        action_shape = (self._max_size, action_space.shape)

        self._states = np.ones(observation_shape, dtype=np.float32)
        self._actions = np.ones(action_shape, dtype=np.float32)
        self._rewards = np.ones(self._max_size, dtype=np.float32)
        self._next_states = np.ones(observation_shape, dtype=np.float32)
        self._absorbing = np.ones(self._max_size, dtype=np.bool)
        self._last = np.ones(self._max_size, dtype=np.bool)

    def add(self, dataset):
        next_idx = self._idx + len(dataset)
        assert next_idx <= self._max_size

        self._states[self._idx:next_idx, ...],\
            self._actions[self._idx:next_idx, ...],\
            self._rewards[self._idx:next_idx, ...],\
            self._next_states[self._idx:next_idx, ...],\
            self._absorbing[self._idx:next_idx, ...],\
            self._last[self._idx:next_idx, ...] = parse_dataset(dataset)

        self._idx = next_idx
        if self._idx == self._max_size:
            self._full = True
            self._idx = 0

    def get(self, n_samples):
        idxs = np.random.randint(self.size, size=n_samples)

        return self._states[idxs, ...], self._actions[idxs, ...],\
            self._rewards[idxs, ...], self._next_states[idxs, ...],\
            self._absorbing[idxs, ...], self._last[idxs, ...]

    @property
    def size(self):
        return self._idx if not self._full else self._max_size

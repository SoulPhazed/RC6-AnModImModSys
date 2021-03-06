from .without_queue import ModelWithoutQueue

import numpy as np


class ModelUnlimitedQueue(ModelWithoutQueue):
    def __init__(self, client_t, handling_t, channels):
        super().__init__(client_t, handling_t, channels)

    def get_pi_arg(self, index):
        if index <= 0:
            raise ValueError("index must be more than '0'")

        if index <= self._channels:
            result = np.power(self.client_i, index) / (np.math.factorial(index) * np.power(self.handling_i, index))
        else:
            coef = self.client_i / (self._channels * self.handling_i)
            result = np.power(coef, index - self._channels) * self.get_pi_arg(self._channels)

        return result

    def get_p0(self):
        prefix_coef = self.client_i / (self._channels * self.handling_i)
        if prefix_coef < 1.:
            denom = np.sum([self.get_pi_arg(i) for i in range(1, self._channels + 1)]) + 1
            denom += self.get_pi_arg(self._channels) * prefix_coef / (1 - prefix_coef)

            return 1 / denom
        else:
            return 0

    def is_a_coef_valid(self):
        return self.client_i / (self._channels * self.handling_i) < 1.

    def busy_operators(self):
        prefix_coef = self.client_i / (self._channels * self.handling_i)
        summary = np.sum([i * self.get_pi_arg(i) for i in range(1, self._channels + 1)])
        summary += self._channels * self.get_pi_arg(self._channels) * prefix_coef / (1 - prefix_coef)
        return self.get_p0() * summary

    def queue_prob(self):
        prefix_coef = self.client_i / (self._channels * self.handling_i)
        return self.get_p0() * prefix_coef / (1 - prefix_coef)

    def queue_length_expect(self):
        prefix_coef = self.client_i / (self._channels * self.handling_i)
        return self.get_p0() * self.get_pi_arg(self._channels) / (np.power((1 - prefix_coef), 2))

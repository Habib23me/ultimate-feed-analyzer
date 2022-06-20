import numpy as np
from tqdm import tqdm

from util import Singleton


class BaseEnvironment(metaclass=Singleton):

    def __init__(self, rewards, item_col_name, visitor_col_name, reward_col_name, random_seed=1):

        np.random.seed(random_seed)

        self.rewards = rewards
        self.item_col_name = item_col_name
        self.visitor_col_name = visitor_col_name
        self.reward_col_name = reward_col_name

        # items under test
        self.items = self.rewards[self.item_col_name].unique()
        self.n_items = len(self.items)

        # visitors in the historical rewards (e.g., from ratings df)
        self.visitors = self.rewards[self.visitor_col_name].unique()
        self.n_visitors = len(self.visitors)

        # number of times each item has been sampled (previously n_sampled)
        self.n_item_samples = np.zeros(self.n_items)

        # fraction of time each item has resulted in a reward (previously movie_clicks)
        self.n_item_rewards = np.zeros(self.n_items)

    def select_item(self):
        return np.random.randint(self.n_items)

    def record_result(self, item_idx, reward):

        self.n_item_samples[item_idx] += 1

        alpha = 1./self.n_item_samples[item_idx]
        self.n_item_rewards[item_idx] += alpha * \
            (reward - self.n_item_rewards[item_idx])


class EpsilonGreedyEnvironment(BaseEnvironment):

    def __init__(self, epsilon, rewards, item_col_name, visitor_col_name, reward_col_name):
        super(EpsilonGreedyEnvironment, self).__init__(rewards,
                                                       item_col_name, visitor_col_name, reward_col_name)

        # parameter to control exploration vs exploitation
        self.epsilon = epsilon

    def select_item(self):

        # decide to explore or exploit
        if np.random.uniform() < self.epsilon:  # explore
            item_id = super(EpsilonGreedyEnvironment, self).select_item()

        else:  # exploit
            item_id = np.argmax(self.n_item_rewards)

        return item_id

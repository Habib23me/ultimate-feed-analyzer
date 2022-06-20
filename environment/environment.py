import numpy as np
from tqdm import tqdm
import pickle
from util import Singleton


class BaseEnvironment(metaclass=Singleton):

    def __init__(self, rewards, clusters, item_col_name, visitor_col_name, random_seed=1):

        np.random.seed(random_seed)

        self.rewards = rewards
        self.item_col_name = item_col_name
        self.visitor_col_name = visitor_col_name

        # items under test
        self.items = clusters
        self.n_items = len(self.items)

        # number of times each item has been sampled (previously n_sampled)
        self.n_item_samples = np.zeros(self.n_items)

        # fraction of time each item has resulted in a reward (previously movie_clicks)
        self.n_item_rewards = np.zeros(self.n_items)

    def reset(self):
        # number of times each item has been sampled (previously n_sampled)
        self.n_item_samples = np.zeros(self.n_items)

        # fraction of time each item has resulted in a reward (previously movie_clicks)
        self.n_item_rewards = np.zeros(self.n_items)

    def save_state(self):

        pickle.dump((self.items, self.n_item_samples, self.n_item_rewards),
                    open('rewards.pkl', 'wb'))

    def load_state(self):
        self.items, self.n_item_samples, self.n_item_rewards = pickle.load(
            open('rewards.pkl', 'rb'))

    def get_state(self):
        return self.items, self.n_item_samples, self.n_item_rewards

    def select_item(self):
        return np.random.randint(self.n_items)

    def record_result(self, user_idx, item_idx, reward):

        self.n_item_samples[item_idx] += 1

        alpha = 1./self.n_item_samples[item_idx]
        self.n_item_rewards[item_idx] += alpha * \
            (reward - self.n_item_rewards[item_idx])


class EpsilonGreedyEnvironment(BaseEnvironment):

    def __init__(self, epsilon, rewards, clusters, item_col_name, visitor_col_name, ):
        super(EpsilonGreedyEnvironment, self).__init__(rewards, clusters,
                                                       item_col_name, visitor_col_name)

        # parameter to control exploration vs exploitation
        self.epsilon = epsilon

    def select_item(self, user_id=None):

        # decide to explore or exploit
        if np.random.uniform() < self.epsilon:  # explore
            item_id = super(EpsilonGreedyEnvironment, self).select_item()

        else:  # exploit
            item_id = np.argmax(self.n_item_rewards)

        return item_id

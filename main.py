from services.database import ActivityClusterDatabaseService, ActivityUserDatabaseService, ClusterFeatureDatabaseService
from subscribers import new_activity_callback, record_result_callback, get_feed_callback
from services import RabbitMQService
import numpy as np
import pandas as pd
import pickle

from environment import EpsilonGreedyEnvironment


if __name__ == '__main__':
    # get activity_cluster
    # activity_cluster = pd.DataFrame.from_records(
    #     ActivityClusterDatabaseService().get_all())

    epsilon = 0.4

    activity_cluster = pd.DataFrame.from_records(
        ActivityClusterDatabaseService().get_all()).drop('score', axis=1)
    cluster_feature = pd.DataFrame.from_records(
        ClusterFeatureDatabaseService().get_all())
    clusters = cluster_feature['cluster'].unique().tolist()

    activity_user = pd.DataFrame.from_records(
        ActivityUserDatabaseService().get_all())
    cluster_userid_score = activity_user.merge(activity_cluster, on="activityId").groupby([
        "cluster", "userId"]).mean().reset_index()

    item_col_name = 'cluster_id'
    visitor_col_name = 'user_id'

    env = EpsilonGreedyEnvironment(
        epsilon, cluster_userid_score, clusters, item_col_name, visitor_col_name,)

    env.load_state()

    rabbitMQService = RabbitMQService()
    rabbitMQService.init()
    # time.sleep(5)
    rabbitMQService.subscribe(
        'activity', new_activity_callback)
    rabbitMQService.subscribe(
        'engagement', record_result_callback)
    rabbitMQService.subscribe(
        'feed_request', get_feed_callback)

    rabbitMQService.start_consuming()

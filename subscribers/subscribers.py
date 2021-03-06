from environment import EpsilonGreedyEnvironment
import json
from data_model.activity import *
from services.analyzer import *
from data_model.activity import activity_from_str
from services.cluster_features import predictCluster
from services.database import ActivityClusterDatabaseService, ActivityUserDatabaseService,ClusterFeatureDatabaseService
from services.rabbitmq import RabbitMQService


# {
#   actor: 123456789,
#   time: 2020-01-01T00:00:00.000Z,
#   foreign_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
#   media: []
#   caption: 'check this out'
# }

def new_activity_callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    activity: Activity = activity_from_str(body.decode())
    analyzed_data = analyseActivity(activity)
    for data in analyzed_data:
        data.cluster = predictCluster(data.feature)
        features= ClusterFeatureDatabaseService().getFeaturesByClusterId(data.cluster);
        print(features);
        ActivityClusterDatabaseService().put(data.to_dict())

# {
#   userId: 84c3e94e-ce0d-4721-8443-370b0325abd0,
# }


def get_feed_callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    parsed_body = json.loads(body)
    # implement by fitsum
    cluster = EpsilonGreedyEnvironment().select_item(parsed_body['userId'])
    # cluster = 1
    feed = ActivityClusterDatabaseService().getActivitiesByCluster(cluster)
    RabbitMQService().send('feed_response', json.dumps({
        "data": feed, "userId": parsed_body['userId']}))


# {
#   activityId: 4e0fd601-4ecf-471a-ac90-e71db0e68593,
#   userId: 84c3e94e-ce0d-4721-8443-370b0325abd0,
#   score: 0.8,
# }


def record_result_callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    parsed_body = json.loads(body)
    ActivityUserDatabaseService().putOrUpdate({
        "activityId": parsed_body['activity_id'],
        "userId": parsed_body['actor'],
        "score": parsed_body['score']
    }, parsed_body['activity_id']+"_"+parsed_body['actor'])
    env = EpsilonGreedyEnvironment()
    ActivityClusterDatabaseService().getActivityCluster(
        parsed_body['activityId'])
    env.record_result(None, ActivityClusterDatabaseService().getActivityCluster(
        parsed_body['activityId']), parsed_body['score'])
    env.save_state()

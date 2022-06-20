from environment import EpsilonGreedyEnvironment
import json
from data_model.activity import *
from services.analyzer import *
from data_model.activity import activity_from_str
from services.cluster_features import predictCluster
from services.database import ActivityClusterDatabaseService
from services.rabbitmq import RabbitMQService


# {
#   activity_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
#   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
#   score: 0.8,
# }

def new_activity_callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    activity: Activity = activity_from_str(body.decode())
    analyzed_data=analyseActivity(activity)
    for data in analyzed_data:
        data.cluster=predictCluster(data.feature)
        # ActivityClusterDatabaseService()

    # implement by Habib
    # get cluster 
    # record result to database
    


# {
#   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
# }
def get_feed_callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    parsed_body = json.loads(body)
    # implement by fitsum
    feed = [];
    # get_feed(parsed_body['user_id'])
    RabbitMQService().send('feed_response', feed)


# {
#   activity_id: 4e0fd601-4ecf-471a-ac90-e71db0e68593,
#   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
#   reward: 0.8,
# }
def record_result_callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    parsed_body = json.loads(body)
    # implement by Habib
    # record_result(parsed_body['activity_id'], parsed_body['user_id'], parsed_body['score'])

    env = EpsilonGreedyEnvironment()
    env.record_result(parsed_body['activity_id'], parsed_body['score'])

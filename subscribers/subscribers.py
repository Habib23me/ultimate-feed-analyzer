from environment import EpsilonGreedyEnvironment
import json
from data_model.activity import *
from services.analyzer import *
from data_model.activity import activity_from_str


# {
#   activity_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
#   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
#   score: 0.8,
# }

def new_activity_callback(ch, method, properties, body):
    print(type(body.decode()))
    print(" [x] Received %r" % body.decode())
    activity: Activity = activity_from_str(body.decode())
    analyseActivity(activity)


# {
#   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
# }
def get_feed_callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# {
#   activity_id: 4e0fd601-4ecf-471a-ac90-e71db0e68593,
#   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
#   reward: 0.8,
# }
def record_result_callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    parsed_body = json.loads(body)

    env = EpsilonGreedyEnvironment()
    env.record_result(parsed_body['activity_id'], parsed_body['reward'])

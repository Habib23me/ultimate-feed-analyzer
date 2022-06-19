import json


def convert_byte_string_to_json(byte_string):
    """
    Converts a byte string to a json string.
    :param byte_string:
    :return:
    """
    return json.loads(byte_string.decode('utf-8').replace("'", '"'))


def convert_json_to_byte_string(json_string):
    """
    Converts a json string to a byte string.
    :param json:
    :return:
    """
    return json.dumps(json_string).encode('utf-8')

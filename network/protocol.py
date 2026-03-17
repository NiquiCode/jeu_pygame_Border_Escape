import json


def encode_message(data):
    """
    Encode un dictionnaire Python en JSON ligne par ligne.
    """
    return (json.dumps(data) + "\n").encode("utf-8")


def decode_message(line):
    """
    Décode une ligne JSON en dictionnaire Python.
    """
    return json.loads(line)
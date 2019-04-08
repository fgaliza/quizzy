import base64
import json


def url_encrypt(quiz_id):
    data = {
        "quiz_id": quiz_id,
    }
    return base64.b64encode(json.dumps(data).encode('utf-8')).decode()


def url_decrypt(hash):
    return base64.b64decode(hash).decode()

import threading
import json

from core import generate


def encode_experience_key(form):
    key = "experience-" + form["id"]
    return key


class Listener(threading.Thread):
    HOUR = 3600

    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def run(self):
        for item in self.pubsub.listen():
            
            if item["type"] == "message" and item["channel"] == b"spp-exp-channel":
                data = json.loads(item["data"])
                anwser = generate(data["text"])
                self.redis.set(
                    name=encode_experience_key(data), # key like experience-<id>
                    value=anwser, # model output
                    ex=self.HOUR * 48,  # keep the data for 48 hours
                )

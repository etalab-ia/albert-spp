import threading
import json
import datetime as dt

from core import generate


class Listener(threading.Thread):
    HOUR = 3600

    def __init__(self, r, channels):
        print("info: listener init")  # TODO: replace with logger later
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def run(self):
        print("info: listener run")  # TODO: replace with logger later
        for item in self.pubsub.listen():
            if item["type"] == "message" and item["channel"] == b"spp-exp-channel":
                data = json.loads(item["data"])

                duration = dt.datetime.now(dt.timezone.utc) - dt.datetime.strptime(
                    data["time"], "%Y-%m-%d %H:%M:%S.%f%z"
                )
                print(f"duration time - {data['id']}: {duration.total_seconds()} s")

                try:
                    anwser = generate(data["text"])
                except Exception as e:
                    print("Error in generating text: ", e)
                    anwser = "Error in generating text."

                self.redis.set(
                    name=data["id"],  # key
                    value=anwser,  # model output
                    ex=self.HOUR * 48,  # keep the data for 48 hours
                )

import datetime as dt
import json
import threading

from redis import Redis

from llm import few_shots


class Listener(threading.Thread):
    HOUR = 3600
    KILL_PILL = "EXIT"

    def __init__(self, r: Redis, channels):
        print("info: listener init")  # TODO: replace with logger later
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
        self.pubsub.subscribe(self.KILL_PILL)  # Subscribe to a special stop channel

    def run(self):
        print("info: listener run")  # TODO: replace with logger later
        for item in self.pubsub.listen():
            if item["type"] == "message" and item["channel"] == self.KILL_PILL.encode():
                break

            if item["type"] == "message" and item["channel"] == b"spp-exp-channel":
                data = json.loads(item["data"])

                duration = dt.datetime.now(dt.timezone.utc) - dt.datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S.%f%z")
                print(f"duration time - {data['id']}: {duration.total_seconds()} s")

                # do not fail silently
                try:
                    answer = few_shots(prompt=data["text"])
                except Exception as e:
                    answer = "error"

                self.redis.set(
                    name=data["id"],  # key
                    value=answer,  # model output
                    ex=self.HOUR * 48,  # keep the data for 48 hours
                )

    def stop(self):
        self.redis.publish(self.KILL_PILL, "terminated")
        self.pubsub.close()
        self.join()

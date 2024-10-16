import datetime as dt
import json
import threading
import logging

from redis import Redis

from app.llm import few_shots


class Listener(threading.Thread):
    HOUR = 3600
    KILL_PILL = "EXIT"

    def __init__(self, r: Redis, channels):
        logging.info("listener init")
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
        self.pubsub.subscribe(self.KILL_PILL)  # Subscribe to a special stop channel

    def run(self):
        logging.info("listener run")
        for item in self.pubsub.listen():
            if item["type"] == "message" and item["channel"] == self.KILL_PILL.encode():
                break

            if item["type"] == "message" and item["channel"] == b"spp-exp-channel":
                data = json.loads(item["data"])

                duration = dt.datetime.now(dt.timezone.utc) - dt.datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S.%f%z")
                logging.info(f"duration time - {data["id"]}: {duration.total_seconds()} s")

                try:
                    answer = few_shots(prompt=data["text"])
                except Exception:
                    import traceback

                    error_traceback = traceback.format_exc()
                    logging.error(f"\nRequest prompt:\n{data["text"]}\n\nError:\n{error_traceback}")
                    answer = f"error on {data["id"]} request, please resend prompt later."

                self.redis.set(
                    name=data["id"],  # key
                    value=answer,  # model output
                    ex=self.HOUR * 48,  # keep the data for 48 hours
                )

    def stop(self):
        self.redis.publish(self.KILL_PILL, "terminated")
        self.pubsub.close()
        self.join()

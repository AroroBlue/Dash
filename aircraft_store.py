import threading
import time


class AircraftStore:

    def __init__(self):
        self.lock = threading.Lock()
        self.targets = {}

    def update_target(self, target):

        key = f"{target['source']}_{target['track_number']}"

        with self.lock:
            self.targets[key] = target

    def get_targets(self):

        with self.lock:
            return list(self.targets.values())

    def cleanup(self, timeout=30):

        now = time.time()

        with self.lock:

            remove_keys = []

            for key, value in self.targets.items():

                if now - value["timestamp"] > timeout:
                    remove_keys.append(key)

            for key in remove_keys:
                del self.targets[key]
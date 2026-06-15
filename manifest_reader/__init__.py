import json
import logging
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='manifest.log', level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger.info('Started')


def spawn_json(path):
    default = {"total": 0, "frames": {}}
    with open(path, "w") as f:
        f.write(json.dumps(default))

class ManifestReader:
    def __init__(self, filename: str = "manifest.json"):
        self.file = filename
        with open(filename, "r") as f:
            self._raw = json.loads(f.read())
            self.total = self._raw["total"]
            self.frames = self._raw["frames"]

    def commit(self):
        with open(self.file, "w") as f:
            f.write(json.dumps(self._raw))

    def set_total(self, total):
        self.total = total
        self._raw["total"] = total

    def set_type(self, n, type):
        n = str(n)
        types = {0: None, 1: "normal", 2: "sniff", 3: "pick"}
        self._raw["frames"][n] = types[type]

    def add_frame(self, frame):
        self._raw["frames"][frame] = None

    def get_type(self, n):
        logger.debug(f"Request: {n} {self._raw['frames'][str(n)]}")
        return self._raw["frames"][str(n)]

if __name__ == "__main__":
    reader = ManifestReader("../manifest.json")
    logger.info(reader.total)
    logger.info(reader.frames)
    reader.set_type(2, 1)
    logger.info(reader.frames)


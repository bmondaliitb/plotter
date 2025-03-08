
from sample import Sample

class Plot:
    def __init__(self, config):
        self.config = config
        self.name = config["name"]
        self.samples = self.config["samples"]
        self.type = config["type"]
        self.x_label = config["x_label"]
        self.y_label = config["y_label"]
        self.x_range = config["x_range"]
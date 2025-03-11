
from sample import Sample

class Plot:
    def __init__(self, config):
        self.config = config
        self.name = config["name"]
        self.samples = self.config["samples"]
        self.type = config["type"]
        if "x_label" in config:
            self.x_label = config["x_label"]
        if "y_label" in config:
            self.y_label = config["y_label"]
        if "x_range" in config:
            self.x_range = config["x_range"]
        if "y_range" in config:
            self.y_range = config["y_range"]
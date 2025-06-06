
from sample import Sample

class Plot:
    def __init__(self, config):
        self.config = config
        self.name = config["name"]
        self.samples = self.config["samples"]
        self.type = config["type"]
        self.x_label = config.get("x_label", "")
        self.y_label = config.get("y_label", "")
        self.x_range = config.get("x_range", None)
        self.y_range = config.get("y_range", None)
        self.setlogy = config.get("setlogy", False)
        self.setlogx = config.get("setlogx", False)
        self.y_range_ratio = config.get("y_range_ratio", None)
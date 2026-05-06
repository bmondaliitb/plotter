
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
        self.z_range = config.get("z_range", None)
        self.setlogy = config.get("setlogy", False)
        self.setlogx = config.get("setlogx", False)
        self.y_range_ratio = config.get("y_range_ratio", None)
        self.x_tick_interval = config.get("x_tick_interval", None)
        self.draw_errors = config.get("draw_errors", True)
        self.plot_labels = config.get("plot_label", None)
        self.ratio_pad_margin_up = config.get("ratio_pad_margin_up", None)
        self.ratio_pad_margin_down = config.get("ratio_pad_margin_down", None)
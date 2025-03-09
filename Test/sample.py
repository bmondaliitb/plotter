from plotter.dataset import dataset
from plotter.histo import histo

class Sample:
    def __init__(self, config):
        self.name = config["name"]
        self.file = config["file_path"]
        self.hist_name = config["variable"]
        self.hist = self.load_histogram()

    def load_histogram(self):
        root_file = dataset(self.name, self.file)
        histogram = root_file.get(self.hist_name)
        hist = histo(self.name, histogram)
        return hist

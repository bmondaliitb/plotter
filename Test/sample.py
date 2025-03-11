import ROOT
from plotter.dataset import dataset
from plotter.tfile2 import TFile2 as tfile2
from plotter.histo import histo
from plotter.histo import histo2D

class Sample:
    def __init__(self, config):
        self.name = config["name"]
        self.file = config["file_path"]
        self.hist_name = config["variable"]
        self.hist = self.load_histogram()

    def load_histogram(self):
        root_file = tfile2(self.file)
        histogram = root_file.Get(self.hist_name)
        if isinstance(histogram, ROOT.TH2):
            hist = histo2D(self.name, histogram)
        elif isinstance(histogram, ROOT.TH1):
            hist = histo(self.name, histogram)
        return hist

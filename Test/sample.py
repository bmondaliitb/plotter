import ROOT
from plotter.dataset import dataset
from plotter.tfile2 import TFile2 as tfile2
from plotter.histo import histo
from plotter.histo import histo2D

class Sample:
    def __init__(self, sample_config, job_config):
        self.name = sample_config["name"]
        self.file = sample_config.get("file_path", job_config["file_path"]) # if file_path is not in sample_config, use job_config
        self.hist_name = sample_config["variable"]
        self.hist = self.load_histogram()

    def load_histogram(self):
        root_file = tfile2(self.file)
        histogram = root_file.Get(self.hist_name)
        if isinstance(histogram, ROOT.TH2):
            hist = histo2D(self.name, histogram)
        elif isinstance(histogram, ROOT.TH1):
            hist = histo(self.name, histogram)
        return hist

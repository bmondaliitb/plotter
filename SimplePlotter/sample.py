import glob
import sys
import ROOT
from plotter.dataset import dataset
from plotter.tfile2 import TFile2 as tfile2
from plotter.histo import histo
from plotter.histo import histo2D

class Sample:
    def __init__(self, sample_config, job_config):
        self.name = sample_config["name"]
        self.files = self._expand_file_paths(sample_config.get("file_paths", job_config["file_paths"])) # if file_paths not set in sample, use job file_paths
        self.hist_name = sample_config["variable"]
        self.hist = self.load_histogram()

    def _expand_file_paths(self, file_paths):
        expanded_files = []
        for path in file_paths:
            matched_files = glob.glob(path)
            if not matched_files:
                print(f"Error: No files found matching path '{path}'")
                sys.exit(1)
            expanded_files.extend(matched_files)
        return expanded_files

    def load_histogram(self):
        hist = None
        for file_path in self.files:
            root_file = tfile2(file_path)
            histogram = root_file.Get(self.hist_name)
            if not histogram:
                print(f"Error: Histogram '{self.hist_name}' not found in file '{file_path}'")
                sys.exit(1)
            if isinstance(histogram, ROOT.TH2):
                if hist is None:
                    hist = histo2D(self.name, histogram)
                else:
                    hist.th.Add(histogram)
            elif isinstance(histogram, ROOT.TH1):
                if hist is None:
                    hist = histo(self.name, histogram)
                else:
                    hist.th.Add(histogram)
        return hist
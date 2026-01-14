import glob
import sys
import ROOT
from plotter.dataset import dataset
from plotter.tfile2 import TFile2 as tfile2
from plotter.histo import histo
from plotter.histo import histo2D

from plotter.canvas import canvas

class Canvas:
    def __init__(self, name, canvas_obj):
        self.name = name
        self.canvas = canvas_obj
        self.th = canvas_obj  # For compatibility with the existing code

    def SetLineColor(self, color):
        pass  # Canvas doesn't have line color

    def SetLineStyle(self, style):
        pass  # Canvas doesn't have line style

    def SetLineWidth(self, width):
        pass  # Canvas doesn't have line width

    def SetMarkerStyle(self, style):
        pass  # Canvas doesn't have marker style

class Sample:
    def __init__(self, sample_config, job_config):
        self.name = sample_config["name"]
        self.files = self._expand_file_paths(sample_config.get("file_paths", job_config["file_paths"]))
        self.hist_name = sample_config["variable"]
        self.normalize = sample_config.get("normalize", False)
        self.hist = self.load_histogram()
        if self.normalize and hasattr(self.hist, "th") and not isinstance(self.hist.th, ROOT.TCanvas):
            self.normalize_histogram()

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
            obj = root_file.Get(self.hist_name)
            if not obj:
                print(f"Error: Object '{self.hist_name}' not found in file '{file_path}'")
                sys.exit(1)

            if isinstance(obj, ROOT.TCanvas):
                # Handle canvas objects
                if hist is None:
                    hist = Canvas(self.name, obj)
                else:
                    print(f"Warning: Cannot add multiple canvas objects for '{self.name}'")
            elif isinstance(obj, ROOT.TH2):
                if hist is None:
                    hist = histo2D(self.name, obj)
                else:
                    hist.th.Add(obj)
            elif isinstance(obj, ROOT.TH1):
                if hist is None:
                    hist = histo(self.name, obj)
                else:
                    hist.th.Add(obj)
            else:
                print(f"Warning: Object '{self.hist_name}' is not a histogram or canvas")

        return hist

    def normalize_histogram(self):
        if hasattr(self.hist, "th"):
            integral = self.hist.th.Integral()+self.hist.th.GetBinContent(self.hist.th.GetNbinsX()+1)+self.hist.th.GetBinContent(0)
            if integral != 0:
                self.hist.th.Scale(1.0 / integral)
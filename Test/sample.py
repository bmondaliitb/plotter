from plotter.dataset import dataset
from plotter.histo import histo

class Sample:
    def __init__(self, config, preset):
        self.name = config["name"]
        self.file = config["file_path"]
        self.hist_name = config["variable"]
        self.preset = preset
        self.hist = self.load_histogram()

    def load_histogram(self):
        root_file = dataset(self.name, self.file)
        histogram = root_file.get(self.hist_name)
        hist = histo(self.name, histogram)
        self.apply_preset(hist)
        return hist

    def apply_preset(self, hist):
        hist.SetFillColor(self.preset.fillcolor)
        hist.SetFillStyle(self.preset.fillstyle)
        hist.SetLineColor(self.preset.linecolor)
        hist.SetLineWidth(self.preset.linewidth)
        hist.SetMarkerSize(self.preset.markersize)
        hist.SetMarkerStyle(self.preset.markerstyle)
        hist.SetLineStyle(self.preset.linestyle)
import glob                                                                                                                
import sys                                                                                                                 
import ROOT                                                                                                                
from root_io import RootFile                                                                                              
from histogram import Histogram1D, Histogram2D                                                                            
                                                                                                                           
class CanvasWrapper:                                                                                                       
    """Wrapper so canvas can be treated like a histogram holder."""                                                        
    def __init__(self, name, canvas):                                                                                      
        self.name = name                                                                                                   
        self.canvas = canvas                                                                                               
        self.th = canvas  # for compatibility                                                                              
        self.legend_title = name

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
        expanded = []
        for path in file_paths:
            matches = glob.glob(path)
            if not matches:
                print(f"Error: No files found matching path '{path}'")
                sys.exit(1)
            expanded.extend(matches)
        return expanded

    def load_histogram(self):
        hist = None
        for file_path in self.files:
            with RootFile(file_path) as f:
                obj = f.Get(self.hist_name)
                if not obj:
                    print(f"Error: Object '{self.hist_name}' not found in file '{file_path}'")
                    sys.exit(1)

                cloned = None
                if isinstance(obj, ROOT.TCanvas):
                    cloned = obj.Clone()
                elif isinstance(obj, ROOT.TH2):
                    cloned = obj.Clone()
                    cloned.SetDirectory(0)
                elif isinstance(obj, ROOT.TH1):
                    cloned = obj.Clone()
                    cloned.SetDirectory(0)
                else:
                    print(f"Warning: Object '{self.hist_name}' is not a histogram or canvas")
                    continue

            # use the cloned, detached object after the file is closed
            if isinstance(cloned, ROOT.TCanvas):
                if hist is None:
                    hist = CanvasWrapper(self.name, cloned)
                else:
                    print(f"Warning: Cannot add multiple canvas objects for '{self.name}'")
            elif isinstance(cloned, ROOT.TH2):
                if hist is None:
                    hist = Histogram2D(self.name, cloned)
                else:
                    hist.th.Add(cloned)
            elif isinstance(cloned, ROOT.TH1):
                if hist is None:
                    hist = Histogram1D(self.name, cloned)
                else:
                    hist.th.Add(cloned)
        return hist

    def normalize_histogram(self):
        integral = self.hist.th.Integral()
        if integral != 0:
            self.hist.th.Scale(1.0 / integral)

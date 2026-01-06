import ROOT                                                 
                                                                                                                           
class Histogram1D:                                                                                                         
    """Light wrapper over ROOT.TH1 for styling and legend title."""                                                        
    def __init__(self, name, th1):                          
        self.name = name                                                                                                   
        self.th = th1                                                                                                      
        self.legend_title = name
        self.th.SetTitle(name)                              
                                                                                                                           
    # Style setters used by SimplePlotter.apply_style                                                                      
    def SetLineColor(self, c): self.th.SetLineColor(c)                                                                     
    def SetLineStyle(self, s): self.th.SetLineStyle(s)                                                                     
    def SetLineWidth(self, w): self.th.SetLineWidth(w)      
    def SetMarkerStyle(self, s): self.th.SetMarkerStyle(s)
                                                                                                                           
    def Add(self, other): self.th.Add(other.th)                                                                            
                                                                                                                           
    def clone(self, suffix):                                                                                               
        clone = self.th.Clone(f"{self.name}_{suffix}")
        new = Histogram1D(clone.GetName(), clone)
        new.legend_title = getattr(self, "legend_title", self.name)
        return new

    def ratio_to(self, other, fill_to_line=False):
        """Return a clone divided by other."""
        h = self.clone("ratio")
        h.th.Divide(other.th) 
        if fill_to_line:
            h.th.SetFillStyle(0)
        return h

class Histogram2D:
    def __init__(self, name, th2):
        self.name = name
        self.th = th2
        self.legend_title = name
        self.th.SetTitle(name)

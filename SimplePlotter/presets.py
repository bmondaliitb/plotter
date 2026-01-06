import ROOT                                                 
from histogram import Histogram1D, Histogram2D
                             
class _Pad1D:                                               
    def __init__(self, canvas, pad=None, drawoption="hist E"):
        self.canvas = canvas                                
        self.pad = pad if pad else canvas              
        self.drawoption = drawoption   
        self._histos = []                                   
        self.primitives = []  # populated after plot        
                                                            
    def cd(self):           
        self.pad.cd()                                       
                             
    def add_histos(self, histos):
        self._histos.extend(histos)               
                                                            
    def add_histo(self, histo):                                                                                            
        self._histos.append(histo)                                                                                         
                                                            
    def plot_histos(self):                                  
        self.cd()                                           
        first = True                                                                                                       
        for h in self._histos:                          
            opt = self.drawoption if first else self.drawoption + " same"
            h.th.Draw(opt)                                                                                                 
            first = False                                                                                                  
        self.primitives = list(self._histos)  # for tick-interval handling
                                                            
    def set_xrange(self, xmin, xmax):                                                                                      
        for h in self._histos:                                                                                             
            h.th.GetXaxis().SetRangeUser(xmin, xmax)     
                                                                                                                           
    def set_yrange(self, ymin, ymax):
        for h in self._histos:       
            h.th.GetYaxis().SetRangeUser(ymin, ymax)
                                                            
    def logx(self, on=True):                                
        self.pad.SetLogx(on)
                                                                                                                           
    def logy(self, on=True):
        self.pad.SetLogy(on)                                
                                                            
class _PadRatio(_Pad1D):
    def __init__(self, canvas, pad): 
        super().__init__(canvas, pad, drawoption="hist E")
    def set_yrange(self, ymin, ymax):             
        for h in self._histos:                         
            h.th.GetYaxis().SetRangeUser(ymin, ymax)
                                                            
def _legend_for(histos):
    leg = ROOT.TLegend(0.6, 0.7, 0.88, 0.88)
    for h in histos:
        title = getattr(h, "legend_title", h.th.GetTitle())
        leg.AddEntry(h.th, title, "lp")
    return leg

class SimplePlot:           
    def __init__(self, name="", x_title="", y_title="Events", draw_legend=True):                                           
        self.canvas = ROOT.TCanvas(name, name, 800, 700)                                                                   
        self.draw_legend = draw_legend                                                                                     
        self._x_title = x_title               
        self._y_title = y_title
        self.mainPad = _Pad1D(self.canvas)

    def add_and_plot(self, histos):
        if not histos:
            raise RuntimeError("No histograms to plot")
        # set titles if missing
        for h in histos:
            # hide histogram title box while keeping legend titles separate
            h.th.SetTitle("")
            if self._x_title: 
                h.th.GetXaxis().SetTitle(self._x_title)
            if self._y_title: 
                h.th.GetYaxis().SetTitle(self._y_title)
        self.mainPad.add_histos(histos)
        self.mainPad.plot_histos()
        if self.draw_legend:
            leg = _legend_for(histos)
            self.canvas.cd()
            leg.Draw()
        self.canvas.Update()

    def logx(self, on=True): self.mainPad.logx(on)
    def logy(self, on=True): self.mainPad.logy(on)
    def set_xrange(self, xmin, xmax): self.mainPad.set_xrange(xmin, xmax)
    def set_yrange(self, ymin, ymax): self.mainPad.set_yrange(ymin, ymax)
    def save(self, path): self.canvas.SaveAs(path)

class ComparisonPlot:
    def __init__(self, name="", x_title="", y_title="Events", ratio_title="Ratio", draw_legend=True):
        self.canvas = ROOT.TCanvas(name, name, 800, 800)
        self.draw_legend = draw_legend
        self.pad_main = ROOT.TPad("main", "main", 0, 0.3, 1, 1.0)
        self.pad_ratio = ROOT.TPad("ratio", "ratio", 0, 0.0, 1, 0.3)
        self.pad_main.SetBottomMargin(0.02)
        self.pad_ratio.SetTopMargin(0.02)
        self.pad_ratio.SetBottomMargin(0.3)
        self.pad_main.Draw(); self.pad_ratio.Draw()
        self.mainPad = _Pad1D(self.canvas, self.pad_main)
        self.ratioPad = _PadRatio(self.canvas, self.pad_ratio)
        self._x_title = x_title
        self._y_title = y_title
        self._ratio_title = ratio_title

    def add_and_plot(self, histos):
        if len(histos) < 2:
            raise RuntimeError("Need at least reference + one overlay histogram")
        ref = histos[0]

        # Main pad
        for h in histos:
            h.th.SetTitle("")
            if self._x_title: 
                h.th.GetXaxis().SetTitle(self._x_title)
            if self._y_title: 
                h.th.GetYaxis().SetTitle(self._y_title)
        self.mainPad.add_histos(histos)
        self.mainPad.plot_histos()
        if self.draw_legend:
            self.canvas.cd()
            _legend_for(histos).Draw()

        # Ratio pad
        ratios = []
        for h in histos[1:]:
            r = h.ratio_to(ref)
            r.th.GetYaxis().SetTitle(self._ratio_title)
            r.th.GetYaxis().SetNdivisions(505)
            r.th.GetYaxis().SetTitleSize(0.10)
            r.th.GetYaxis().SetLabelSize(0.08)
            r.th.GetXaxis().SetTitleSize(0.10)
            r.th.GetXaxis().SetLabelSize(0.08)
            ratios.append(r)
        self.ratioPad.add_histos(ratios)
        self.ratioPad.plot_histos()
        self.canvas.Update()

    def set_xrange(self, xmin, xmax):
        self.mainPad.set_xrange(xmin, xmax)
        self.ratioPad.set_xrange(xmin, xmax)

    def logx(self, on=True):
        self.mainPad.logx(on) 
        self.ratioPad.logx(on)

    def logy(self, on=True):
        self.mainPad.logy(on) 

    def save(self, path):
        self.canvas.cd()
        self.canvas.SaveAs(path)

class SimpleTH2Plot:
    def __init__(self, name="", x_title="", y_title=""):
        self.canvas = ROOT.TCanvas(name, name, 800, 700)
        self._x_title = x_title
        self._y_title = y_title
        # keep compatibility
        self.mainPad = self

    def add_and_plot(self, h2):
        if not isinstance(h2, Histogram2D):
            raise TypeError("Expected Histogram2D")
        if self._x_title: h2.th.GetXaxis().SetTitle(self._x_title)
        if self._y_title: h2.th.GetYaxis().SetTitle(self._y_title)
        h2.th.Draw("colz")
        self.canvas.Update()

    def set_xrange(self, xmin, xmax):
        self.canvas.cd()
        obj = self.canvas.GetListOfPrimitives()[0]
        obj.GetXaxis().SetRangeUser(xmin, xmax)

    def set_yrange(self, ymin, ymax):
        self.canvas.cd()
        obj = self.canvas.GetListOfPrimitives()[0]
        obj.GetYaxis().SetRangeUser(ymin, ymax)

    def set_zrange(self, zmin, zmax):
        self.canvas.cd()
        obj = self.canvas.GetListOfPrimitives()[0]
        obj.SetMinimum(zmin); obj.SetMaximum(zmax)

    def logx(self, on=True): self.canvas.SetLogx(on)
    def logy(self, on=True): self.canvas.SetLogy(on)
    def logz(self, on=True): self.canvas.SetLogz(on)
    def save(self, path): self.canvas.SaveAs(path)

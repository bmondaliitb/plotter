import logging
from typing import List, Optional

import ROOT

from .canvas import canvas
from .histo import histo, histo2D
from .legend import legend
from .pad import COMPARISON_PAD_STYLE, pad


log = logging.getLogger(__name__)

ERROR_BAND_STYLE = {
    "drawoption": "e2",
    "markersize": 0,
    "fillstyle": 3154,
    "linestyle": 3,
}


def _legend_from_config(legend_position):
    if not isinstance(legend_position, dict):
        return legend()
    allowed_keys = {
        "xMin", "xMax", "yMax", "height", "nColumns", "textSize", "textFont"
    }
    kwargs = {key: value for key, value in legend_position.items() if key in allowed_keys}
    return legend(**kwargs) if kwargs else legend()


class simple:
    def __init__(
        self,
        plotName: str = "",
        xTitle: Optional[str] = None,
        yTitle: Optional[str] = "Events",
        isTH1: bool = True,
        autoY=True,
        draw_legend=True,
        legend_position=None,
    ):
        self.canvas = canvas(plotName)
        self.draw_legend = draw_legend
        self.legend_position = legend_position

        self.mainPad = pad("main", isTH1=isTH1, autoY=autoY)
        self.canvas.add_pad(self.mainPad)
        self.mainPad.set_title(xTitle, yTitle)

    def add_and_plot(self, hs: List[histo]):
        if not hs:
            log.error("List of histograms is empty")
            raise RuntimeError

        self.hs = hs
        self.mainPad.add_histos(self.hs)
        self.mainPad.plot_histos()

        self.canvas.tcan.cd()
        if self.draw_legend:
            self.leg = _legend_from_config(self.legend_position)
            self.leg.add_histos(self.hs)
            self.leg.create_and_draw()

    def logx(self, doLog=True):
        self.mainPad.logx(doLog)

    def set_xrange(self, min, max):
        self.mainPad.set_xrange(min, max)

    def set_yrange(self, min, max):
        self.mainPad.set_yrange(min, max)

    def save(self, plotName: str, verbose=False):
        self.canvas.save(plotName, verbose)


class Comparison:
    def __init__(
        self,
        plotName: str = "",
        xTitle: Optional[str] = "",
        yTitle: Optional[str] = "Events",
        ratioTitle: str = "Ratio",
        fraction: float = 0.3,
        show_nonEmptyOnly: bool = True,
        draw_legend=True,
        legend_position=None,
        draw_ratio_error_band: bool = True,
    ):
        self.canvas = canvas(plotName)

        self.mainPad = pad("main", yl=fraction, style=COMPARISON_PAD_STYLE)
        self.canvas.add_pad(self.mainPad)
        self.mainPad.set_title(xTitle, yTitle)
        self.mainPad.margins(down=0)

        self.ratioPad = pad("ratio", yh=fraction, style=COMPARISON_PAD_STYLE)
        self.canvas.add_pad(self.ratioPad)
        self.ratioPad.set_yrange(0.701, 1.299)
        self.ratioPad.margins(up=0)
        self.ratioPad.set_title(xTitle, ratioTitle)

        self.nonEmpty = show_nonEmptyOnly
        self.draw_legend = draw_legend
        self.legend_position = legend_position
        self.draw_ratio_error_band = draw_ratio_error_band

    def add_and_plot(self, histos: List[histo]):
        if not histos:
            log.error("List of histograms is empty")
            raise RuntimeError

        self.histos = histos

        if self.nonEmpty:
            xMin = histos[0].th.GetBinLowEdge(1)
            xMax = histos[0].th.GetBinLowEdge(histos[0].th.GetNbinsX() + 1)
            prevCont = False
            minDone = False
            maxDone = False
            for i in range(histos[0].th.GetNbinsX()):
                iBin = i + 1
                if histos[0].th.GetBinContent(iBin) == 0:
                    if not minDone:
                        xMin = histos[0].th.GetBinLowEdge(iBin + 1)
                    if prevCont:
                        xMax = histos[0].th.GetBinLowEdge(iBin)
                        maxDone = True
                    prevCont = False
                else:
                    minDone = True
                    prevCont = True
            if not maxDone:
                xMax = histos[0].th.GetBinLowEdge(histos[0].th.GetNbinsX() + 1)
            self.mainPad.set_xrange(xMin, xMax)
            self.ratioPad.set_xrange(xMin, xMax)

        self.mainPad.add_histos(self.histos)
        self.mainPad.plot_histos()

        self.hRatios = [
            h.get_ratio(self.histos[0], fillToLine=False) for h in self.histos[1:]
        ]
        ratio_histos = list(self.hRatios)
        if self.draw_ratio_error_band:
            self.hErr = self.histos[0].get_ratio(self.histos[0])
            self.hErr.color = ROOT.kGray + 1
            self.hErr.style_histo(ERROR_BAND_STYLE)
            ratio_histos.insert(0, self.hErr)
        else:
            self.hUnity = self.histos[0].get_ratio(self.histos[0])
            self.hUnity.linecolor = ROOT.kBlack
            self.hUnity.linestyle = 2
            self.hUnity.linewidth = 2
            self.hUnity.fillstyle = "hollow"
            self.hUnity.inlegend = False
            ratio_histos.insert(0, self.hUnity)

        self.ratioPad.add_histos(ratio_histos)
        self.ratioPad.plot_histos()

        self.canvas.tcan.cd()
        if self.draw_legend:
            self.leg = _legend_from_config(self.legend_position)
            self.leg.add_histos(self.histos)
            self.leg.create_and_draw()

    def set_xrange(self, min, max):
        self.mainPad.set_xrange(min, max)
        self.ratioPad.set_xrange(min, max)

    def logx(self, doLog=True):
        self.mainPad.logx(doLog)
        self.ratioPad.logx(doLog)

    def save(self, plotName: str, verbose=False):
        self.canvas.save(plotName, verbose)


class SimpleTH2:
    def __init__(
        self,
        plotName: str = "",
        xTitle: Optional[str] = None,
        yTitle: Optional[str] = None,
    ):
        self.canvas = canvas(plotName)
        self.mainPad = pad("main", isTH1=False)
        self.canvas.add_pad(self.mainPad)
        self.mainPad.set_title(xTitle, yTitle)

    def add_and_plot(self, h: histo2D):
        self.mainPad.add_histo(h)
        self.mainPad.plot_histos()
        self.set_margins()

    def set_xrange(self, min, max):
        self.mainPad.set_xrange(min, max)

    def set_yrange(self, min, max):
        self.mainPad.set_yrange(min, max)

    def set_zrange(self, min, max):
        self.mainPad.set_zrange(min, max)

    def logx(self, doLog=True):
        self.mainPad.logx(doLog)

    def logy(self, doLog=True):
        self.mainPad.logy(doLog)

    def logz(self, doLog=True):
        self.mainPad.logz(doLog)

    def set_margins(
        self,
        left: float = 0.15,
        right: float = 0.15,
        down: float = 0.15,
        up: float = 0.15,
    ):
        self.mainPad.margins(left=left, right=right, down=down, up=up)

    def save(self, plotName: str, verbose=False):
        self.canvas.save(plotName, verbose)

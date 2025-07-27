# src/plotter/cms.py
from ROOT import TStyle, TROOT
import ROOT
from typing import Dict

import logging

log = logging.getLogger(__name__)

ROOT.gROOT.SetBatch(True)

def SetCmsStyle():
    """Sets custom CMS style, based on the cmsstyle package"""
    cmsStyle = 0
    log.info("Applying CMS style settings...")
    if cmsStyle == 0:
        cmsStyle = CmsStyle()
    ROOT.gROOT.SetStyle("CMS")
    ROOT.gROOT.ForceStyle()

def CmsStyle():
    cmsStyle = TStyle("CMS", "CMS style")

    # use plain black on white colors
    cmsStyle.SetFrameBorderMode(0)
    cmsStyle.SetFrameFillColor(0)
    cmsStyle.SetCanvasBorderMode(0)
    cmsStyle.SetCanvasColor(0)
    cmsStyle.SetPadBorderMode(0)
    cmsStyle.SetPadColor(0)
    cmsStyle.SetStatColor(0)

    # set the paper & margin sizes
    cmsStyle.SetPaperSize(20, 26)

    # set margin sizes
    cmsStyle.SetPadTopMargin(0.08)
    cmsStyle.SetPadRightMargin(0.05)
    cmsStyle.SetPadBottomMargin(0.12)
    cmsStyle.SetPadLeftMargin(0.16)

    # set title offsets (for axis label)
    cmsStyle.SetTitleXOffset(1.1)
    cmsStyle.SetTitleYOffset(1.3)

    # use large fonts
    font = 42  # Helvetica
    tsize = 0.05
    cmsStyle.SetTextFont(font)
    cmsStyle.SetTextSize(tsize)

    cmsStyle.SetLabelFont(font, "x")
    cmsStyle.SetTitleFont(font, "x")
    cmsStyle.SetLabelFont(font, "y")
    cmsStyle.SetTitleFont(font, "y")
    cmsStyle.SetLabelFont(font, "z")
    cmsStyle.SetTitleFont(font, "z")

    cmsStyle.SetLabelSize(tsize, "x")
    cmsStyle.SetTitleSize(tsize, "x")
    cmsStyle.SetLabelSize(tsize, "y")
    cmsStyle.SetTitleSize(tsize, "y")
    cmsStyle.SetLabelSize(tsize, "z")
    cmsStyle.SetTitleSize(tsize, "z")

    # use bold lines and markers
    cmsStyle.SetMarkerStyle(20)
    cmsStyle.SetMarkerSize(1.2)
    cmsStyle.SetHistLineWidth(2)
    cmsStyle.SetLineStyleString(2, "[12 12]")  # postscript dashes

    # get rid of error bar caps
    cmsStyle.SetEndErrorSize(0)

    # do not display any of the standard histogram decorations
    cmsStyle.SetOptTitle(0)
    cmsStyle.SetOptStat(0)
    cmsStyle.SetOptFit(0)

    # put tick marks on top and RHS of plots
    cmsStyle.SetPadTickX(1)
    cmsStyle.SetPadTickY(1)

    return cmsStyle

def CmsText(x: float = 0.15, y: float = 0.94, text: str = "",
             color: int = ROOT.kBlack, align: int = 11):
    """Adds CMS label to the canvas at x,y position with additional text

    Arguments:
        x (``float``): x coordinate on the canvas (fraction)
        y (``float``): y coordinate on the canvas (fraction)
        text (``str``): text to be displayed after "CMS"
        color (``int``): ROOT TColor of the text, black by default
        align (``int``): Text alignment (11=top-left, 22=center, 33=bottom-right)
    """
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(61)  # Bold
    l.SetTextSize(0.06)
    l.SetTextColor(color)
    l.SetTextAlign(align)
    l.DrawLatex(x, y, "CMS")

    if text:
        p = ROOT.TLatex()
        p.SetNDC()
        p.SetTextFont(52)  # Italic
        p.SetTextSize(0.045)
        p.SetTextColor(color)
        p.SetTextAlign(align)
        p.DrawLatex(x + 0.15, y, text)

def add_lumi_text(x: float = 0.9, y: float = 0.94, lumi: float = 0,
                  energy: int = 13, unit: str = "fb", align: int = 31):
    """Adds luminosity text to the canvas

    Arguments:
        x (``float``): x coordinate on the canvas (fraction)
        y (``float``): y coordinate on the canvas (fraction)
        lumi (``float``): luminosity value
        energy (``int``): collision energy in TeV
        unit (``str``): luminosity unit (fb or pb)
        align (``int``): Text alignment (11=top-left, 31=top-right)
    """
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextSize(0.045)
    l.SetTextColor(ROOT.kBlack)
    l.SetTextAlign(align)

    if lumi > 0:
        l.DrawLatex(x, y, f"{lumi:.1f} {unit}^{{-1}} ({energy} TeV)")
    else:
        l.DrawLatex(x, y, f"({energy} TeV)")

def recommended_colors():
    """Some recommended ROOT colors for CMS style"""
    return [
        ROOT.kBlack,
        ROOT.kBlue,
        ROOT.kRed,
        ROOT.kGreen+2,
        ROOT.kMagenta+1,
        ROOT.kOrange+7,
        ROOT.kCyan+1,
        ROOT.kYellow+2,
        ROOT.kGray+1,
        ROOT.kViolet-1,
        ROOT.kSpring+5,
        ROOT.kAzure+1,
        ROOT.kPink+7
    ]
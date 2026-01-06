import ROOT

def _apply_common_style():
    """Lightweight ROOT style that matches ATLAS/CMS defaults."""
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTitleFont(42, "XYZ")
    ROOT.gStyle.SetLabelFont(42, "XYZ")
    ROOT.gStyle.SetTextFont(42)
    ROOT.gStyle.SetTitleSize(0.05, "XYZ")
    ROOT.gStyle.SetLabelSize(0.04, "XYZ")
    ROOT.gStyle.SetPadLeftMargin(0.14)
    ROOT.gStyle.SetPadRightMargin(0.06)
    ROOT.gStyle.SetPadTopMargin(0.08)
    ROOT.gStyle.SetPadBottomMargin(0.12)
    ROOT.gStyle.SetLegendBorderSize(0)

def set_atlas_style():
    _apply_common_style()
    ROOT.gStyle.SetPalette(ROOT.kViridis)

def set_cms_style():
    _apply_common_style()
    ROOT.gStyle.SetPalette(ROOT.kViridis)

def atlas_label(x, y, text):
    latex = ROOT.TLatex()
    latex.SetNDC(True)
    latex.SetTextFont(72)  # bold
    latex.SetTextSize(0.05)
    latex.DrawLatex(x, y, f"ATLAS {text}")
    return latex

def cms_label(x, y, text):
    latex = ROOT.TLatex()
    latex.SetNDC(True)
    latex.SetTextFont(61)  # CMS bold
    latex.SetTextSize(0.05)
    latex.DrawLatex(x, y, f"CMS {text}")
    return latex

def add_text(x, y, text, size=0.04):
    latex = ROOT.TLatex()
    latex.SetNDC(True)
    latex.SetTextFont(42)
    latex.SetTextSize(size)
    latex.DrawLatex(x, y, text)
    return latex

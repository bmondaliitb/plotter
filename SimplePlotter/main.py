#!/usr/bin/env python
from config_reader import ConfigReader
from plotting import Plotting
import argparse

from plotter.atlas import SetAtlasStyle

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Plotting script")
    parser.add_argument("-c", "--config", help="Path to the configuration file", required=True)
    args = parser.parse_args()

    SetAtlasStyle()
    config_reader = ConfigReader(args.config)
    config_reader.read_config()
    config_reader.print_config()

    plotter = Plotting(config_reader)
    plotter.generate_plots()
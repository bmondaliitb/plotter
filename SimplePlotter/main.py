#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

if __package__:
    from .config_reader import ConfigReader
    from .plotting import Plotting
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from SimplePlotter.config_reader import ConfigReader
    from SimplePlotter.plotting import Plotting


def main():
    parser = argparse.ArgumentParser(description="Plotting script")
    parser.add_argument("-c", "--config", help="Path to the configuration file", required=True)
    args = parser.parse_args()

    config_reader = ConfigReader(args.config)
    config_reader.read_config()
    config_reader.print_config()

    plotter = Plotting(config_reader)
    plotter.generate_plots()


if __name__ == "__main__":
    main()

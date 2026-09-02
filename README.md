# SimplePlotter

[![Python package](https://github.com/fnechans/plotter/actions/workflows/python-package.yml/badge.svg)](https://github.com/fnechans/plotter/actions/workflows/python-package.yml)

## Table of contents

- [Introduction](#introduction)
- [Installation](#installation)

## Introduction

A small YAML-driven plotting application built on PyROOT. It supports simple TH1,
TH2, overlay/ratio, and stored-canvas plots with ATLAS or CMS styling.


## Installation

Requires ROOT 6 with python3 pyroot.

To install plotter, simply call following in the repository directory:

    $ pip3 install --user -e .

Run a plotting configuration with:

    python3 SimplePlotter/main.py -c share/config.yaml

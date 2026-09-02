from setuptools import find_packages, setup

setup(
    name="simpleplotter",
    version="0.1.0",
    description="A YAML-driven plotting application built on PyROOT",
    packages=find_packages(),
    package_data={"SimplePlotter.plotter": ["extern/shortuuid/COPYING"]},
    install_requires=["PyYAML"],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": ["simple-plotter=SimplePlotter.main:main"],
    },
)

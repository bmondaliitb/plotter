import os
from sample import Sample
from plot import Plot
from plotter import presets
from plotter.presets import Preset
from plotter import atlas

class Plotting:
    def __init__(self, config_reader):
        self.config_reader = config_reader
        self.job_config = config_reader.get_job()
        self.sample_configs = config_reader.get_samples()
        self.plot_configs = config_reader.get_plots()
        # Create actual objects from configurations
        self.samples = self._create_samples(self.sample_configs)
        self.plots = self._create_plots()

    def _create_preset(self, sample_config):
        return Preset(
            fillcolor=sample_config.get('fillcolor', 0),
            fillstyle=sample_config.get('fillstyle', 1001),
            linecolor=sample_config.get('linecolor', 1),
            linewidth=sample_config.get('linewidth', 1),
            markersize=sample_config.get('markersize', 1),
            markerstyle=sample_config.get('markerstyle', 20),
            linestyle=sample_config.get('linestyle', 1)
        )
    def _create_samples(self, sample_configs):
        samples = []
        for sample_config in sample_configs:
            preset = self._create_preset(sample_config)
            sample_obj = Sample(sample_config, preset)
            samples.append(sample_obj)
        return samples

    def _create_plots(self):
        plots = []
        for plot in self.plot_configs:
            plot_obj = Plot(plot)
            plots.append(plot_obj)
        return plots


    def plot_overlay(self):
        comparison_plot = presets.Comparison(self.plots[0].name, self.plots[0].x_label, "Events")

        histo_list = []
        for plot in self.plots:
            for sample in self.samples:
                if sample.name not in plot.samples:
                    continue
                hist = sample.hist
                histo_list.append(hist)

        comparison_plot.add_and_plot(histo_list)
        comparison_plot.canvas.cd()
        atlas.ATLASLabel(0.22, 0.9, "Internal")
        # Save the plot
        if not os.path.exists(self.job_config['job_name']):
            os.makedirs(self.job_config['job_name'])

        comparison_plot.set_xrange(self.plots[0].x_range[0], self.plots[0].x_range[1])
        comparison_plot.save(f"{self.job_config['job_name']}/{self.plots[0].name}.pdf")


    def generate_plots(self):
        """Generate all plots based on the configuration."""
        for plot in self.plot_configs:
            plot_type = plot["type"]
            if plot_type == "overlay":
                self.plot_overlay()
            elif plot_type == "stack":
                self.plot_stack(plot["samples"], plot["name"])
            elif plot_type == "ratio":
                self.plot_ratio(plot["samples"], plot["name"])
            else:
                print(f"Unknown plot type: {plot_type}")

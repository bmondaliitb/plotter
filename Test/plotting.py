import os
from sample import Sample
from plot import Plot
from plotter import presets
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

    def _create_samples(self, sample_configs):
        samples = []
        for sample_config in sample_configs:
            sample_obj = Sample(sample_config)
            samples.append(sample_obj)
        return samples

    def _create_plots(self):
        plots = []
        for plot_config in self.plot_configs:
            plot_obj = Plot(plot_config)
            plots.append(plot_obj)
        return plots

    def plot_overlay(self):

        for plot in self.plots:
            comparison_plot = presets.Comparison(plot.name, plot.x_label, plot.y_label)
            histo_list = []
            for sample in self.samples:
                for plot_sample in plot.samples:
                    if sample.name == plot_sample["name"]:
                        self.apply_style(sample.hist, plot_sample)
                        histo_list.append(sample.hist)

            comparison_plot.mainPad.drawoption = "hist E"
            #comparison_plot.ratioPad.drawoptions = "hist"
            comparison_plot.add_and_plot(histo_list)
            comparison_plot.canvas.cd()
            atlas.ATLASLabel(0.22, 0.9, "Internal")
            # Save the plot
            if not os.path.exists(self.job_config['job_name']):
                os.makedirs(self.job_config['job_name'])
            # if x_range is set, use it
            if plot.x_range:
                comparison_plot.set_xrange(plot.x_range[0], plot.x_range[1])
            comparison_plot.save(f"{self.job_config['job_name']}/{plot.name}.pdf")

    def apply_style(self, hist, style_config):
        hist.SetLineColor(style_config.get('linecolor', 1))
        hist.SetLineStyle(style_config.get('linestyle', 1))
        hist.SetLineWidth(style_config.get('linewidth', 1))
        hist.SetMarkerStyle(style_config.get('markerstyle', 20))

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

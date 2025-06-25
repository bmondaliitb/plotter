import os
import logging
from sample import Sample
from plot import Plot
from plotter import presets
from plotter import atlas

log = logging.getLogger(__name__)

class Plotting:
    def __init__(self, config_reader):
        self.config_reader = config_reader
        self.job_config = config_reader.get_job()
        self.sample_configs = config_reader.get_samples()
        self.plot_configs = config_reader.get_plots()

        # Create actual objects from configurations
        self.samples = self._create_samples(self.sample_configs)
        self.plots = self._create_plots()

        # Get optional configurations
        atlas_label_config = self.job_config.get("atlas_label", "")
        if isinstance(atlas_label_config, dict):
            self.atlas_label_text = atlas_label_config.get("name", "")
            self.atlas_label_pos = atlas_label_config.get("position", [])
        else:
            self.atlas_label_text = atlas_label_config
            self.atlas_label_pos = [0.22, 0.9]
        self.plot_labels = self.job_config.get("plot_label", [])
        self.legend_position = self.job_config.get("legend_position", {})
        self.output_directory = self.job_config.get("output_directory", "output")

        # Create the output directory if it doesn't exist
        self.output_path = os.path.join(self.output_directory, self.job_config['job_name'])
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def _create_samples(self, sample_configs):
        samples = []
        for sample_config in sample_configs:
            sample_obj = Sample(sample_config, self.job_config)
            samples.append(sample_obj)
        return samples

    def _create_plots(self):
        plots = []
        for plot_config in self.plot_configs:
            plot_obj = Plot(plot_config)
            plots.append(plot_obj)
        return plots

    def plot_th1(self, plots_th1):
        for plot in plots_th1:
            simple_plot = presets.simple(plot.name, plot.x_label, plot.y_label)
            histo_list = []
            for sample in self.samples:
                for plot_sample in plot.samples:
                    if sample.name == plot_sample["name"]:
                        self.apply_style(sample.hist, plot_sample)
                        histo_list.append(sample.hist)
                        if not plot.x_label:
                            plot.x_label = sample.hist.th.GetXaxis().GetTitle()
                        if not plot.y_label:
                            plot.y_label = sample.hist.th.GetYaxis().GetTitle()

            simple_plot.mainPad.drawoption = "hist E"
            if getattr(plot, "setlogy", False):
                simple_plot.mainPad.logy()
            if getattr(plot, "setlogx", False):
                simple_plot.mainPad.logx()

            simple_plot.add_and_plot(histo_list)
            simple_plot.canvas.cd()
            if self.atlas_label_text:
                atlas.ATLASLabel(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)

            for label in self.plot_labels:
                atlas.add_text(label["x"], label["y"], label["text"])
            # if x_range is set, use it
            if hasattr(plot, 'x_range') and plot.x_range is not None:
                simple_plot.set_xrange(plot.x_range[0], plot.x_range[1])
            simple_plot.save(f"{self.output_path}/{plot.name}.pdf")

    def plot_th1_ratio(self, plots_th1_ratio):
        for plot in plots_th1_ratio:
            comparison_plot = presets.Comparison(plot.name, plot.x_label, plot.y_label)
            histo_list = []
            for sample in self.samples:
                for plot_sample in plot.samples:
                    if sample.name == plot_sample["name"]:
                        self.apply_style(sample.hist, plot_sample)
                        histo_list.append(sample.hist)
                        if not plot.x_label:
                            plot.x_label = sample.hist.th.GetXaxis().GetTitle()
                        if not plot.y_label:
                            plot.y_label = sample.hist.th.GetYaxis().GetTitle()

            comparison_plot.mainPad.drawoption = "hist E"
            if getattr(plot, "setlogy", False):
                comparison_plot.mainPad.logy()
            if getattr(plot, "setlogx", False):
                comparison_plot.mainPad.logx()
            if hasattr(plot, 'y_range_ratio') and plot.y_range_ratio is not None:
                comparison_plot.ratioPad.set_yrange(plot.y_range_ratio[0], plot.y_range_ratio[1])
            else:
                comparison_plot.ratioPad.set_yrange(0.80, 1.20)
            comparison_plot.add_and_plot(histo_list)
            comparison_plot.canvas.cd()
            if self.atlas_label_text:
                atlas.ATLASLabel(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)
            for label in self.plot_labels:
                atlas.add_text(label["x"], label["y"], label["text"])
            # if x_range is set, use it
            if hasattr(plot, 'x_range') and plot.x_range is not None:
                comparison_plot.set_xrange(plot.x_range[0], plot.x_range[1])
            comparison_plot.save(f"{self.output_path}/{plot.name}.pdf")


    def plot_th2(self, plots_th2):
        for plot in plots_th2:
            simpleTH2_plot = presets.SimpleTH2(plot.name, plot.x_label, plot.y_label)
            histogram = None
            sample_found = False
            for plot_sample in plot.samples:
                for sample in self.samples:
                    if plot_sample["name"] == sample.name:
                        sample_found = True
                        histogram = sample.hist
                        if not plot.x_label:
                            plot.x_label = sample.hist.th.GetXaxis().GetTitle()
                        if not plot.y_label:
                            plot.y_label = sample.hist.th.GetYaxis().GetTitle()
            # if no sample was found, log an error
            if not sample_found:
                log.error(f"ERROR: No sample found for plot {plot.name}")
                return  # Safely exit the function

            simpleTH2_plot.mainPad.drawoption = "colz"
            simpleTH2_plot.add_and_plot(histogram)

            if hasattr(plot, 'x_range') and plot.x_range is not None:
                simpleTH2_plot.set_xrange(plot.x_range[0], plot.x_range[1])
            if hasattr(plot, 'y_range') and plot.y_range is not None:
                simpleTH2_plot.set_yrange(plot.y_range[0], plot.y_range[1])

            #simpleTH2_plot.set_zrange(0, 100) # hardcoded for now
            if hasattr(plot, 'z_range') and plot.z_range is not None:
                simpleTH2_plot.set_zrange(plot.z_range[0], plot.z_range[1])
            else:
                simpleTH2_plot.set_zrange(0, 100)

            simpleTH2_plot.canvas.cd()
            if self.atlas_label_text:
                atlas.ATLASLabel(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)
            for label in self.plot_labels:
                atlas.add_text(label["x"], label["y"], label["text"])
            simpleTH2_plot.save(f"{self.output_path}/{plot.name}.pdf")



    def apply_style(self, hist, style_config):
        hist.SetLineColor(style_config.get('linecolor', 1))
        hist.SetLineStyle(style_config.get('linestyle', 1))
        hist.SetLineWidth(style_config.get('linewidth', 1))
        hist.SetMarkerStyle(style_config.get('markerstyle', 20))

    def generate_plots(self):
        # create plot objects based on plot type
        plots_th1 = [plot for plot in self.plots if plot.type == "simple_th1"]
        plots_th1_ratio = [plot for plot in self.plots if plot.type == "overlay"]
        plots_th2 = [plot for plot in self.plots if plot.type == "simple_th2"]

        if plots_th1 :
            self.plot_th1(plots_th1)
        if plots_th1_ratio:
            self.plot_th1_ratio(plots_th1_ratio)
        if plots_th2:
            self.plot_th2(plots_th2)

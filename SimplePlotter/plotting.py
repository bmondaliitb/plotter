import os
import logging
from sample import Sample
from plot import Plot
from plotter import presets
from plotter import atlas
from plotter import cmsstyle

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

        # set plot style
        self.style = self.job_config.get("style", "atlas").lower()

        # Get optional configurations
        atlas_label_config = self.job_config.get("atlas_label", "")
        if isinstance(atlas_label_config, dict):
            self.atlas_label_text = atlas_label_config.get("name", "")
            self.atlas_label_pos = atlas_label_config.get("position", [])
        else:
            self.atlas_label_text = atlas_label_config
            self.atlas_label_pos = [0.22, 0.9]
        self.plot_labels = self.job_config.get("plot_label", [])
        self.ratio_pad_margin_up = self.job_config.get("ratio_pad_margin_up", 0.05)
        self.ratio_pad_margin_down = self.job_config.get("ratio_pad_margin_down", None)
        self.legend_position = self.job_config.get("legend_position", {})
        self.output_directory = self.job_config.get("output_directory", "output")

        # Create the output directory if it doesn't exist
        self.output_path = os.path.join(self.output_directory, self.job_config['job_name'])
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # save format
        save_format_input = self.job_config.get("save_format", "png")
        self.save_formats = [fmt.strip() for fmt in save_format_input.split(",")] if isinstance(save_format_input, str) else ["png"]

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

    def _get_plot_labels(self, plot):
        labels = getattr(plot, "plot_labels", None)
        if labels is None:
            labels = self.plot_labels
        if isinstance(labels, dict):
            labels = [labels]
        return labels or []

    def _draw_plot_labels(self, labels):
        for label in labels:
            atlas.add_text(
                label["x"],
                label["y"],
                label["text"],
                color=label.get("color", 1),
                font=label.get("font", 42),
                size=label.get("size", 0.04),
            )

    def plot_th1(self, plots_th1):
        for plot in plots_th1:
            draw_legend = plot.config.get("draw_legend", True)
            simple_plot = presets.simple(plot.name, plot.x_label, plot.y_label,
                                         draw_legend=draw_legend,
                                         legend_position=self.legend_position)
            histo_list = []
            sample_by_name = {sample.name: sample for sample in self.samples}
            for plot_sample in plot.samples:
                sample = sample_by_name.get(plot_sample["name"])
                if sample is None:
                    log.warning(f"Sample '{plot_sample['name']}' not found for plot {plot.name}")
                    continue
                self.apply_style(sample.hist, plot_sample)
                histo_list.append(sample.hist)
                if not plot.x_label:
                    plot.x_label = sample.hist.th.GetXaxis().GetTitle()
                if not plot.y_label:
                    plot.y_label = sample.hist.th.GetYaxis().GetTitle()

            drawoption = "hist E" if plot.draw_errors else "hist"
            simple_plot.mainPad.drawoption = drawoption
            if getattr(plot, "setlogy", False):
                simple_plot.mainPad.logy()
            if getattr(plot, "setlogx", False):
                simple_plot.mainPad.logx()

            simple_plot.add_and_plot(histo_list)
            simple_plot.canvas.cd()
            # Set X-axis tick interval if specified
            if hasattr(plot, 'x_tick_interval') and plot.x_tick_interval is not None:
                for hist in histo_list:
                    xmin = hist.th.GetXaxis().GetXmin()
                    xmax = hist.th.GetXaxis().GetXmax()
                    if plot.x_range:
                        xmin, xmax = plot.x_range
                    self.apply_tick_interval(hist.th.GetXaxis(), plot.x_tick_interval, xmin, xmax)
                    break  # Apply to first histogram only

            if self.atlas_label_text:
                if(self.style == "atlas"):
                    atlas.SetAtlasStyle()
                    atlas.ATLASLabel(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)
                if (self.style == "cms"):
                    cmsstyle.SetCmsStyle()
                    cmsstyle.CmsText(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)

            self._draw_plot_labels(self._get_plot_labels(plot))
            # if x_range is set, use it
            if hasattr(plot, 'x_range') and plot.x_range is not None:
                simple_plot.set_xrange(plot.x_range[0], plot.x_range[1])
            for fmt in self.save_formats:
                #simple_plot.save(f"{self.output_path}/{plot.name}_{self.job_config['job_name']}.{fmt}")
                simple_plot.save(f"{self.output_path}/{plot.name}.{fmt}")

    def plot_th1_ratio(self, plots_th1_ratio):
        for plot in plots_th1_ratio:
            draw_legend = plot.config.get("draw_legend", True)
            comparison_plot = presets.Comparison(plot.name, plot.x_label, plot.y_label,
                                                 draw_legend=draw_legend,
                                                 legend_position=self.legend_position,
                                                 draw_ratio_error_band=plot.draw_errors)
            histo_list = []
            sample_by_name = {sample.name: sample for sample in self.samples}
            for plot_sample in plot.samples:
                sample = sample_by_name.get(plot_sample["name"])
                if sample is None:
                    log.warning(f"Sample '{plot_sample['name']}' not found for plot {plot.name}")
                    continue
                self.apply_style(sample.hist, plot_sample)
                histo_list.append(sample.hist)
                if not plot.x_label:
                    plot.x_label = sample.hist.th.GetXaxis().GetTitle()
                if not plot.y_label:
                    plot.y_label = sample.hist.th.GetYaxis().GetTitle()

            drawoption = "hist E" if plot.draw_errors else "hist"
            comparison_plot.mainPad.drawoption = drawoption
            comparison_plot.ratioPad.drawoption = drawoption
            if getattr(plot, "setlogy", False):
                comparison_plot.mainPad.logy()
            if getattr(plot, "setlogx", False):
                comparison_plot.logx() # dont call comparison_plot.mainPad.logx(), that only acts on mainPad not ratio pad
            ratio_pad_margin_up = getattr(plot, "ratio_pad_margin_up", None)
            if ratio_pad_margin_up is None:
                ratio_pad_margin_up = self.ratio_pad_margin_up
            ratio_pad_margin_down = getattr(plot, "ratio_pad_margin_down", None)
            if ratio_pad_margin_down is None:
                ratio_pad_margin_down = self.ratio_pad_margin_down
            if ratio_pad_margin_up is not None or ratio_pad_margin_down is not None:
                comparison_plot.ratioPad.margins(
                    up=ratio_pad_margin_up,
                    down=ratio_pad_margin_down,
                )
            if hasattr(plot, 'y_range_ratio') and plot.y_range_ratio is not None:
                comparison_plot.ratioPad.set_yrange(plot.y_range_ratio[0], plot.y_range_ratio[1])
            else:
                comparison_plot.ratioPad.set_yrange(0.80, 1.20)
            comparison_plot.add_and_plot(histo_list)
            comparison_plot.canvas.cd()
            # Set X-axis tick interval if specified
            if hasattr(plot, 'x_tick_interval') and plot.x_tick_interval is not None:
                # Apply to both main pad and ratio pad histograms
                for hist in histo_list:
                    xmin = hist.th.GetXaxis().GetXmin()
                    xmax = hist.th.GetXaxis().GetXmax()
                    if plot.x_range:
                        xmin, xmax = plot.x_range
                    self.apply_tick_interval(hist.th.GetXaxis(), plot.x_tick_interval, xmin, xmax)
                    break  # Apply to first histogram only

                # Also apply to ratio pad histograms
                for obj in comparison_plot.ratioPad.primitives:
                    if hasattr(obj, 'GetXaxis'):
                        self.apply_tick_interval(obj.GetXaxis(), plot.x_tick_interval, xmin, xmax)
                        break

            if self.atlas_label_text:
                if(self.style == "atlas"):
                    atlas.SetAtlasStyle()
                    atlas.ATLASLabel(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)
                if (self.style == "cms"):
                    cmsstyle.SetCmsStyle()
                    cmsstyle.CmsText(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)
            self._draw_plot_labels(self._get_plot_labels(plot))
            # if x_range is set, use it
            if hasattr(plot, 'x_range') and plot.x_range is not None:
                comparison_plot.set_xrange(plot.x_range[0], plot.x_range[1])
            for fmt in self.save_formats:
                #comparison_plot.save(f"{self.output_path}/{plot.name}_{self.job_config['job_name']}.{fmt}")
                comparison_plot.save(f"{self.output_path}/{plot.name}.{fmt}")


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

            # Set log scale before plotting
            if getattr(plot, "setlogx", False):
                simpleTH2_plot.mainPad.logx()
            if getattr(plot, "setlogy", False):
                simpleTH2_plot.mainPad.logy()
            if getattr(plot, "setlogz", False):
                simpleTH2_plot.mainPad.logz()

            simpleTH2_plot.add_and_plot(histogram)

            # Set X-axis tick interval if specified
            if hasattr(plot, 'x_tick_interval') and plot.x_tick_interval is not None:
                xmin = histogram.th.GetXaxis().GetXmin()
                xmax = histogram.th.GetXaxis().GetXmax()
                if plot.x_range:
                    xmin, xmax = plot.x_range
                self.apply_tick_interval(histogram.th.GetXaxis(), plot.x_tick_interval, xmin, xmax)

            if hasattr(plot, 'x_range') and plot.x_range is not None:
                simpleTH2_plot.set_xrange(plot.x_range[0], plot.x_range[1])
            if hasattr(plot, 'y_range') and plot.y_range is not None:
                simpleTH2_plot.set_yrange(plot.y_range[0], plot.y_range[1])
            if hasattr(plot, 'z_range') and plot.z_range is not None:
                simpleTH2_plot.set_zrange(plot.z_range[0], plot.z_range[1])
            else:
                zmin = histogram.th.GetMinimum()
                zmax = histogram.th.GetMaximum()
                simpleTH2_plot.set_zrange(zmin, zmax)

            simpleTH2_plot.canvas.cd()

            if self.atlas_label_text:
                if(self.style == "atlas"):
                    atlas.SetAtlasStyle()
                    atlas.ATLASLabel(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)
                if (self.style == "cms"):
                    cmsstyle.SetCmsStyle()
                    cmsstyle.CmsText(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)
            self._draw_plot_labels(self._get_plot_labels(plot))
            for fmt in self.save_formats:
                #simpleTH2_plot.save(f"{self.output_path}/{plot.name}_{self.job_config['job_name']}.{fmt}")
                simpleTH2_plot.save(f"{self.output_path}/{plot.name}.{fmt}")

    # plot canvas
    def plot_canvas(self, plots_canvas):
        for plot in plots_canvas:
            for plot_sample in plot.samples:
                for sample in self.samples:
                    if sample.name == plot_sample["name"]:
                        # Get original canvas
                        new_canvas = sample.hist.canvas
                        new_canvas.cd()
                        new_canvas.Draw()

                        # Find the histogram or graph in the canvas
                        for obj in new_canvas.GetListOfPrimitives():
                            # Check if object has axes
                            if hasattr(obj, 'GetXaxis') and hasattr(obj, 'GetYaxis'):
                                # Set axis labels if provided in plot configuration
                                if plot.x_label:
                                    obj.GetXaxis().SetTitle(plot.x_label)
                                if plot.y_label:
                                    obj.GetYaxis().SetTitle(plot.y_label)
                                # Apply axis ranges if specified
                                if hasattr(plot, 'x_range') and plot.x_range is not None:
                                    obj.GetXaxis().SetRangeUser(plot.x_range[0], plot.x_range[1])
                                if hasattr(plot, 'y_range') and plot.y_range is not None:
                                    obj.GetYaxis().SetRangeUser(plot.y_range[0], plot.y_range[1])
                                # Apply tick interval if specified
                                if hasattr(plot, 'x_tick_interval') and plot.x_tick_interval is not None:
                                    xmin = obj.GetXaxis().GetXmin()
                                    xmax = obj.GetXaxis().GetXmax()
                                    if plot.x_range:
                                        xmin, xmax = plot.x_range
                                    self.apply_tick_interval(obj.GetXaxis(), plot.x_tick_interval, xmin, xmax)

                        # Add ATLAS label
                        if self.atlas_label_text:
                            if(self.style == "atlas"):
                                atlas.SetAtlasStyle()
                                atlas.ATLASLabel(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)
                            if (self.style == "cms"):
                                cmsstyle.SetCmsStyle()
                                cmsstyle.CmsText(self.atlas_label_pos[0], self.atlas_label_pos[1], self.atlas_label_text)

                        # Add custom plot labels
                        self._draw_plot_labels(self._get_plot_labels(plot))

                        # Update the canvas
                        new_canvas.Update()

                        # Save the canvas
                        for fmt in self.save_formats:
                            new_canvas.SaveAs(f"{self.output_path}/{plot.name}_{self.job_config['job_name']}.{fmt}")

    def apply_style(self, hist, style_config):
        hist.SetLineColor(style_config.get('linecolor', 1))
        hist.SetLineStyle(style_config.get('linestyle', 1))
        hist.SetLineWidth(style_config.get('linewidth', 1))
        hist.SetMarkerStyle(style_config.get('markerstyle', 20))

        if 'legend' in style_config:
            hist.th.SetTitle(style_config['legend'])

    def apply_tick_interval(self, axis, interval, xmin, xmax):
        if interval is not None:
            axis.SetNdivisions(-1)  # Disable automatic divisions
            # Calculate number of divisions based on interval
            ndiv = int((xmax - xmin) / interval)
            # Ensure a reasonable number of divisions
            ndiv = max(1, min(ndiv, 20))
            axis.SetNdivisions(ndiv, 0, 0, False)

    def generate_plots(self):
        # create plot objects based on plot type
        plots_th1 = [plot for plot in self.plots if plot.type == "simple_th1"]
        plots_th1_ratio = [plot for plot in self.plots if plot.type == "overlay"]
        plots_th2 = [plot for plot in self.plots if plot.type == "simple_th2"]
        plots_canvas = [plot for plot in self.plots if plot.type == "canvas"]

        if plots_th1 :
            self.plot_th1(plots_th1)
        if plots_th1_ratio:
            self.plot_th1_ratio(plots_th1_ratio)
        if plots_th2:
            self.plot_th2(plots_th2)
        if plots_canvas:
            self.plot_canvas(plots_canvas)

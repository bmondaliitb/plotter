This document lists the YAML settings supported by the SimplePlotter config loader.

**Job**
Primary settings:
- `job_name` (string, required): output subfolder name.
- `file_paths` (list of strings, required unless each Sample overrides): ROOT file paths or glob patterns.
- `output_directory` (string, optional): base directory for outputs; defaults to `output`.
- `save_format` (string, optional): comma-separated formats like `png, root`; defaults to `png`.
- `style` (string, optional): `atlas` or `cms`; defaults to `atlas`.

Label and legend settings:
- `atlas_label` (string or dict, optional): string uses default position; dict supports `name` and `position: [x, y]`.
- `plot_label` (list of dicts, optional): each entry has `x`, `y`, `text` for extra annotations.
- `legend_position` (dict, optional): supports `xMin`, `xMax`, `yMax`, `height`, `nColumns`, `textSize`, `textFont`.
- `ratio_pad_margin_up` (number, optional): default top margin for overlay ratio pads.
- `ratio_pad_margin_down` (number, optional): default bottom margin for overlay ratio pads.

Style defaults:
- `CommonStyles` (dict, optional): merged into each `Plot.samples` style entry (keys like `linecolor`, `linestyle`, `linewidth`, `markerstyle`, `legend`).

**Sample**
- `name` (string, required): unique sample identifier.
- `variable` (string, required): object name in the ROOT file.
- `file_paths` (list of strings, optional): overrides Job-level `file_paths` for this sample.
- `normalize` (bool, optional): normalize histogram to unit area.

**Plot**
Core plot fields:
- `name` (string, required): output plot name.
- `type` (string, required): `simple_th1`, `overlay`, `simple_th2`, or `canvas`.
- `samples` (list of dicts, required): sample references and style overrides.
- `x_label` (string, optional): x-axis title.
- `y_label` (string, optional): y-axis title.
- `y_label_ratio` (string, optional): ratio-pad y-axis title; defaults to `Ratio`.
- `y_label_ratio_font_size` (number, optional): ratio-pad y-axis title size.
- `x_label_ratio_font_size` (number, optional): ratio-pad x-axis title size.
- `x_range` (list `[min, max]`, optional): x-axis range.
- `draw_errors` ([true,false]): whether to draw error bar or not

Axis/range options:
- `y_range` (list `[min, max]`, optional): y-axis range.
- `z_range` (list `[min, max]`, optional): z-axis range (TH2 only).
- `x_tick_interval` (number, optional): fixed tick spacing for x-axis.

Display options:
- `setlogx` (bool, optional): log scale for x-axis.
- `setlogy` (bool, optional): log scale for y-axis.
- `setlogz` (bool, optional): log scale for the TH2 color axis, with color contours spaced linearly in `log10(z)`.
- `draw_legend` (bool, optional): draw legend (TH1 and overlay only).
- `y_range_ratio` (list `[min, max]`, optional): ratio pad y-range (overlay only).
- `ratio_pad_margin_up` (number, optional): extra top margin for overlay ratio pads when tick labels are clipped.
- `ratio_pad_margin_down` (number, optional): optional bottom margin override for the ratio pad.
- `plot_label` (list of dicts, optional): plot-specific annotations that override the Job-level `plot_label` for that plot only.
- Each label dict supports `x`, `y`, `text`, and optional `color`, `font`, `size` keys.

Default behavior:
- If a plot does not set `ratio_pad_margin_up` or `ratio_pad_margin_down`, the `Job` values are used.
- If the `Job` block also omits them, the code falls back to `ratio_pad_margin_up = 0.05` and leaves `ratio_pad_margin_down` unset.

Example:
```yaml
plot_label:
  - text: "Dijet, JZ2-JZ9"
    x: 0.25
    y: 0.80
  - text: "response = E_{reco}/E_{truth}"
    x: 0.25
    y: 0.72
```

Per-sample style keys inside `Plot.samples`:
- `name` (string, required): sample name from `Sample`.
- `linecolor` (int, optional): ROOT color index.
- `linestyle` (int, optional): ROOT line style.
- `linewidth` (int, optional): ROOT line width.
- `markerstyle` (int, optional): ROOT marker style.
- `legend` (string, optional): legend entry text.

Notes:
- Some older example configs use `file_path` (singular); the loader currently expects `file_paths` (list).

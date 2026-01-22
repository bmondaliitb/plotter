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
- `x_range` (list `[min, max]`, optional): x-axis range.

Axis/range options:
- `y_range` (list `[min, max]`, optional): y-axis range.
- `z_range` (list `[min, max]`, optional): z-axis range (TH2 only).
- `x_tick_interval` (number, optional): fixed tick spacing for x-axis.

Display options:
- `setlogx` (bool, optional): log scale for x-axis.
- `setlogy` (bool, optional): log scale for y-axis.
- `draw_legend` (bool, optional): draw legend (TH1 and overlay only).
- `y_range_ratio` (list `[min, max]`, optional): ratio pad y-range (overlay only).

Per-sample style keys inside `Plot.samples`:
- `name` (string, required): sample name from `Sample`.
- `linecolor` (int, optional): ROOT color index.
- `linestyle` (int, optional): ROOT line style.
- `linewidth` (int, optional): ROOT line width.
- `markerstyle` (int, optional): ROOT marker style.
- `legend` (string, optional): legend entry text.

Notes:
- Some older example configs use `file_path` (singular); the loader currently expects `file_paths` (list).

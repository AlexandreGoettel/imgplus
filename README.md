# IMGPLUS

Allows using typical pyplot functions to create plots and save figures. The image files are embedded with metadata that lets you programmatically edit and regenerate the plots - with nothing more required than the image file itself!

## Why it's useful

Normally when you save a plot, you lose the plotting commands. To change a line color or add data, you must re-run your original code. With Imgplus, the plot file stores the plotting commands as metadata. You can:

- **Load a plot**, add/modify/delete curves
- **Change styles** (colors, line widths, labels) without re-generating the original data
- **Regenerate** the plot at any resolution


## Example

```python
from imgplus import Imgplus
import numpy as np

# Create and save a plot
iax = Imgplus(figsize=(8, 4.5))
iax.plot(np.linspace(0, 10), np.sin(np.linspace(0, 10)), label="sin")
iax.axhline(0, color="r", linestyle="--")
iax.savefig("my_plot.png")

# Later: load, edit, and re-save
iax = Imgplus.from_file("my_plot.png", figsize=(4.5, 8))

# Change the sin curve to black, dotted
iax.update_curve(0, color="k", linestyle=":")

# Remove the horizontal line
iax.delete_curve(1)

# Save the modified plot
iax.savefig("my_plot_updated.png")
```

> [!TIP] Note
> you can use `iax.show_labels(filename)` to render the plot with each curve labeled by its index. Useful for identifying curve indices when editing. Output is a regular image (no imgplus metadata).

## Supported formats

1. PNG
2. PDF
3. EPS

## TODO

- [ ] Add file size check to prevent embedding metadata in excessively large files
- [ ] Add support for `imshow` and `colorbar`

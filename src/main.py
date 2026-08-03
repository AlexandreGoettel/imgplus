"""Read/Write scientific plots with the means to regenerate themselves."""
import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json


class Uniplot():

    def __init__(self, data=None, **fig_kwargs):
        self.fig_kwargs = fig_kwargs
        if data is None:
            plt.figure(**fig_kwargs)
            self.ax = plt.subplot(111)
            self.data = {"idx": 0}
        else:
            self.data = self.deserialise_keys(data)
            self.ax = self.regenerate_ax(**fig_kwargs)

    @classmethod
    def from_png(cls, filename, **fig_kwargs):
        img = Image.open(filename)
        data = json.loads(img.text["metadata"])
        # TODO: could add fig_kwargs to metadata, but maybe not really important?
        return cls(data, **fig_kwargs)

    @staticmethod
    def serialise(*args):
        output = []
        for arg in args:
            if isinstance(arg, np.ndarray):
                if len(arg.shape) > 1:
                    raise NotImplementedError("Does not support multidimensional arrays")
                arg = list(arg)

            output.append(arg)
        return output

    @staticmethod
    def deserialise_keys(kwargs):
        output = {}
        for k, v in kwargs.items():
            try:
                k = int(k)
            except (TypeError, ValueError):
                pass
            output[k] = v
        return output

    def apply(self, func, *args, **kwargs):
        args = self.serialise(*args)
        self.data[self.data["idx"]] = [func, *args, kwargs]
        self.data["idx"] += 1
        getattr(self.ax, func)(*args, **kwargs)

    def __getattr__(self, x):
        if getattr(self.ax, x, None) is not None:
            def inner(*args, **kwargs):
                return self.apply(x, *args, **kwargs)
            return inner
        else:
            raise AttributeError

    def savefig(self, filename):
        _, ext = os.path.splitext(filename)
        if ext != ".png":
            raise NotImplemented(f"Only .png is supported for now, not '{ext}'")

        metadata_str = json.dumps(self.data)
        pnginfo = PngInfo()
        pnginfo.add_text(key="metadata", value=metadata_str)

        # Save with plt, then re-open to overwrite with metadata
        plt.savefig(filename)
        img = Image.open(filename)
        img.save(filename, pnginfo=pnginfo)

    def iter_curves(self):
        for k, v in self.data.items():
            if k == "idx":
                continue
            yield k, v

    def regenerate_ax(self, **fig_kwargs):
        plt.close()

        self.fig_kwargs.update(fig_kwargs)
        plt.figure(**self.fig_kwargs)
        ax = plt.subplot(111)
        for _, [func, *args, kwargs] in self.iter_curves():
            getattr(ax, func)(*args, **kwargs)
        return ax

    def show_labels(self, filename):
        """
        Plot the saved image with all label indices and save to file.
        This file is not a uniplot file, just a default plt.savefig.
        """
        plt.close()
        plt.figure(**self.fig_kwargs)
        ax = plt.subplot(111)
        for i, [func, *args, kwargs] in self.iter_curves():
            kwargs.update({"label": i})
            getattr(ax, func)(*args, **kwargs)
        ax.legend()
        plt.savefig(filename)

    def update_curve(self, idx, **fig_kwargs):
        """Update the kwargs of a particular curve, then regenerate ax."""
        self.data[idx][-1].update(fig_kwargs)
        self.regenerate_ax()

    def delete_curve(self, idx):
        """Delete curve at position idx, then regenerate ax."""
        del self.data[idx]
        self.regenerate_ax()


# Testing
if __name__ == '__main__':
    x = np.linspace(0, np.pi, 100)

    iax = Uniplot(figsize=(8, 4.5))
    iax.plot(x, np.sin(x), linewidth=2, color="C1", label="sin")
    iax.axhline(0, color="r", linestyle="--")
    iax.savefig("img.png")
    plt.close()

    iax = Uniplot.from_png("img.png", figsize=(4.5, 8))
    iax.plot(x, np.cos(x), color="C2", label="cos")
    # iax.show_labels("img_labels.png")

    iax.update_curve(0, color="k", linestyle=":")
    iax.delete_curve(1)
    plt.show()

    # Todo: imshow
    # Todo: pdf, eps

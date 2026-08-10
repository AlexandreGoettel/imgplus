"""Read/Write scientific plots with the means to regenerate themselves."""
import os
import numpy as np
from matplotlib import pyplot as plt
import json

import imgplus.io as io


class Imgplus:

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
    def from_file(cls, filename, **fig_kwargs):
        """Load a Imgplus from a file. Dispatches based on file extension."""
        _, ext = os.path.splitext(filename)
        # MAINT: Could us importlib to auto check
        if ext == ".png":
            func = io.from_png
        elif ext == ".pdf":
            func = io.from_pdf
        elif ext == ".eps":
            func = io.from_eps
        else:
            raise NotImplementedError(f"Unsupported file format: '{ext}'")

        data = func(filename)
        return cls(data, **fig_kwargs)

    def savefig(self, filename):
        """Wrap plt.savefig to correctly handle metadata."""
        io.savefig(self.metadata, filename)

    @property
    def metadata(self):
        return json.dumps(self.data)

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
        This file is not a imgplus file, just a default plt.savefig.
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

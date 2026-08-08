"""Tests for save/load/update/delete across file formats."""
import os
import shutil
import tempfile
import numpy as np
from matplotlib import pyplot as plt
import pytest

from uniplot import Uniplot

EXTENSIONS = ["pdf", "png", "eps"]


def _make_plot(extension):
    """Create a plot, save it, and return tmpdir + filepath."""
    x = np.linspace(0, np.pi, 100)
    tmpdir = tempfile.mkdtemp()
    filepath = os.path.join(tmpdir, f"test.{extension}")
    iax = Uniplot(figsize=(8, 4.5))
    iax.plot(x, np.sin(x), linewidth=2, color="C1", label="sin")
    iax.axhline(0, color="r", linestyle="--")
    assert iax.data["idx"] == 2
    iax.savefig(filepath)
    plt.close()
    return tmpdir, filepath


@pytest.mark.parametrize("extension", EXTENSIONS)
def test_load(extension):
    """Save and reload preserves the initial plot."""
    tmpdir, filepath = _make_plot(extension)
    try:
        iax = Uniplot.from_file(filepath, figsize=(4.5, 8))
        assert iax.data["idx"] == 2
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.parametrize("extension", EXTENSIONS)
def test_update_curve(extension):
    """Updating a curve changes its properties."""
    tmpdir, filepath = _make_plot(extension)
    try:
        iax = Uniplot.from_file(filepath)
        iax.update_curve(0, color="k", linestyle=":")
        assert iax.data[0][-1]["color"] == "k"
        assert iax.data[0][-1]["linestyle"] == ":"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.parametrize("extension", EXTENSIONS)
def test_delete_curve(extension):
    """Deleting a curve removes it from data."""
    tmpdir, filepath = _make_plot(extension)
    k = 0
    try:
        iax = Uniplot.from_file(filepath)
        iax.delete_curve(k)
        assert k not in iax.data
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

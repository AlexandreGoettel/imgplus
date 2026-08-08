"""I/O functions for Uniplot file formats."""
import os
import json
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from pypdf import PdfReader
from matplotlib import pyplot as plt


# --- PNG ---
def to_png(metadata: str, filename: str):
    """Save a Uniplot to a PNG file with embedded metadata."""
    _, ext = os.path.splitext(filename)
    if ext != ".png":
        raise NotImplementedError(f"Only .png is supported for now, not '{ext}'")

    pnginfo = PngInfo()
    pnginfo.add_text(key="metadata", value=metadata)

    # Save with plt, then re-open to overwrite with metadata
    plt.savefig(filename)
    img = Image.open(filename)
    img.save(filename, pnginfo=pnginfo)


def from_png(filename: str) -> dict:
    """Load a Uniplot from a PNG file with embedded metadata."""
    img = Image.open(filename)
    data = json.loads(img.text["metadata"])
    return data
    # TODO: could add fig_kwargs to metadata, but maybe not really important?


# --- PDF ---
def to_pdf(metadata_str: str, filename: str):
    """Save a Uniplot to a PDF file."""
    # TODO: This can be used for all types
    plt.savefig(
        filename,
        metadata={"metadata": metadata_str},
    )


def from_pdf(filename: str) -> dict:
    """Load a Uniplot from a PDF file."""
    reader = PdfReader(filename)
    metadata = reader.metadata["/metadata"]
    return json.loads(metadata)


# --- EPS ---
def to_eps(uniplot, filename):
    """Save a Uniplot to an EPS file. (skeleton)"""
    _, ext = os.path.splitext(filename)
    if ext != ".eps":
        raise NotImplementedError(f"Only .eps is supported by this function, not '{ext}'")
    # TODO: Implement EPS metadata embedding
    plt.savefig(filename)


def from_eps(filename, **fig_kwargs):
    """Load a Uniplot from an EPS file. (skeleton)"""
    # TODO: Implement EPS metadata reading
    raise NotImplementedError("EPS loading not yet implemented")

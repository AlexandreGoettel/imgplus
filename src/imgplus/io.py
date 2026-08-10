"""I/O functions for Imgplus file formats."""
import os
import json
from PIL import Image
from pypdf import PdfReader
from matplotlib import pyplot as plt

VALID_EXTENSIONS = set((".pdf", ".png", ".eps"))


def savefig(metadata_str: str, filename: str) -> None:
    """Save plot to file with metadata."""
    _, ext = os.path.splitext(filename)
    if ext not in VALID_EXTENSIONS:
        raise NotImplementedError(f"'{ext}' is not supported, must be in {VALID_EXTENSIONS}")

    if ext == ".eps":
        key = "Creator"
    else:
        key = "metadata"

    plt.savefig(
        filename,
        metadata={key: metadata_str},
    )


def from_png(filename: str) -> dict:
    """Load Imgplus metadata from a PNG file."""
    img = Image.open(filename)
    return json.loads(img.text["metadata"])
    # TODO: could add fig_kwargs to metadata, but maybe not really important?


def from_pdf(filename: str) -> dict:
    """Load Imgplus metadata from a PDF file."""
    reader = PdfReader(filename)
    metadata_str = reader.metadata["/metadata"]
    return json.loads(metadata_str)


def from_eps(filename: str) -> dict:
    """Load Imgplus metadata from an EPS file."""
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if "Creator" in line:
                metadata_str = line[11:]
                break
        else:
            raise ValueError("Could not find Imgplus metadata in file.")
    return json.loads(metadata_str)

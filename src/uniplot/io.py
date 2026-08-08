"""I/O functions for Uniplot file formats."""
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
    plt.savefig(
        filename,
        metadata={"metadata": metadata_str},
    )


def from_png(filename: str) -> dict:
    """Load a Uniplot from a PNG file with embedded metadata."""
    img = Image.open(filename)
    data = json.loads(img.text["metadata"])
    return data
    # TODO: could add fig_kwargs to metadata, but maybe not really important?


def from_pdf(filename: str) -> dict:
    """Load a Uniplot from a PDF file."""
    reader = PdfReader(filename)
    metadata = reader.metadata["/metadata"]
    return json.loads(metadata)


# --- EPS ---
# def to_eps(uniplot, filename):
#     """Save a Uniplot to an EPS file. (skeleton)"""
#     _, ext = os.path.splitext(filename)
#     if ext != ".eps":
#         raise NotImplementedError(f"Only .eps is supported by this function, not '{ext}'")
#     # TODO: Implement EPS metadata embedding
#     plt.savefig(filename)


def from_eps(filename, **fig_kwargs):
    """Load a Uniplot from an EPS file. (skeleton)"""
    # TODO: Implement EPS metadata reading
    raise NotImplementedError("EPS loading not yet implemented")

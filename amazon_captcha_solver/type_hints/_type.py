from io import RawIOBase, BufferedIOBase
from pathlib import Path
from typing import TypedDict

from PIL.Image import Image


type StrPath = Path | str
type BinaryIO = RawIOBase | BufferedIOBase
type ImageSource = StrPath | bytes | BinaryIO


TrainingDataType = TypedDict(
    'TrainingDataType',
    {
        'A': set[str],
        'B': set[str],
        'C': set[str],
        'E': set[str],
        'F': set[str],
        'G': set[str],
        'H': set[str],
        'J': set[str],
        'K': set[str],
        'L': set[str],
        'M': set[str],
        'N': set[str],
        'P': set[str],
        'R': set[str],
        'T': set[str],
        'U': set[str],
        'X': set[str],
        'Y': set[str],
    },
)

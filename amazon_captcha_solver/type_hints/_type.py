from io import RawIOBase, BufferedIOBase
from pathlib import Path

from PIL.Image import Image


type StrPath = Path | str
type BinaryIO = RawIOBase | BufferedIOBase
type ImageSource = StrPath | bytes | BinaryIO

from io import BufferedIOBase, RawIOBase
from pathlib import Path


type BinaryIO = RawIOBase | BufferedIOBase
type StrPath = Path | str
type ImageSource = bytes | BinaryIO | StrPath

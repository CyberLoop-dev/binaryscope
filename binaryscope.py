#!/usr/bin/env python3
"""Read-only overview of a local file's header bytes."""

import argparse
from pathlib import Path

SIGNATURES = {
    b"\x89PNG\r\n\x1a\n": "PNG image",
    b"\xff\xd8\xff": "JPEG image",
    b"GIF87a": "GIF image",
    b"GIF89a": "GIF image",
    b"%PDF-": "PDF document",
    b"PK\x03\x04": "ZIP archive",
}


def inspect(path: Path) -> dict:
    with path.open("rb") as stream:
        header = stream.read(32)
    kind = next((label for sig, label in SIGNATURES.items() if header.startswith(sig)), "Unknown")
    return {"name": path.name, "size": path.stat().st_size,
            "type": kind, "header_hex": header.hex(" ")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    result = inspect(args.file)
    for key, value in result.items():
        print(f"{key:>12}: {value}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate, preview, and package a numbered transparent PNG sticker set."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError as error:
    raise SystemExit("Pillow is required: install it in the agent environment before packaging") from error


def numeric_prefix(path: Path) -> int:
    try:
        return int(path.name.split("-", 1)[0])
    except ValueError as error:
        raise SystemExit(f"Sticker filename needs a numeric prefix: {path.name}") from error


def pngs(folder: Path) -> list[Path]:
    files = sorted(folder.glob("*.png"), key=numeric_prefix)
    if not files:
        raise SystemExit(f"No PNG files found in {folder}")
    return files


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(files: list[Path], expected: int, start: int | None = None) -> list[dict[str, object]]:
    if len(files) != expected:
        raise SystemExit(f"Expected {expected} PNGs, found {len(files)}")
    if start is not None:
        actual = [numeric_prefix(path) for path in files]
        wanted = list(range(start, start + expected))
        if actual != wanted:
            missing = sorted(set(wanted) - set(actual))
            repeated = sorted(number for number in set(actual) if actual.count(number) > 1)
            raise SystemExit(f"Numbering mismatch; missing={missing}, repeated={repeated}")

    records: list[dict[str, object]] = []
    hashes: set[str] = set()
    for path in files:
        file_hash = digest(path)
        if file_hash in hashes:
            raise SystemExit(f"Exact duplicate image: {path.name}")
        hashes.add(file_hash)
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            alpha = rgba.getchannel("A")
            low, high = alpha.getextrema()
            if low != 0 or high == 0:
                raise SystemExit(f"Image needs transparent and visible pixels: {path.name}")
            records.append({
                "file": path.name,
                "width": image.width,
                "height": image.height,
                "sha256": file_hash,
            })
    return records


def preview(files: list[Path], destination: Path) -> None:
    columns = min(10, len(files))
    rows = (len(files) + columns - 1) // columns
    cell = 180
    canvas = Image.new("RGB", (columns * cell, rows * cell), (24, 24, 28))
    draw = ImageDraw.Draw(canvas)
    for index, path in enumerate(files):
        with Image.open(path) as source:
            image = source.convert("RGBA")
            image.thumbnail((150, 145), Image.Resampling.LANCZOS)
            left = index % columns * cell + (cell - image.width) // 2
            top = index // columns * cell + 8 + (145 - image.height) // 2
            canvas.paste(image, (left, top), image)
        x = index % columns * cell
        y = index // columns * cell
        label = str(numeric_prefix(path))
        draw.rounded_rectangle((x + 6, y + 153, x + 58, y + 176), 6, fill=(45, 45, 52))
        draw.text((x + 13, y + 157), label, fill=(235, 235, 240))
    canvas.save(destination, quality=92, optimize=True)


def write_zip(destination: Path, files: list[Path]) -> None:
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, path.name)
    with zipfile.ZipFile(destination) as archive:
        if len(archive.namelist()) != len(files):
            raise SystemExit(f"ZIP entry mismatch: {destination}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--additions", type=Path, required=True)
    parser.add_argument("--expected-additions", type=int, required=True)
    parser.add_argument("--start-index", type=int, required=True)
    parser.add_argument("--existing", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--slug", default="reaction-stickers")
    args = parser.parse_args()

    additions = pngs(args.additions)
    records = validate(additions, args.expected_additions, args.start_index)
    args.output_root.mkdir(parents=True, exist_ok=True)
    additions_zip = args.output_root / f"{args.slug}-additions-{len(additions)}.zip"
    preview_path = args.output_root / f"{args.slug}-additions-{len(additions)}-preview.jpg"
    manifest_path = args.output_root / f"{args.slug}-manifest.json"
    write_zip(additions_zip, additions)
    preview(additions, preview_path)

    combined_zip = None
    combined_count = len(additions)
    if args.existing:
        existing = pngs(args.existing)
        combined_dir = args.output_root / f"{args.slug}-{len(existing) + len(additions)}"
        if combined_dir.exists():
            raise SystemExit(f"Combined output already exists; use a fresh output root: {combined_dir}")
        combined_dir.mkdir()
        for path in existing + additions:
            destination = combined_dir / path.name
            if destination.exists():
                raise SystemExit(f"Filename collision in combined pack: {path.name}")
            shutil.copy2(path, destination)
        combined = sorted(combined_dir.glob("*.png"), key=numeric_prefix)
        combined_hashes = [digest(path) for path in combined]
        if len(set(combined_hashes)) != len(combined):
            raise SystemExit("Combined pack contains exact duplicate images")
        combined_count = len(combined)
        combined_zip = args.output_root / f"{args.slug}-{combined_count}.zip"
        write_zip(combined_zip, combined)

    manifest_path.write_text(json.dumps({
        "addition_count": len(additions),
        "combined_count": combined_count,
        "files": records,
    }, indent=2) + "\n")
    print(json.dumps({
        "additions_zip": str(additions_zip),
        "combined_zip": str(combined_zip) if combined_zip else None,
        "preview": str(preview_path),
        "manifest": str(manifest_path),
    }))


if __name__ == "__main__":
    main()

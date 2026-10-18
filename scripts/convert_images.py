"""Convert the site's raster illustrations to lossless WebP without changing their text.

Run from the repository root:

    python scripts/convert_images.py --dry-run
    python scripts/convert_images.py --apply

The conversion keeps image pixels intact unless a small image is enlarged.  The
originals remain in Git history, so ``git restore`` can roll this batch back.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from PIL import Image, ImageFile, ImageOps


ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
CONTENT_EXTENSIONS = {".md", ".html"}
MANIFEST = ROOT / "assets" / "image-conversion-manifest.json"
DISPLAY_SIZES = ROOT / "assets" / "image-original-widths.js"

MARKDOWN_IMAGE = re.compile(r"(!\[[^\]]*\]\()(?P<url>[^)]+)(\))")
HTML_IMAGE = re.compile(
    r"(<img\b[^>]*?\bsrc\s*=\s*['\"])(?P<url>[^'\"]+)(['\"])", re.IGNORECASE
)
LIQUID_PATH = re.compile(r"['\"]([^'\"]+\.(?:png|jpe?g|webp))['\"]", re.IGNORECASE)
IMAGE_SUFFIX = re.compile(r"\.(?:png|jpe?g)(?=[^./]*$)", re.IGNORECASE)


def images() -> list[Path]:
    return sorted(
        p for p in (ROOT / "subjects").rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def content_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*")
        if p.is_file()
        and p.suffix.lower() in CONTENT_EXTENSIONS
        and not any(part in {".git", ".idea"} for part in p.relative_to(ROOT).parts)
    )


def referenced_path(url: str, document: Path) -> Path | None:
    if url.strip().lower().startswith(("http://", "https://", "data:", "//")):
        return None
    liquid = LIQUID_PATH.search(url)
    if liquid:
        path = unquote(liquid.group(1))
    else:
        path = unquote(urlsplit(url.strip().split(" ", 1)[0]).path)
    if not path:
        return None
    if path.startswith("/"):
        return (ROOT / path.lstrip("/")).resolve()
    return (document.parent / path).resolve()


def replace_links(document: Path, text: str, known: set[Path]) -> tuple[str, int]:
    count = 0

    def rewrite(match: re.Match[str]) -> str:
        nonlocal count
        url = match.group("url")
        target = referenced_path(url, document)
        if target not in known:
            return match.group(0)
        suffix = IMAGE_SUFFIX.search(url)
        if suffix is None:
            raise ValueError(f"Cannot rewrite image link in {document}: {url}")
        new_url = url[: suffix.start()] + ".webp" + url[suffix.end() :]
        count += 1
        start, end = match.span("url")
        return match.group(0)[: start - match.start()] + new_url + match.group(0)[end - match.start() :]

    text = MARKDOWN_IMAGE.sub(rewrite, text)
    text = HTML_IMAGE.sub(rewrite, text)
    return text, count


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def convert(source: Path) -> dict[str, object]:
    destination = source.with_suffix(".webp")
    recovered_truncated_source = False
    with Image.open(source) as image:
        try:
            image.load()
        except OSError as error:
            if "truncated" not in str(error).lower():
                raise
            # A few imported JPEGs already have incomplete tails. Preserve
            # everything their browser-visible decoder can recover.
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            try:
                with Image.open(source) as recovered:
                    recovered.load()
                    image = recovered.copy()
                recovered_truncated_source = True
                print(f"Recovered truncated source: {source.relative_to(ROOT)}", flush=True)
            finally:
                ImageFile.LOAD_TRUNCATED_IMAGES = False
        original_size = image.size
        image = ImageOps.exif_transpose(image)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        if image.mode == "RGBA" and image.getchannel("A").getextrema() == (255, 255):
            image = image.convert("RGB")
        width, height = image.size
        # Keep existing high-resolution material pixel-perfect. Small figures
        # receive a bounded 2x Lanczos enlargement for smooth HiDPI display.
        scale = min(2.0, 1600 / width, 6000 / max(width, height)) if width < 800 else 1.0
        if scale > 1.05:
            image = image.resize(
                (round(width * scale), round(height * scale)), Image.Resampling.LANCZOS
            )
        if not destination.exists():
            tmp = destination.with_name(destination.name + ".tmp")
            try:
                image.save(tmp, format="WEBP", lossless=True, method=5, exact=True)
                tmp.replace(destination)
            finally:
                tmp.unlink(missing_ok=True)
        with Image.open(destination) as result:
            result.load()
            if result.size != image.size:
                raise ValueError(f"Unexpected dimensions: {destination}")
            if result.mode != image.mode or result.tobytes() != image.tobytes():
                raise ValueError(f"WebP pixel mismatch: {destination}")
    return {
        "source": source.relative_to(ROOT).as_posix(),
        "output": destination.relative_to(ROOT).as_posix(),
        "source_dimensions": list(original_size),
        "output_dimensions": list(image.size),
        "source_bytes": source.stat().st_size,
        "output_bytes": destination.stat().st_size,
        "source_sha256": sha256(source),
        "output_sha256": sha256(destination),
        "upscaled": image.size != original_size,
        "recovered_truncated_source": recovered_truncated_source,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.dry_run == args.apply:
        parser.error("Choose exactly one of --dry-run and --apply")

    sources = images()
    known = {p.resolve() for p in sources}
    references = 0
    changed_files: list[tuple[Path, str]] = []
    for document in content_files():
        old = document.read_bytes().decode("utf-8")
        new, count = replace_links(document, old, known)
        references += count
        if new != old:
            changed_files.append((document, new))
    print(
        f"Images: {len(sources)}; references: {references}; "
        f"content files to update: {len(changed_files)}",
        flush=True,
    )
    if args.dry_run:
        return

    if MANIFEST.exists():
        raise FileExistsError(f"Manifest exists; refusing to repeat batch: {MANIFEST}")
    entries = []
    for index, source in enumerate(sources, 1):
        entries.append(convert(source))
        if index % 100 == 0 or index == len(sources):
            print(f"Converted {index}/{len(sources)}", flush=True)

    # Change references only after every output has been written and verified.
    for document, new in changed_files:
        document.write_bytes(new.encode("utf-8"))
    for source in sources:
        source.unlink()

    manifest = {
        "method": "lossless WebP; small images upscaled at most 2x with Lanczos",
        "image_count": len(entries),
        "reference_count": references,
        "changed_content_files": len(changed_files),
        "source_bytes": sum(e["source_bytes"] for e in entries),
        "output_bytes": sum(e["output_bytes"] for e in entries),
        "upscaled_count": sum(e["upscaled"] for e in entries),
        "recovered_truncated_count": sum(e["recovered_truncated_source"] for e in entries),
        "images": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    display_widths = {
        entry["output"]: entry["source_dimensions"][0]
        for entry in entries if entry["upscaled"]
    }
    DISPLAY_SIZES.write_text(
        "window.bowenImageOriginalWidths = "
        + json.dumps(display_widths, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"Manifest: {MANIFEST}", flush=True)


if __name__ == "__main__":
    main()

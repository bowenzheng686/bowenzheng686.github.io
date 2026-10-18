"""Validate converted local image files and all Markdown/HTML image links."""

from __future__ import annotations

import json
import sys

from PIL import Image

from convert_images import (
    HTML_IMAGE,
    MANIFEST,
    MARKDOWN_IMAGE,
    ROOT,
    content_files,
    referenced_path,
)


def main() -> int:
    if not MANIFEST.exists():
        print("Missing conversion manifest", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    broken: list[str] = []
    local_references = 0
    for document in content_files():
        text = document.read_text(encoding="utf-8")
        for pattern in (MARKDOWN_IMAGE, HTML_IMAGE):
            for match in pattern.finditer(text):
                target = referenced_path(match.group("url"), document)
                if target is None:
                    continue
                try:
                    target.relative_to(ROOT)
                except ValueError:
                    continue
                if target.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
                    continue
                local_references += 1
                if not target.is_file():
                    broken.append(f"{document.relative_to(ROOT)} -> {match.group('url')}")

    images = manifest["images"]
    expected_paths = {item["output"] for item in images}
    expected_paths.update(item["active"] for item in manifest.get("ai_redrawn", []))
    bad_images: list[str] = []
    for relative_path in sorted(expected_paths):
        path = ROOT / relative_path
        if not path.is_file():
            bad_images.append(relative_path + " missing")
            continue
        try:
            with Image.open(path) as image:
                image.load()
                if image.width < 1 or image.height < 1:
                    bad_images.append(relative_path + " unexpected dimensions")
        except Exception as error:
            bad_images.append(relative_path + " " + str(error))

    actual_paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / "subjects").rglob("*.webp")}
    unexpected = actual_paths - expected_paths
    for path in sorted(unexpected):
        bad_images.append(path + " unrecorded")

    originals = list((ROOT / "subjects").rglob("*.png"))
    originals += list((ROOT / "subjects").rglob("*.jpg"))
    originals += list((ROOT / "subjects").rglob("*.jpeg"))
    print(
        f"Manifest images: {len(images)}; project WebP files: {len(actual_paths)}; "
        f"local references: {local_references}; "
        f"broken references: {len(broken)}; invalid images: {len(bad_images)}; "
        f"unconverted originals: {len(originals)}"
    )
    for problem in (broken + bad_images)[:30]:
        print("ERROR", problem)
    return 1 if broken or bad_images or originals else 0


if __name__ == "__main__":
    raise SystemExit(main())

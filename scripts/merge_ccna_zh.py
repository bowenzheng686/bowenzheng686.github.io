"""Build the CCNA Chinese subject from the two local lecture volumes.

Usage: python scripts/merge_ccna_zh.py [source-lecture-directory]
The source defaults to D:/github.io/materials/networking/lecture.
"""

from __future__ import annotations

import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\github.io\materials\networking\lecture")
DEST = ROOT / "subjects" / "CCNA"
PAGE_TYPES = ("index-zh.html", "references-zh.html", "code-images-zh.html")
APPENDIX_PREFIX = {"index-zh.html": "", "references-zh.html": "ref-", "code-images-zh.html": "code-"}


def chapter_key(path: Path) -> tuple[int, int]:
    volume = int(path.parent.name.removeprefix("volume"))
    chapter = int(path.name.rsplit("chapter", 1)[1])
    return volume, chapter


def output_name(key: tuple[int, int]) -> str:
    return f"v{key[0]}-{key[1]:02d}.html"


def text_of(element) -> str:
    return " ".join("".join(element.itertext()).split())


def escape_yaml(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def rewrite_link(href: str, source_file: Path, source_to_key: dict[Path, tuple[int, int]]) -> str:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:", "//")):
        return href
    if not parsed.path:
        target = source_file
    else:
        target = (source_file.parent / unquote(parsed.path)).resolve()
    if target not in source_to_key:
        raise ValueError(f"Unmapped local link in {source_file}: {href}")
    fragment = parsed.fragment
    if fragment:
        fragment = APPENDIX_PREFIX[target.name] + fragment
    same_chapter = source_to_key[target] == source_to_key[source_file]
    page = "" if same_chapter else output_name(source_to_key[target])
    return page + ("#" + fragment if fragment else "") or "#"


def prepare_main(source_file: Path, source_to_key: dict[Path, tuple[int, int]]):
    document = html.parse(str(source_file))
    main = document.xpath("//main")
    if len(main) != 1:
        raise ValueError(f"Expected exactly one main in {source_file}")
    main = main[0]
    prefix = APPENDIX_PREFIX[source_file.name]
    for element in main.iter():
        if element.get("id") and prefix:
            element.set("id", prefix + element.get("id"))
        if element.get("name") and prefix:
            element.set("name", prefix + element.get("name"))
        if element.get("aria-describedby") and prefix:
            element.set("aria-describedby", " ".join(prefix + item for item in element.get("aria-describedby").split()))
        if element.get("aria-labelledby") and prefix:
            element.set("aria-labelledby", " ".join(prefix + item for item in element.get("aria-labelledby").split()))
        if element.get("href"):
            element.set("href", rewrite_link(element.get("href"), source_file, source_to_key))
        if element.get("src"):
            src = element.get("src")
            asset = (source_file.parent / unquote(src)).resolve()
            if not asset.is_file() or asset.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"):
                raise ValueError(f"Missing or unsupported image in {source_file}: {src}")
            relative_chapter = source_file.parent.relative_to(SOURCE)
            element.set("src", (Path("assets") / relative_chapter / "images" / asset.name).as_posix())
    return main


def render_children(main) -> str:
    chunks = []
    if main.text and main.text.strip():
        chunks.append(main.text)
    for child in main:
        chunks.append(html.tostring(child, encoding="unicode", method="html"))
    return "\n".join(chunks).replace("\r\n", "\n").replace("\r", "\n")


def nav_link(label: str, key: tuple[int, int] | None) -> str:
    if key is None:
        return "<span></span>"
    return f'<a href="{output_name(key)}">{label}</a>'


def build():
    chapter_dirs = sorted(SOURCE.glob("volume*/part*-chapter*"), key=chapter_key)
    if not chapter_dirs:
        raise ValueError(f"No chapters found in {SOURCE}")
    source_to_key = {
        (directory / filename).resolve(): chapter_key(directory)
        for directory in chapter_dirs
        for filename in PAGE_TYPES
        if (directory / filename).is_file()
    }
    groups: dict[tuple[int, int], list[tuple[tuple[int, int], str]]] = defaultdict(list)
    keys = [chapter_key(directory) for directory in chapter_dirs]
    image_sources = sorted(SOURCE.glob("volume*/part*-chapter*/assets/images/*"))
    if len(image_sources) != 1035:
        raise ValueError(f"Expected 1035 source images, found {len(image_sources)}")
    DEST.mkdir(parents=True, exist_ok=True)

    for position, directory in enumerate(chapter_dirs):
        key = chapter_key(directory)
        source_file = directory / "index-zh.html"
        document = html.parse(str(source_file))
        title_elements = document.xpath('//main//h2[contains(concat(" ", normalize-space(@class), " "), " h2a ")]')
        part_elements = document.xpath('//header//p[starts-with(@id,"part")]')
        if not title_elements or not part_elements:
            raise ValueError(f"Missing chapter title or part label in {source_file}")
        title = text_of(title_elements[0])
        part = int(re.search(r"part(\d+)", directory.name).group(1))
        part_title = text_of(part_elements[0]).split("：", 1)[-1]
        groups[(key[0], part)].append((key, title))

        sections = []
        for filename in PAGE_TYPES:
            path = directory / filename
            if not path.is_file():
                continue
            main = prepare_main(path, source_to_key)
            if filename == "index-zh.html":
                sections.append(f'<div class="ccna-source ccna-chapter">\n{render_children(main)}\n</div>')
            else:
                heading = "答案解析与术语表" if filename == "references-zh.html" else "代码原图"
                sections.append(f'<section class="ccna-source ccna-appendix" aria-label="{heading}">\n{render_children(main)}\n</section>')

        previous = keys[position - 1] if position else None
        following = keys[position + 1] if position + 1 < len(keys) else None
        volume_name = "第一卷" if key[0] == 1 else "第二卷"
        nav = '<nav class="ccna-chapter-nav" aria-label="章节导航">' + nav_link("← 上一章", previous) + nav_link("下一章 →", following) + "</nav>"
        page = (
            "---\n"
            "layout: default\n"
            f"title: {escape_yaml(f'CCNA 网络技术 · {volume_name}第 {key[1]} 章 · {title}')}\n"
            "subject_page: true\n"
            "ccna_notes: true\n"
            "---\n\n"
            '<p class="ccna-back"><a href="{{ \'/subjects/CCNA/\' | relative_url }}">← 返回 CCNA 目录</a></p>\n'
            f'<p class="ccna-part-label">{volume_name} · {part_title}</p>\n'
            + nav + f"\n\n{{% raw %}}\n<span id=\"part{part:02d}\"></span>\n"
            + "\n\n".join(sections)
            + "\n{% endraw %}\n\n"
            + nav + "\n"
        )
        (DEST / output_name(key).replace(".html", ".md")).write_text(page, encoding="utf-8", newline="\n")

    index_lines = [
        "---", "layout: default", "title: CCNA 网络技术", "subject_page: true", "---", "",
        "# CCNA 网络技术", "",
        "第一卷和第二卷中文内容按原书的部分与章节整合。每章包含完整正文、自测答案解析、术语表，以及原书提供的代码原图；保留原始插图。", "",
    ]
    for volume in (1, 2):
        index_lines += [f"## {'第一卷' if volume == 1 else '第二卷'}", ""]
        for (group_volume, part), entries in sorted(groups.items()):
            if group_volume != volume:
                continue
            first_dir = next(directory for directory in chapter_dirs if chapter_key(directory) == entries[0][0])
            first_doc = html.parse(str(first_dir / "index-zh.html"))
            label = text_of(first_doc.xpath('//header//p[starts-with(@id,"part")]')[0]).split("：", 1)[-1]
            index_lines += [f"### 第 {part} 部分 · {label}", "", "<ol>"]
            for key, title in entries:
                index_lines.append(f'  <li><a href="{{{{ \'/subjects/CCNA/{output_name(key)}\' | relative_url }}}}">第 {key[1]} 章 · {title}</a></li>')
            index_lines += ["</ol>", ""]
    (DEST / "index.md").write_text("\n".join(index_lines), encoding="utf-8", newline="\n")

    for source in image_sources:
        if not source.is_file():
            raise ValueError(f"Unexpected non-file image path: {source}")
        destination = DEST / "assets" / source.parent.parent.parent.relative_to(SOURCE) / "images" / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    print(f"Generated {len(chapter_dirs)} chapters, {len(source_to_key)} Chinese source pages, {len(image_sources)} images in {DEST}")


if __name__ == "__main__":
    build()

"""Build the publishable static site into dist/."""

from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
PAGES = (
    "index.html",
    "journal.html",
    "experiments.html",
    "laboratory.html",
    "sources.html",
    "manifesto.html",
    "contact.html",
)
LOCALES = ("", "ru", "zh")
PREVIEW_MARKERS = (
    "LOCAL PREVIEW",
    "UNPUBLISHED",
    "НЕ ОПУБЛИКОВАНО",
    "本地预览",
    "尚未发布",
    "DEMO DRAFT",
    "DEMO ISSUE",
    "ЧЕРНОВИК ДЛЯ ДЕМО",
    "ДЕМОНСТРАЦИОННЫЙ ВЫПУСК",
    "演示草稿",
    "演示版",
)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        if tag not in {"a", "link", "img", "script"}:
            return
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.targets.append(value)


subprocess.run([sys.executable, str(ROOT / "build_demo.py")], check=True)
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()

for locale in LOCALES:
    target = DIST / locale
    target.mkdir(exist_ok=True)
    for page in PAGES:
        shutil.copy2(ROOT / locale / page, target / page)

shutil.copy2(ROOT / "style.css", DIST / "style.css")
shutil.copytree(ROOT / "assets", DIST / "assets")
(DIST / ".nojekyll").touch()

for page in sorted(DIST.rglob("*.html")):
    html = page.read_text(encoding="utf-8")
    for marker in PREVIEW_MARKERS:
        if marker in html:
            raise SystemExit(f"Preview text in {page.relative_to(DIST)}: {marker}")
    links = Links()
    links.feed(html)
    for link in links.targets:
        parsed = urlsplit(link)
        if parsed.scheme or link.startswith("#"):
            continue
        target = (page.parent / unquote(parsed.path)).resolve()
        if not target.is_file() or not target.is_relative_to(DIST.resolve()):
            raise SystemExit(f"Broken local link in {page.relative_to(DIST)}: {link}")

print(f"Release ready: {len(PAGES) * len(LOCALES)} pages in {DIST}")

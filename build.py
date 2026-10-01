#!/usr/bin/env python3
"""
Простой генератор статического сайта.
Читает Markdown из content/, конфиг из config.json,
подставляет в шаблон templates/base.html и сохраняет в public/.
"""

import json
import shutil
from pathlib import Path

try:
    import markdown
except ImportError:
    raise SystemExit(
        "Не установлена библиотека 'markdown'.\n"
        "Установите её командой:\n"
        "    pip install markdown"
    )

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
PUBLIC_DIR = ROOT / "public"


def load_config():
    with open(ROOT / "config.json", encoding="utf-8") as f:
        return json.load(f)


def read_markdown(name):
    path = CONTENT_DIR / f"{name}.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    return markdown.markdown(text, extensions=["extra", "sane_lists"])


def render_template(template_text, context):
    # Простейший шаблонизатор: {{ key }} -> значение
    result = template_text
    for key, value in context.items():
        result = result.replace("{{ " + key + " }}", str(value))
        result = result.replace("{{" + key + "}}", str(value))
    return result


def build():
    config = load_config()

    sections = {
        "hero":       read_markdown("hero"),
        "teaching":   read_markdown("teaching"),
        "education":  read_markdown("education"),
        "approach":   read_markdown("approach"),
        "experience": read_markdown("experience"),
    }

    context = {
        "name":       config["name"],
        "tagline":    config["tagline"],
        "price_rub":  config["price_rub"],
        "price_usd":  config["price_usd"],
        "email":      config["email"],
        "year":       "2025",
        **sections,
    }

    template_text = (TEMPLATES_DIR / "base.html").read_text(encoding="utf-8")
    html = render_template(template_text, context)

    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir(parents=True)
    (PUBLIC_DIR / "index.html").write_text(html, encoding="utf-8")

    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, PUBLIC_DIR / "static")

    print(f"✔ Сайт собран: {PUBLIC_DIR / 'index.html'}")
    print("  Откройте его в браузере или запустите:")
    print(f"      cd public && python -m http.server 8000")


if __name__ == "__main__":
    build()
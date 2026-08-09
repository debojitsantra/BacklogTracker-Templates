#!/usr/bin/env python3

from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

#configs
DATA_DIR = Path("data")
OUTPUT_FILE = Path("data.md")
GITHUB_OWNER = "debojitsantra"
GITHUB_REPO = "BacklogTracker-Templates"
GITHUB_BRANCH = "main"
DEFAULT_EMOJI = "📌"
DEFAULT_COLOR = "#6750a4"
VALID_DAYS = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
VALID_GROWTH_MODES = {"perday", "repeat", "none"}
VALID_COMPLETION_MODES = {"backlog", "todo"}

# Boilerplate descriptions 

GENERIC_DESCRIPTIONS = {
    "shared backlog tracker template",
}

MARKER_RE = re.compile(r"<!--\s*template:\s*(.+?)\s*-->")


def load_already_documented(text: str) -> set[str]:
    return set(MARKER_RE.findall(text))


def pick_item_source(data: dict):
    for key in ("items", "subjects", "games", "work", "tasks", "categories"):
        if key in data and data[key]:
            return data[key]
    return None


def normalize_items(source) -> list[dict]:
    if source is None:
        return []

    if isinstance(source, list):
        raw_entries = [
            (item.get("name") or item.get("title") or item.get("label") or f"Item {i + 1}", item)
            for i, item in enumerate(source)
            if isinstance(item, dict)
        ]
    elif isinstance(source, dict):
        raw_entries = list(source.items())
    else:
        return []

    normalized = []
    for fallback_name, item in raw_entries:
        if not isinstance(item, dict):
            continue

        name = str(item.get("name") or item.get("title") or item.get("label") or fallback_name).strip()
        if not name:
            continue

        entry = {
            "name": name,
            "emoji": (item.get("emoji") or DEFAULT_EMOJI).strip() or DEFAULT_EMOJI,
            "color": (item.get("color") or DEFAULT_COLOR).strip() or DEFAULT_COLOR,
        }

        perday = item.get("perday", item.get("daily_increase"))
        if isinstance(perday, (int, float)):
            entry["perday"] = perday

        perday_type = item.get("perday_type")
        if isinstance(perday_type, str) and perday_type.strip():
            entry["perday_type"] = perday_type.strip()

        repeat_days = item.get("repeat_days")
        if isinstance(repeat_days, list):
            days = [d for d in repeat_days if isinstance(d, str) and d in VALID_DAYS]
            if days:
                entry["repeat_days"] = days

        backlog = item.get("backlog")
        if isinstance(backlog, (int, float)):
            entry["backlog"] = backlog

        growth_mode = item.get("growth_mode")
        if isinstance(growth_mode, str) and growth_mode.strip() in VALID_GROWTH_MODES:
            entry["growth_mode"] = growth_mode.strip()

        completion_mode = item.get("completion_mode")
        if isinstance(completion_mode, str) and completion_mode.strip() in VALID_COMPLETION_MODES:
            entry["completion_mode"] = completion_mode.strip()

        normalized.append(entry)

    return normalized


def filename_to_title(filename: str) -> str:
    stem = re.sub(r"\.json$", "", filename, flags=re.IGNORECASE)
    words = re.split(r"[-_]+", stem)
    return " ".join(w.capitalize() for w in words if w)


def build_item_details(it: dict) -> str:
    details = []
    growth_mode = it.get("growth_mode")

    if growth_mode == "none":
        details.append("one-time")
    elif "perday" in it:
        unit = it.get("perday_type", "per day")
        details.append(f"{it['perday']} {unit}")

    if "repeat_days" in it:
        details.append("repeats: " + ", ".join(it["repeat_days"]))

    if "backlog" in it:
        details.append(f"backlog: {it['backlog']}")

    if it.get("completion_mode") == "todo":
        details.append("todo item")

    return "; ".join(details) if details else "—"


def download_url(filename: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/"
        f"{GITHUB_BRANCH}/{DATA_DIR.name}/{filename}"
    )


def build_entry_markdown(filename: str, data: dict) -> str:
    title = (
        (data.get("title") or "").strip()
        or (data.get("name") or "").strip()
        or (data.get("template_name") or "").strip()
        or (data.get("course_name") or "").strip()
        or filename_to_title(filename)
    )

    description = (data.get("description") or "").strip()
    if description.lower() in GENERIC_DESCRIPTIONS:
        description = ""
    items = normalize_items(pick_item_source(data))

    lines = []
    lines.append(f"<!-- template: {filename} -->")
    lines.append(f"### {title}")
    lines.append("")
    if description:
        lines.append(description)
        lines.append("")

    meta_bits = []
    if isinstance(data.get("classes_per_day"), (int, float)):
        meta_bits.append(f"classes/day: `{data['classes_per_day']}`")
    if "skip_sunday" in data:
        meta_bits.append(f"skip Sunday: `{bool(data['skip_sunday'])}`")
    if meta_bits:
        lines.append(" · ".join(meta_bits))
        lines.append("")

    lines.append(f"**{len(items)} item(s)** · source: `{filename}`")
    lines.append("")

    if items:
        lines.append("| | Name | Details |")
        lines.append("|---|---|---|")
        for it in items:
            details_str = build_item_details(it)
            lines.append(f"| {it['emoji']} | {it['name']} | {details_str} |")
        lines.append("")

    lines.append(f"[⬇ Download {filename}]({download_url(filename)})")
    lines.append("")

    added = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines.append(f"_Added {added}_")
    lines.append("")
    lines.append(f"<!-- /template: {filename} -->")
    lines.append("")

    return "\n".join(lines)


HEADER = (
    "# Backlog Tracker — Templates\n\n"
    "Auto-generated using scripts/append.py \n\n"
)


def main() -> int:
    if not DATA_DIR.exists():
        print(f"error: data dir '{DATA_DIR}' does not exist", file=sys.stderr)
        return 1

    if OUTPUT_FILE.exists():
        existing_text = OUTPUT_FILE.read_text(encoding="utf-8")
    else:
        OUTPUT_FILE.write_text(HEADER, encoding="utf-8")
        existing_text = HEADER

    already_done = load_already_documented(existing_text)

    json_files = sorted(p for p in DATA_DIR.glob("*.json"))
    new_blocks = []
    skipped_bad = []

    for path in json_files:
        if path.name in already_done:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            skipped_bad.append((path.name, str(e)))
            continue

        items = normalize_items(pick_item_source(data))
        if not items:
            skipped_bad.append((path.name, "no usable items/subjects found"))
            continue

        new_blocks.append(build_entry_markdown(path.name, data))

    if not new_blocks:
        print("No new templates to add. DATA.md is already up to date.")
    else:
        with OUTPUT_FILE.open("a", encoding="utf-8") as f:
            for block in new_blocks:
                f.write(block)
                f.write("\n")
        print(f"Added {len(new_blocks)} new template(s) to {OUTPUT_FILE}:")
        for path in json_files:
            if path.name not in already_done and any(path.name in b for b in new_blocks):
                print(f"  + {path.name}")

    if skipped_bad:
        print("\nSkipped (invalid or empty):")
        for name, reason in skipped_bad:
            print(f"  - {name}: {reason}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

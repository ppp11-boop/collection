#!/usr/bin/env python3
"""Offline pre-submission checks for the ARTT3005 collection."""

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "records.json"
REQUIRED = ("title", "date", "place", "recorder", "not_captured", "certainty")
ALLOWED_TYPES = {"image", "sound", "text"}
ALLOWED_CERTAINTY = {"high", "medium", "low"}


def main() -> int:
    errors = []
    try:
        records = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Could not read valid records.json: {exc}")
        return 1

    if not isinstance(records, list):
        print("ERROR: records.json must contain one JSON array.")
        return 1

    if len(records) != 20:
        errors.append(f"Found {len(records)} records; exactly 20 are required.")

    types = Counter(record.get("type") for record in records if isinstance(record, dict))
    if types["image"] < 6:
        errors.append(f"Found {types['image']} image records; at least 6 are required.")
    if types["sound"] < 1:
        errors.append("No sound record was found.")
    if types["text"] < 1:
        errors.append("No text record was found.")

    seen_ids = set()
    for position, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"Record {position} is not a JSON object.")
            continue

        record_id = record.get("id")
        if record_id in seen_ids:
            errors.append(f"Record ID {record_id!r} is duplicated.")
        seen_ids.add(record_id)

        for field in REQUIRED:
            value = record.get(field)
            if value is None or not str(value).strip():
                errors.append(f"Record {position} is missing {field}.")

        if record.get("type") not in ALLOWED_TYPES:
            errors.append(f"Record {position} has invalid type {record.get('type')!r}.")
        if str(record.get("certainty", "")).lower() not in ALLOWED_CERTAINTY:
            errors.append(f"Record {position} certainty must be high, medium or low.")

        for field, value in record.items():
            if isinstance(value, str) and re.search(r"\[(ENTER|PASTE)", value, re.I):
                errors.append(f"Record {position} still has a placeholder in {field}.")

        filename = record.get("file")
        if not filename:
            errors.append(f"Record {position} has no file path.")
        else:
            media_path = (ROOT / filename).resolve()
            try:
                media_path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"Record {position} points outside the collection folder.")
            else:
                if not media_path.is_file():
                    errors.append(f"Missing media file: {filename}")

    concept_files = list(ROOT.glob("*-collection-concept.md"))
    if len(concept_files) != 1:
        errors.append("There must be exactly one correctly named *-collection-concept.md file.")
    else:
        concept = concept_files[0].read_text(encoding="utf-8")
        word_count = len(re.findall(r"\b[\w'-]+\b", concept))
        if word_count >= 500:
            errors.append(f"Concept statement has {word_count} words; it must be under 500.")
        if "PASTE YOUR GITHUB" in concept:
            errors.append("The concept statement still needs your GitHub repository link.")

    if ROOT.name.startswith("studentID-"):
        errors.append("Rename the collection folder using your real student ID and name.")

    if errors:
        print(f"NOT READY - {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print("READY - all automatic checks passed.")
    print("Final manual check: preview all images, play both sounds and read every text record.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

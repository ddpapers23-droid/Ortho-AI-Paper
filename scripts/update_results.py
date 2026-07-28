"""Apply a batch of screening decisions to screening_results.csv.

Reads a JSON file: {"Fractured/IMG0000019.jpg": {"decision": "EXCLUDE", ...}, ...}
and updates matching rows by filename, setting status="done".
"""

import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "screening_results.csv"

FIELDS = [
    "filename",
    "source_category",
    "decision",
    "fracture_location",
    "view_type",
    "hardware_present",
    "image_quality",
    "primary_reason",
    "confidence",
    "status",
]


def main(updates_path):
    updates = json.loads(Path(updates_path).read_text())

    with CSV_PATH.open() as f:
        rows = list(csv.DictReader(f))

    applied = 0
    missing = set(updates.keys())
    for row in rows:
        if row["filename"] in updates:
            row.update(updates[row["filename"]])
            row["status"] = "done"
            applied += 1
            missing.discard(row["filename"])

    with CSV_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied {applied} updates.")
    if missing:
        print(f"WARNING: {len(missing)} filenames not found: {sorted(missing)}")


if __name__ == "__main__":
    main(sys.argv[1])

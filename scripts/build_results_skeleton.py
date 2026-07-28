"""Build screening_results.csv skeleton from images/Fractured and images/Non_fractured.

Non_fractured images are deterministically EXCLUDEd (no fracture present fails
inclusion criterion 3), so they don't need visual review. Fractured images are
left as pending rows for manual visual screening against the tibial-shaft-fracture
inclusion/exclusion criteria.
"""

import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
OUT_PATH = REPO_ROOT / "screening_results.csv"

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


def main():
    rows = []

    non_fractured_dir = IMAGES_DIR / "Non_fractured"
    for path in sorted(non_fractured_dir.glob("*.jpg")):
        rows.append({
            "filename": f"Non_fractured/{path.name}",
            "source_category": "Non_fractured",
            "decision": "EXCLUDE",
            "fracture_location": "N/A",
            "view_type": "Unclear",
            "hardware_present": "No",
            "image_quality": "N/A",
            "primary_reason": "Source-labeled non-fractured; no fracture present (fails inclusion criterion 3).",
            "confidence": "High",
            "status": "done",
        })

    fractured_dir = IMAGES_DIR / "Fractured"
    for path in sorted(fractured_dir.glob("*.jpg")):
        rows.append({
            "filename": f"Fractured/{path.name}",
            "source_category": "Fractured",
            "decision": "",
            "fracture_location": "",
            "view_type": "",
            "hardware_present": "",
            "image_quality": "",
            "primary_reason": "",
            "confidence": "",
            "status": "pending",
        })

    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    done = sum(1 for r in rows if r["status"] == "done")
    pending = sum(1 for r in rows if r["status"] == "pending")
    print(f"Wrote {len(rows)} rows to {OUT_PATH} ({done} done, {pending} pending)")


if __name__ == "__main__":
    main()

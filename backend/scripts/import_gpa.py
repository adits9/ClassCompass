# backend/scripts/import_gpa.py

import csv
from pathlib import Path
from api.models import Course


def load_gpa_csv(csv_path: str):
    """
    Parse Wade Fagen's GPA dataset and insert/update Course rows.

    Expected columns in uiuc-gpa-dataset.csv include:
    - Subject (e.g. "CS")
    - Number (e.g. "225")
    - Course Title (e.g. "Data Structures")
    - Students (enrollment count for that section)
    - plus columns for grade counts (A, A-, B+, ...)

    We'll use Subject + Number as our course_id, and Course Title for title.
    Credits are unknown in this dataset, so we default to 4 for now or leave 3.
    Dept is just Subject.
    """
    csv_path = Path(csv_path)

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        created = 0
        updated = 0

        for row in reader:
            subject = row.get("Subject", "").strip()
            number = row.get("Number", "").strip()
            title = row.get("Course Title", "").strip()

            if not subject or not number or not title:
                continue

            course_id = f"{subject} {number}"  # e.g. "CS 225"

            # naive guess for credits (can refine later with catalog data)
            default_credits = 4 if subject == "CS" else 3

            obj, was_created = Course.objects.get_or_create(
                course_id=course_id,
                defaults={
                    "dept": subject,
                    "title": title,
                    "credits": default_credits,
                },
            )

            if was_created:
                created += 1
            else:
                # if title changed / dept changed over time, we could refresh it
                changed = False
                if obj.title != title:
                    obj.title = title
                    changed = True
                if obj.dept != subject:
                    obj.dept = subject
                    changed = True
                if changed:
                    obj.save()
                    updated += 1

        print(f"[import_gpa] created {created} courses, updated {updated} courses")

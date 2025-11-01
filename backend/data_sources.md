# Course & GPA Data Sources

Source:
- "UIUC GPA Dataset" from wadefagen/datasets (GitHub).
  - Public FOIA + Illinois Student Council GPA data
  - File: `gpa/uiuc-gpa-dataset.csv`
  - Contains course subject, number, title, instructor, term, and grade distribution.
  - Rows are per course section per term.

Why we care:
- We can compute an "avg GPA" / "difficulty proxy" per course.
- We can attach that to `Course` in our DB later as a signal.

Planned pipeline:
1. Download `uiuc-gpa-dataset.csv` locally (not committed to git if it's big).
2. Run `python manage.py shell` and call our `import_gpa` helper to:
   - create any missing Course rows
   - (later) calculate an average GPA and store it in a signals table

Status:
- Script stub exists in `scripts/import_gpa.py`
- Not wired into production yet.
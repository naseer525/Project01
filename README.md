# DSA Lab 4 — Part 2 (PyQt5 CRUD)

This is a repaired version of the sample project in the lab materials. It uses the original `scrape.ui` from Qt Designer (with improved field placeholders, a Lab 4 heading, and two extra controls).

## Setup (Windows / VS Code)

1. Open this directory in Visual Studio Code.
2. Check Python: `py --version`
3. Install GUI dependencies: `py -m pip install -r requirements.txt`
4. Run: `py main.py`
5. Add a record, choose Refresh Records to read the CSV, select a row to edit/delete.
6. Close the app and re-open it to verify persistence.

`student.csv` is created next to `main.py` when the app launches. If you wish to test with demonstration data, copy `student_example.csv` to `student.csv` *before launching*. The included sample intentionally contains fictional records and should not be used as real student data.

## Architecture

- `scrape.ui`: front end made in Qt Designer
- `main.py`: event-handling, validation, CRUD operations
- `student.csv`: persistent store; created automatically and ignored by Git

## Upload

Create your repo on GitHub or GitLab and run the normal Git commands from this folder. The lab manual specifically asks for a **GitLab** URL submitted to Eduko; please confirm whether GitHub is acceptable before submitting your GitHub link.

Only add the application source and non-sensitive example data. `.gitignore` excludes `student.csv` to avoid publishing people's phone numbers.

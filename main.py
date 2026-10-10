"""DSA Lab 4, Part 2: PyQt5 Student CRUD with persistent CSV storage.

Uses the instructor's Qt Designer interface (scrape.ui).
Run: py main.py
"""

import csv
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "student.csv"
UI_FILE = BASE_DIR / "scrape.ui"


class StudentCRUD(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(str(UI_FILE), self)

        self.records = []
        self.selected_reg = None

        # Keep the supplied design, including its custom title-bar buttons.
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.CrossButton.clicked.connect(self.close)

        # Readable input placeholders.
        fields = {
            self.NameEdit: "Student Name",
            self.RegEdit: "Registration Number",
            self.gpaEdit: "GPA (0 to 4)",
            self.NumberEdit: "Phone Number",
            self.uniEdit: "University",
        }
        for widget, placeholder in fields.items():
            widget.clear()
            widget.setPlaceholderText(placeholder)

        # Make it obvious which full row is being edited or deleted.
        table = self.StuInfoTable
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        table.setHorizontalHeaderLabels(
            ["Student Name", "Registration Number", "GPA", "Phone", "University"]
        )
        table.itemSelectionChanged.connect(self.fill_values)

        # Connect buttons to the four CRUD operations.
        self.AddButton.clicked.connect(self.add_student)
        self.EditButton.clicked.connect(self.edit_student)
        self.DeleteButton.clicked.connect(self.delete_student)
        self.RefreshButton.clicked.connect(self.load_table)  # READ
        self.ClearButton.clicked.connect(self.clear_fields)

        self.load_table()  # Restore saved data as soon as the app opens.

    def read_form(self):
        """Get the five fields and perform simple input validation."""
        values = [
            self.NameEdit.text().strip(),
            self.RegEdit.text().strip(),
            self.gpaEdit.text().strip(),
            self.NumberEdit.text().strip(),
            self.uniEdit.text().strip(),
        ]
        if not all(values):
            QtWidgets.QMessageBox.warning(self, "Missing data", "Fill in all five fields.")
            return None

        try:
            gpa = float(values[2])
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Invalid GPA", "Enter a numeric GPA.")
            return None
        if not 0 <= gpa <= 4:
            QtWidgets.QMessageBox.warning(self, "Invalid GPA", "GPA must be between 0 and 4.")
            return None
        return values

    def save_records(self):
        """WRITE the current records to the CSV file after each change."""
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerows(self.records)

    def load_table(self):
        """READ CSV data from disk and show it in the table."""
        if not CSV_FILE.exists():
            CSV_FILE.touch()  # First run: create an empty CSV file.

        with CSV_FILE.open("r", newline="", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))

        # The supplied student.csv has no header and stores exactly five fields.
        self.records = [row for row in rows if len(row) == 5]
        self.selected_reg = None
        table = self.StuInfoTable
        table.blockSignals(True)
        table.clearSelection()
        table.setRowCount(len(self.records))
        for row_index, record in enumerate(self.records):
            for column_index, value in enumerate(record):
                table.setItem(
                    row_index,
                    column_index,
                    QtWidgets.QTableWidgetItem(value),
                )
        table.blockSignals(False)

    def fill_values(self):
        """When a user selects a record, place it into the editing fields."""
        row = self.StuInfoTable.currentRow()
        if row < 0 or row >= len(self.records):
            self.selected_reg = None
            return
        values = self.records[row]
        self.selected_reg = values[1]
        for widget, value in zip(
            [self.NameEdit, self.RegEdit, self.gpaEdit,
             self.NumberEdit, self.uniEdit],
            values,
        ):
            widget.setText(value)

    def clear_fields(self):
        """Clear the form and stop editing the previously selected record."""
        self.StuInfoTable.blockSignals(True)
        self.StuInfoTable.clearSelection()
        self.StuInfoTable.setCurrentCell(-1, -1)
        self.StuInfoTable.blockSignals(False)
        self.selected_reg = None
        for widget in [
            self.NameEdit, self.RegEdit, self.gpaEdit,
            self.NumberEdit, self.uniEdit,
        ]:
            widget.clear()

    def add_student(self):
        """CREATE a student record, rejecting duplicate registration numbers."""
        student = self.read_form()
        if student is None:
            return
        if any(row[1].lower() == student[1].lower() for row in self.records):
            QtWidgets.QMessageBox.warning(
                self, "Duplicate registration", "This registration number already exists."
            )
            return
        self.records.append(student)
        self.save_records()
        self.load_table()
        self.clear_fields()
        QtWidgets.QMessageBox.information(self, "Saved", "Student added successfully.")

    def edit_student(self):
        """UPDATE the selected record, even if the registration number changes."""
        if self.selected_reg is None:
            QtWidgets.QMessageBox.warning(self, "Select a student", "Select a row before editing.")
            return
        updated = self.read_form()
        if updated is None:
            return
        if any(
            row[1].lower() == updated[1].lower()
            and row[1].lower() != self.selected_reg.lower()
            for row in self.records
        ):
            QtWidgets.QMessageBox.warning(
                self, "Duplicate registration", "Another student has that registration number."
            )
            return
        for index, student in enumerate(self.records):
            if student[1] == self.selected_reg:
                self.records[index] = updated
                break
        self.save_records()
        self.load_table()
        self.clear_fields()
        QtWidgets.QMessageBox.information(self, "Saved", "Student updated successfully.")

    def delete_student(self):
        """DELETE the selected record after asking for confirmation."""
        if self.selected_reg is None:
            QtWidgets.QMessageBox.warning(self, "Select a student", "Select a row before deleting.")
            return
        answer = QtWidgets.QMessageBox.question(
            self, "Confirm deletion", "Delete the selected student?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if answer != QtWidgets.QMessageBox.Yes:
            return
        self.records = [
            row for row in self.records if row[1] != self.selected_reg
        ]
        self.save_records()
        self.load_table()
        self.clear_fields()
        QtWidgets.QMessageBox.information(self, "Deleted", "Student deleted successfully.")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = StudentCRUD()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

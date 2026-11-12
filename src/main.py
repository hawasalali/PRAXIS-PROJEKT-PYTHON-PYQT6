from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QTextCharFormat, QColor
import csv

def update_status():
    status.setText(f"Anzahl Einträge: {table.rowCount()}")

def add_entry():
    text = activity.text().strip()

    if not text:
        QMessageBox.warning(None, "Warnung", "Bitte Tätigkeit eingeben!")
        return

    row = table.rowCount()
    table.insertRow(row)

    data = [
        calendar.selectedDate().toString("dd.MM.yyyy"),
        combo.currentText(),
        text
    ]

    for col, value in enumerate(data):
        table.setItem(row, col, QTableWidgetItem(value))

    activity.clear()
    update_status()

def delete_entry():
    row = table.currentRow()

    if row < 0:
        QMessageBox.information(None, "Hinweis", "Bitte Zeile auswählen!")
        return

    if QMessageBox.question(
        None,
        "Löschen",
        "Eintrag wirklich löschen?"
    ) == QMessageBox.StandardButton.Yes:

        table.removeRow(row)
        update_status()

def save_csv():
    file, _ = QFileDialog.getSaveFileName(
        None, "CSV speichern", "", "CSV (*.csv)"
    )

    if not file:
        return

    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        writer.writerow(["Datum", "Kategorie", "Tätigkeit"])

        for row in range(table.rowCount()):
            writer.writerow(
                [table.item(row, col).text() for col in range(3)]
            )

    QMessageBox.information(None, "Info", "Datei gespeichert!")

def load_csv():
    file, _ = QFileDialog.getOpenFileName(
        None, "CSV laden", "", "CSV (*.csv)"
    )

    if not file:
        return

    table.setRowCount(0)

    with open(file, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)

        for data in reader:
            row = table.rowCount()
            table.insertRow(row)

            for col, value in enumerate(data):
                table.setItem(row, col, QTableWidgetItem(value))

    update_status()

def show_details(row, col):
    QMessageBox.information(
        None,
        "Details",
        f"Datum: {table.item(row,0).text()}\n"
        f"Kategorie: {table.item(row,1).text()}\n"
        f"Tätigkeit: {table.item(row,2).text()}"
    )

app = QApplication([])

window = QWidget()
window.resize(900, 600)
window.setWindowTitle("Azubi-Berichtsheft")

main_layout = QVBoxLayout()
input_layout = QHBoxLayout()
button_layout = QHBoxLayout()

activity = QLineEdit()
activity.setPlaceholderText("Was hast du heute gemacht?")

combo = QComboBox()
combo.addItems([
    "Programmierung",
    "Berufsschule",
    "Projektarbeit",
    "Support"
])

calendar = QCalendarWidget()

weekend = QTextCharFormat()
weekend.setBackground(QColor("#FFD6D6"))

date = QDate.currentDate().addYears(-1)
end = QDate.currentDate().addYears(1)

while date <= end:
    if date.dayOfWeek() in [6, 7]:
        calendar.setDateTextFormat(date, weekend)
    date = date.addDays(1)

btn_add = QPushButton("Eintrag hinzufügen")
btn_add.clicked.connect(add_entry)

table = QTableWidget(0, 3)
table.setHorizontalHeaderLabels(
    ["Datum", "Kategorie", "Tätigkeit"]
)
table.horizontalHeader().setSectionResizeMode(
    QHeaderView.ResizeMode.Stretch
)
table.setSelectionBehavior(
    QTableWidget.SelectionBehavior.SelectRows
)
table.cellDoubleClicked.connect(show_details)

btn_delete = QPushButton("Zeile löschen")
btn_delete.clicked.connect(delete_entry)

btn_save = QPushButton("CSV speichern")
btn_save.clicked.connect(save_csv)

btn_load = QPushButton("CSV laden")
btn_load.clicked.connect(load_csv)

status = QLabel("Anzahl Einträge: 0")

input_layout.addWidget(activity)
input_layout.addWidget(combo)
input_layout.addWidget(calendar)
input_layout.addWidget(btn_add)

button_layout.addWidget(btn_delete)
button_layout.addWidget(btn_save)
button_layout.addWidget(btn_load)
button_layout.addWidget(status)

main_layout.addLayout(input_layout)
main_layout.addWidget(table)
main_layout.addLayout(button_layout)

window.setLayout(main_layout)
window.show()

app.exec()
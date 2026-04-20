import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QRadioButton, QButtonGroup, QGroupBox, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from docx import Document
from docx.shared import Pt, RGBColor

from devices import Iron, Tv, Washer
from calculator import Calculator


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчет электроэнергии")
        self.setFixedSize(500, 520)

        self.last_result = None
        self.calc = Calculator(cost_per_kwh=6.0)
        self.devices = {
            "Iron": Iron(1200),
            "Tv": Tv(100),
            "Washer": Washer(2000)
        }

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Заголовок
        title = QLabel("Расчет потребления электроэнергии")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Выбор прибора
        group = QGroupBox("Выберите прибор:")
        group_layout = QVBoxLayout()
        self.btn_group = QButtonGroup()

        for i, (key, device) in enumerate(self.devices.items()):
            rb = QRadioButton(str(device))
            rb.setProperty("key", key)
            if i == 0:
                rb.setChecked(True)
            self.btn_group.addButton(rb)
            group_layout.addWidget(rb)

        group.setLayout(group_layout)
        layout.addWidget(group)

        # Поле: часы
        layout.addWidget(QLabel("Часы использования:"))
        self.hours_input = QLineEdit()
        layout.addWidget(self.hours_input)

        # Поле: цена
        layout.addWidget(QLabel("Цена за кВт·ч (руб.):"))
        self.price_input = QLineEdit("6.0")
        layout.addWidget(self.price_input)

        # Кнопки
        btn_layout = QHBoxLayout()
        calc_btn = QPushButton("Рассчитать")
        calc_btn.setStyleSheet("background-color: green; color: white; font-size: 12px;")
        calc_btn.clicked.connect(self.calculate)

        save_btn = QPushButton("Сохранить отчет")
        save_btn.setStyleSheet("background-color: blue; color: white; font-size: 12px;")
        save_btn.clicked.connect(self.save_report)

        btn_layout.addWidget(calc_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        # Результат
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

    def __str__(self):
        return f"App(devices={list(self.devices.keys())})"

    def __repr__(self):
        return f"App(calc={self.calc})"

    def get_selected_key(self):
        for btn in self.btn_group.buttons():
            if btn.isChecked():
                return btn.property("key")
        return "Iron"

    def calculate(self):
        try:
            hours = float(self.hours_input.text())
            price = float(self.price_input.text())

            if hours <= 0:
                raise ValueError("Часы должны быть больше 0")
            if price <= 0:
                raise ValueError("Цена должна быть больше 0")

            key = self.get_selected_key()
            device = self.devices[key]
            self.calc.cost_per_kwh = price

            energy = self.calc.calc_energy(device.power, hours)
            cost = self.calc.calc_cost(device.power, hours)

            self.last_result = {
                "device": str(device),
                "power": device.power,
                "hours": hours,
                "price": price,
                "energy": energy,
                "cost": cost,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            }

            text = f"Прибор: {device}\n"
            text += f"Мощность: {device.power} Вт\n"
            text += f"Время: {hours} ч\n\n"
            text += f"Потребление: {energy:.2f} кВт·ч\n"
            text += f"Цена за кВт·ч: {price} руб.\n"
            text += f"Итого: {cost:.2f} руб."

            self.result_box.setPlainText(text)

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def save_report(self):
        if not self.last_result:
            QMessageBox.warning(self, "Внимание", "Сначала выполните расчет!")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет",
            f"Отчет_{datetime.now().strftime('%d_%m_%Y')}.docx",
            "Word документы (*.docx)"
        )
        if not path:
            return

        try:
            doc = Document()

            title = doc.add_heading("ОТЧЕТ О РАСЧЕТЕ ЭЛЕКТРОЭНЕРГИИ", 0)
            title.alignment = 1

            doc.add_paragraph(f"Дата: {self.last_result['date']}").alignment = 1

            doc.add_heading("Информация о приборе", level=1)
            table = doc.add_table(rows=5, cols=2)
            table.style = "Light Grid Accent 1"

            table.rows[0].cells[0].text = "Прибор"
            table.rows[0].cells[1].text = self.last_result["device"]
            table.rows[1].cells[0].text = "Мощность"
            table.rows[1].cells[1].text = f"{self.last_result['power']} Вт"
            table.rows[2].cells[0].text = "Время использования"
            table.rows[2].cells[1].text = f"{self.last_result['hours']} ч"
            table.rows[3].cells[0].text = "Цена за кВт·ч"
            table.rows[3].cells[1].text = f"{self.last_result['price']} руб."
            table.rows[4].cells[0].text = "Потребление"
            table.rows[4].cells[1].text = f"{self.last_result['energy']:.2f} кВт·ч"

            doc.add_heading("Итого", level=1)
            p = doc.add_paragraph()
            run = p.add_run(f"{self.last_result['cost']:.2f} руб.")
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 0, 0)
            p.alignment = 1

            doc.save(path)
            QMessageBox.information(self, "Успех", f"Отчет сохранен:\n{path}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())

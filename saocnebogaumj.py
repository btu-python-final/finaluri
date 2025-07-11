from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QComboBox,
    QPushButton, QCheckBox, QRadioButton, QMessageBox, QLineEdit
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
import sqlite3
import os


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("იპოვე საშენო მანქანა")
        self.setGeometry(300, 100, 520, 950)
        self.setup_ui()
        self.setWindowIcon(QIcon("images/icon.png"))
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.gacnoba = QLabel('🔎 მიუთითე მანქანის მახასიათებლები:')
        layout.addWidget(self.gacnoba)

        self.tanxmoba = QCheckBox("მე ვეთანხმები წესებს")
        layout.addWidget(self.tanxmoba)

        layout.addWidget(QLabel("სქესი (ნებაყოფლობითი):"))
        self.kaci = QRadioButton("კაცი")
        self.qali = QRadioButton("ქალი")
        self.transformeri = QRadioButton("ტრანსფორმერი")
        layout.addWidget(self.kaci)
        layout.addWidget(self.qali)
        layout.addWidget(self.transformeri)

        layout.addWidget(QLabel("აირჩიე ქვეყანა:"))
        self.qveyana = QComboBox()
        self.qveyana.addItems(['გერმანია', 'იტალია', 'იაპონია'])
        layout.addWidget(self.qveyana)

        layout.addWidget(QLabel("აირჩიე ბიუჯეტი:"))
        self.biujeti = QComboBox()
        self.biujeti.addItems(['50k-100K$', '100K-500k$', '500K-2M$'])
        layout.addWidget(self.biujeti)

        layout.addWidget(QLabel("აირჩიე ცილინდრები:"))
        self.cilindrebi = QComboBox()
        self.cilindrebi.addItems(['6', '8', '10'])
        layout.addWidget(self.cilindrebi)

        self.dzieba_btn = QPushButton("🔍 მოძებნე შესაბამისი მანქანა")
        self.dzieba_btn.clicked.connect(self.dzebna)
        layout.addWidget(self.dzieba_btn)

        self.shedegi = QLabel("➡ თქვენთვის იდეალური მანქანა გამოჩნდება აქ")
        self.shedegi.setObjectName("ResultLabel")
        self.shedegi.setWordWrap(True)
        layout.addWidget(self.shedegi)

        self.image_label = QLabel()
        self.image_label.setObjectName("ImageBox")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(300, 200)
        self.image_label.setMaximumHeight(300)
        layout.addWidget(self.image_label)

        layout.addWidget(QLabel("➕ დაამატე მანქანა (ქვეყანა, ცილინდრი, ბიუჯეტი, მოდელი):"))
        self.new_car_input = QLineEdit()
        self.new_car_input.setPlaceholderText("მაგ: საფრანგეთი, 8, 50K-100K$, Peugeot 505")
        layout.addWidget(self.new_car_input)

        self.add_car_btn = QPushButton("➕ დაამატე მანქანა")
        self.add_car_btn.clicked.connect(self.damate_manqana)
        layout.addWidget(self.add_car_btn)

        layout.addWidget(QLabel("🔎 მოძებნე ან წაშალე მანქანა ID-ით:"))
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("მაგ: 5")
        layout.addWidget(self.id_input)

        self.id_search_btn = QPushButton("🔍 ძებნა ID-ით")
        self.id_search_btn.clicked.connect(self.dzebna_idit)
        layout.addWidget(self.id_search_btn)

        self.delete_btn = QPushButton("🗑️ წაშალე მანქანა ID-ით")
        self.delete_btn.clicked.connect(self.washla_idit)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f5fbff;
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
            }

            QLabel {
                color: #34495e;
                font-weight: 500;
            }

            QLineEdit, QComboBox {
                background-color: #ffffff;
                border: 1.5px solid #d0dce4;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 10px 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QPushButton:pressed {
                background-color: #2471a3;
            }

            QCheckBox, QRadioButton {
                padding: 6px;
            }

            #ImageBox {
                border: 2px solid #d6eaf8;
                border-radius: 12px;
                background-color: #ffffff;
                padding: 10px;
                margin-top: 10px;
            }

            #ResultLabel {
                background-color: #ecfaff;
                border: 1px solid #c5e4f3;
                padding: 10px;
                border-radius: 8px;
                color: #1a5276;
                font-size: 15px;
            }
        """)

    def dzebna(self):
        if not self.tanxmoba.isChecked():
            QMessageBox.warning(self, 'ნუ ცანცარებ', "ჯერ დაეთანხმე წესებს")
            return

        if self.transformeri.isChecked():
            QMessageBox.warning(self, "შორს ლიბერასტები", "ან კაცი აირჩიე ან ქალი, ნუ გარყვნი პროგრამას!")
            return

        qveyana = self.qveyana.currentText()
        biujeti = self.biujeti.currentText()
        cilindrebi = self.cilindrebi.currentText()

        try:
            conn = sqlite3.connect("cars.sqlite")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT model FROM cars
                WHERE country = ? AND cylinders = ? AND price_range = ?
            ''', (qveyana, cilindrebi, biujeti))
            result = cursor.fetchone()
            conn.close()

            if result:
                manqana = result[0]
                self.shedegi.setText(f"✅ თქვენთვის იდეალური მანქანა არის: {manqana}")
                self.load_car_image(manqana)
            else:
                self.shedegi.setText("❌ ვერ მოიძებნა შესაბამისი მანქანა")
                self.image_label.clear()

        except Exception as e:
            QMessageBox.critical(self, "შეცდომა", str(e))

    def load_car_image(self, model):
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
        for ext in extensions:
            img_path = f"images/{model}{ext}"
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path).scaled(
                    self.image_label.width(),
                    self.image_label.height(),
                    Qt.KeepAspectRatio
                )
                self.image_label.setPixmap(pixmap)
                return
        self.image_label.setText("📷 სურათი არ მოიძებნა")

    def damate_manqana(self):
        user_input = self.new_car_input.text().strip()
        try:
            country, cylinders, price_range, model = [x.strip() for x in user_input.split(",")]
        except ValueError:
            QMessageBox.warning(self, "ნუ ცანცარებ", "ფორმატი: ქვეყანა, ცილინდრი, ბიუჯეტი, მოდელი")
            return

        if not (country and cylinders and price_range and model):
            QMessageBox.warning(self, "ცარიელი ველი", "ყველა ველი უნდა იყოს შევსებული!")
            return

        try:
            conn = sqlite3.connect("cars.sqlite")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO cars (country, cylinders, price_range, model)
                VALUES (?, ?, ?, ?)
            ''', (country, cylinders, price_range, model))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "წარმატება", f"მანქანა '{model}' დაემატა.")
            self.new_car_input.clear()

            if country not in [self.qveyana.itemText(i) for i in range(self.qveyana.count())]:
                self.qveyana.addItem(country)
            if cylinders not in [self.cilindrebi.itemText(i) for i in range(self.cilindrebi.count())]:
                self.cilindrebi.addItem(cylinders)
            if price_range not in [self.biujeti.itemText(i) for i in range(self.biujeti.count())]:
                self.biujeti.addItem(price_range)

        except Exception as e:
            QMessageBox.critical(self, "ბაზის შეცდომა", f"შეცდომა:\n{e}")

    def dzebna_idit(self):
        car_id = self.id_input.text().strip()
        if not car_id.isdigit():
            QMessageBox.warning(self, "შეცდომა", "ID უნდა იყოს რიცხვი!")
            return

        try:
            conn = sqlite3.connect("cars.sqlite")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT country, cylinders, price_range, model
                FROM cars
                WHERE id = ?
            ''', (car_id,))
            result = cursor.fetchone()
            conn.close()

            if result:
                country, cylinders, price_range, model = result
                QMessageBox.information(
                    self, "მანქანა მოიძებნა",
                    f"ქვეყანა: {country}\nცილინდრი: {cylinders}\nბიუჯეტი: {price_range}\nმოდელი: {model}"
                )
            else:
                QMessageBox.information(self, "ვერ მოიძებნა", "ამ ID-ით მანქანა არ არსებობს.")

        except Exception as e:
            QMessageBox.critical(self, "ბაზის შეცდომა", f"შეცდომა:\n{e}")

    def washla_idit(self):
        car_id = self.id_input.text().strip()
        if not car_id.isdigit():
            QMessageBox.warning(self, "შეცდომა", "ID უნდა იყოს რიცხვი!")
            return

        try:
            conn = sqlite3.connect("cars.sqlite")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
            conn.commit()

            if cursor.rowcount:
                QMessageBox.information(self, "წარმატება", "მანქანა წაიშალა.")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cars_temp (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        country TEXT,
                        cylinders TEXT,
                        price_range TEXT,
                        model TEXT
                    )
                """)
                cursor.execute("""
                    INSERT INTO cars_temp (country, cylinders, price_range, model)
                    SELECT country, cylinders, price_range, model FROM cars
                """)
                cursor.execute("DROP TABLE cars")
                cursor.execute("ALTER TABLE cars_temp RENAME TO cars")
                conn.commit()
            else:
                QMessageBox.information(self, "შედეგი", "ასეთი ID არ არსებობს.")

            self.id_input.clear()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "ბაზის შეცდომა", f"შეცდომა:\n{e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

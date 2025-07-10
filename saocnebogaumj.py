from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QComboBox,
    QPushButton, QCheckBox, QRadioButton, QMessageBox, QLineEdit
)
import sys
import sqlite3

class MyWindow(QWidget):

    def dzebna(self):
        if not self.tanxmoba.isChecked():
            QMessageBox.warning(self, 'ნუ ცანცარებ', "ჯერ დაეთანხმე წესებს")
            return

        qveyana = self.qveyana.currentText()
        biujeti = self.biujeti.currentText()
        cilindrebi = self.cilindrebi.currentText()

        if self.transformeri.isChecked():
            QMessageBox.warning(self, "შორს ლიბერასტები", "ეგეც შენი ამერიკა და ევროპა! ან კაცი აირჩიე ან ქალი, ნუ გარყვენით ჩემი PyQt5-ის პროგრამა, დატოვეთ რამე წმინდა!")
            return

        try:
            conn = sqlite3.connect("cars.sqlite")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT model FROM cars
                WHERE country = ? AND cylinders = ? AND price_range = ?
            ''', (qveyana, cilindrebi, biujeti))

            result = cursor.fetchone()
            if result:
                manqana = result[0]
            else:
                manqana = "ვერ მოიძებნა შესაბამისი მანქანა"

            self.shedegi.setText(f"თქვენთვის იდეალური მანქანა არის: {manqana}")

        finally:
            conn.close()

    def damate_manqana(self):
        user_input = self.new_car_input.text().strip()
        try:
            country, cylinders, price_range, model = [x.strip() for x in user_input.split(",")]
        except ValueError:
            QMessageBox.warning(self, "ნუ ცანცარებ", "შეიყვანე მონაცემები ამ მიმდევრობით:\nქვეყანა, ცილინდრი, ბიუჯეტი, მოდელი")
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
            QMessageBox.information(self, "წარმატება", f"მანქანა '{model}' წარმატებით დაემატა ბაზაში.")
            self.new_car_input.clear()

            if country not in [self.qveyana.itemText(i) for i in range(self.qveyana.count())]:
                self.qveyana.addItem(country)
            if cylinders not in [self.cilindrebi.itemText(i) for i in range(self.cilindrebi.count())]:
                self.cilindrebi.addItem(cylinders)
            if price_range not in [self.biujeti.itemText(i) for i in range(self.biujeti.count())]:
                self.biujeti.addItem(price_range)

        except Exception as e:
            QMessageBox.critical(self, "ბაზის შეცდომა", f"შეცდომა მოხდა მანქანის დამატებისას:\n{e}")

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
            QMessageBox.critical(self, "ბაზის შეცდომა", f"შეცდომა მოხდა ID-ის ძებნისას:\n{e}")

    def washla_idit(self):
        car_id = self.id_input.text().strip()

        if not car_id.isdigit():
            QMessageBox.warning(self, "შეცდომა", "ID უნდა იყოს რიცხვი!")
            return

        try:
            conn = sqlite3.connect("cars.sqlite")
            cursor = conn.cursor()

            # 1. წაშლა
            cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
            conn.commit()

            if cursor.rowcount:
                QMessageBox.information(self, "წარმატება", "მანქანა წაიშალა.")

                # 2. ID-ების გადათვლა
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
            QMessageBox.critical(self, "ბაზის შეცდომა", f"შეცდომა მოხდა წაშლისას:\n{e}")

    def __init__(self):
        super().__init__()
        self.setWindowTitle('იპოვე საშენო მანქანა')
        self.setGeometry(400, 200, 400, 850)

        self.gacnoba = QLabel('ეროვნების, ცილინდრების რაოდენობის და ბიუჯეტის არჩევის შემდეგ, \nჩვენ გეტყვით თუ რომელია შენთვის საუკეთესო მანქანა')
        self.tanxmoba = QCheckBox("მე ვეთანხმები წესებს")
        self.sqesi = QLabel("აირჩიე სქესი (ნებაყოფლობითი):")
        self.kaci = QRadioButton("კაცი")
        self.qali = QRadioButton("ქალი")
        self.transformeri = QRadioButton("ტრანსფორმერი")

        self.qveyana = QComboBox()
        self.qveyana.addItems(['გერმანია', 'იტალია', 'იაპონია'])

        self.biujeti = QComboBox()
        self.biujeti.addItems(['50k-100K$', '100K-500k$', '500K-2M$'])

        self.cilindrebi = QComboBox()
        self.cilindrebi.addItems(['6', '8', '10'])

        self.shedegi = QLabel("თქვენთვის იდეალური მანქანა არის:")
        self.dzieba_btn = QPushButton('მოძებნე შესაბამისი მანქანა')
        self.dzieba_btn.clicked.connect(self.dzebna)

        self.new_car_input = QLineEdit()
        self.new_car_input.setPlaceholderText("მაგ: საფრანგეთი, 8, 50-100K$, Peugeot 505")

        self.add_car_btn = QPushButton("დაამატე მანქანა")
        self.add_car_btn.clicked.connect(self.damate_manqana)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("შეიყვანე ID (მაგ: 5)")

        self.id_search_btn = QPushButton("ძებნა ID-ით")
        self.id_search_btn.clicked.connect(self.dzebna_idit)

        self.delete_btn = QPushButton("წაშალე მანქანა ID-ით")
        self.delete_btn.clicked.connect(self.washla_idit)

        layout = QVBoxLayout()
        layout.addWidget(self.gacnoba)
        layout.addWidget(self.tanxmoba)
        layout.addWidget(self.sqesi)
        layout.addWidget(self.kaci)
        layout.addWidget(self.qali)
        layout.addWidget(self.transformeri)
        layout.addWidget(QLabel("აირჩიე ქვეყანა:"))
        layout.addWidget(self.qveyana)
        layout.addWidget(QLabel("აირჩიე ბიუჯეტი:"))
        layout.addWidget(self.biujeti)
        layout.addWidget(QLabel("აირჩიე ცილინდრების რაოდენობა:"))
        layout.addWidget(self.cilindrebi)
        layout.addWidget(self.dzieba_btn)
        layout.addWidget(self.shedegi)

        layout.addWidget(QLabel("დაამატე ახალი მანქანა ბაზაში შემდეგი ფორმატით: ქვეყანა, ც.რ, ფასი, სახელი:"))
        layout.addWidget(self.new_car_input)
        layout.addWidget(self.add_car_btn)

        layout.addWidget(QLabel("იპოვე მანქანა ID-ით:"))
        layout.addWidget(self.id_input)
        layout.addWidget(self.id_search_btn)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())

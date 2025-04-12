from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QMainWindow, QDialog, QFormLayout, QLineEdit, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QComboBox, QDateEdit, QTextEdit, QToolBar, QMessageBox
from models import *
from PySide6.QtGui import QAction,QIcon
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtCore import QDate  
from styles import get_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Обращения граждан")
        self.setGeometry(200, 200, 830, 500)
        self.setWindowIcon(QIcon("ic.PNG"))
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        search_layout = QHBoxLayout()
        search = QLabel("Поиск")
        self.search_input = QLineEdit()
        search_btn = QPushButton("Найти")
        search_btn.clicked.connect(self.search)
        add_applicant_btn = QPushButton("Добавить Заявителя")
        add_applicant_btn.clicked.connect(self.add_applicant)
        add_appeal_btn = QPushButton("Добавить обращение")
        add_appeal_btn.clicked.connect(self.add_appeal)
        delete_appeal_btn = QPushButton("Удалить обращение")
        delete_appeal_btn.clicked.connect(self.delete_appeal)
        search_layout.addWidget(add_appeal_btn)
        search_layout.addWidget(add_applicant_btn)
        search_layout.addWidget(search)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(delete_appeal_btn)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Рег номер", "Заявитель", "Ответственный", "Дата регистрации", "Дата ответа", "Категория обращения", "Статус", "Результат"])
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked) 
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        self.load_data()

    def on_cell_double_clicked(self, row, column):
        session = Session()
        reg_number = self.table.item(row, 0).text()
        appeal = session.query(Appeal).filter_by(reg_number=reg_number).first()

        if column == 1:  
            applicant = appeal.applicant
            dialog = DialogApplicant(self, applicant)
            if dialog.exec():
                self.load_data()  
        elif appeal:  
            dialog = DialogAppeal(self, appeal)
            if dialog.exec():
                self.load_data()  
        session.close()

    def add_applicant(self):
        dialog = DialogApplicant(self)
        if dialog.exec():
            self.load_data()  

    def add_appeal(self):
        dialog = DialogAppeal(self)
        if dialog.exec():
            self.load_data()

    def load_data(self, appeals=None):
        session = Session()
        if appeals is None:
            appeals = session.query(Appeal).all()
        self.table.setRowCount(0)
        for row, appeal in enumerate(appeals):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(appeal.reg_number))
            self.table.setItem(row, 1, QTableWidgetItem(appeal.applicant.full_name))
            self.table.setItem(row, 2, QTableWidgetItem(appeal.employee.full_name))
            self.table.setItem(row, 3, QTableWidgetItem(str(appeal.registration_date)))
            answer_date = str(appeal.answer_date) if appeal.answer_date else ""
            self.table.setItem(row, 4, QTableWidgetItem(answer_date))
            self.table.setItem(row, 5, QTableWidgetItem(appeal.category.title))
            self.table.setItem(row, 6, QTableWidgetItem(appeal.status.title))
            self.table.setItem(row, 7, QTableWidgetItem(appeal.result.title))
        session.close()

    def search(self):
        search_text = self.search_input.text().lower()
        session = Session()
        if search_text:
            filtered = session.query(Appeal).join(Employee).join(Applicant).filter(
                (Employee.full_name.ilike(f"%{search_text}%")) |
                (Applicant.full_name.ilike(f"%{search_text}%"))
            ).all()
        else:
            filtered = session.query(Appeal).all()
        self.load_data(filtered)
        session.close()

    def delete_appeal(self):
        selected = self.table.currentRow()
        if selected >= 0:
            reg_number = self.table.item(selected, 0).text()
            reply = QMessageBox.question(
                self, 
                "Подтверждение удаления", 
                f"Вы уверены, что хотите удалить обращение с номером {reg_number}?",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                session = Session()
                appeal = session.query(Appeal).filter_by(reg_number=reg_number).first()
                if appeal:
                    session.delete(appeal)
                    session.commit()
                session.close()
                self.load_data()

class DialogAddWorkPlace(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление места работы")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название организации")
        save_btn = QPushButton("Сохранить")
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self.save_work_place)  
        layout.addWidget(QLabel("Название места работы:"))
        layout.addWidget(self.title_input)
        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)
        self.setLayout(layout)

    def save_work_place(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Ошибка", "Название организации не может быть пустым!")
            return
        session = Session()
        try:
            new_work_place = Place_work(title=title)
            session.add(new_work_place)
            session.commit()
            self.accept()  
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить место работы: {str(e)}")
        finally:
            session.close()

class DialogAddAddress(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление адреса")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Адрес")
        save_btn = QPushButton("Сохранить")
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self.save_address)  
        layout.addWidget(QLabel("Адрес:"))
        layout.addWidget(self.title_input)
        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)
        self.setLayout(layout)

    def save_address(self):
        address = self.title_input.text().strip()
        if not address:
            QMessageBox.warning(self, "Ошибка", "Адрес не может быть пустым!")
            return
        session = Session()
        try:
            new_address = Address(address=address)
            session.add(new_address)
            session.commit()
            self.accept() 
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить адрес: {str(e)}")
        finally:
            session.close()

class DialogApplicant(QDialog):
    def __init__(self, parent=None, applicant=None):
        super().__init__(parent)  
        self.setWindowTitle("Редактирование заявителя" if applicant else "Добавление заявителя")
        self.resize(400, 300)
        self.applicant = applicant
        self.parent_window = parent  
        main_layout = QVBoxLayout()
        toolbar = QToolBar(self)
        add_work_place = QAction("Добавить место работы", self)
        add_work_place.triggered.connect(self.open_add_work_place)
        add_address = QAction("Добавить адрес", self)
        add_address.triggered.connect(self.open_add_address)
        toolbar.addAction(add_work_place)
        toolbar.addAction(add_address)
        main_layout.addWidget(toolbar)
        layout = QFormLayout()
        self.full_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        session = Session()
        self.place_work_combo = QComboBox()
        places = session.query(Place_work).all()
        for place in places:
            self.place_work_combo.addItem(place.title, place.id)
        self.address_combo = QComboBox()
        addresses = session.query(Address).all()
        for address in addresses:
            self.address_combo.addItem(address.address, address.id)
        if self.applicant:
            self.full_name_input.setText(self.applicant.full_name)
            self.phone_input.setText(self.applicant.phone)
            self.email_input.setText(self.applicant.email)
            self.place_work_combo.setCurrentIndex(self.place_work_combo.findData(self.applicant.place_work_id))
            self.address_combo.setCurrentIndex(self.address_combo.findData(self.applicant.address_id))
        layout.addRow("ФИО:", self.full_name_input)
        layout.addRow("Телефон:", self.phone_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Место работы:", self.place_work_combo)
        layout.addRow("Адрес проживания:", self.address_combo)
        save_btn = QPushButton("Сохранить")
        cancel_btn = QPushButton("Отмена")
        save_btn.clicked.connect(self.save_applicant)
        cancel_btn.clicked.connect(self.reject)
        main_layout.addLayout(layout)
        main_layout.addWidget(save_btn)
        main_layout.addWidget(cancel_btn)
        self.setLayout(main_layout)
        session.close()

    def save_applicant(self):
        full_name = self.full_name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        place_id = self.place_work_combo.currentData()
        address_id = self.address_combo.currentData()

        if not full_name or not phone or not email or place_id is None or address_id is None:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        session = Session()
        try:
            if self.applicant:  
                self.applicant = session.merge(self.applicant)
                self.applicant.full_name = full_name
                self.applicant.phone = phone
                self.applicant.email = email
                self.applicant.place_work_id = place_id
                self.applicant.address_id = address_id
                message = "Заявитель обновлен!"
            else:  
                new_applicant = Applicant(
                    full_name=full_name,
                    phone=phone,
                    email=email,
                    place_work_id=place_id,
                    address_id=address_id
                )
                session.add(new_applicant)
                message = "Заявитель добавлен!"

            session.commit()
            QMessageBox.information(self, "Успех", message)
            if self.parent_window:
                self.parent_window.load_data()  
            self.accept()
        except SQLAlchemyError as e:
            session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {str(e)}")
        finally:
            session.close()

    def open_add_work_place(self):
        dialog = DialogAddWorkPlace(self)
        if dialog.exec():
            session = Session()
            try:
                new_work_place = Place_work(title=dialog.title_input.text())
                session.add(new_work_place)
                session.commit()
                self.place_work_combo.clear()
                places = session.query(Place_work).all()
                for place in places:
                    self.place_work_combo.addItem(place.title, place.id)
                self.place_work_combo.setCurrentIndex(self.place_work_combo.findData(new_work_place.id))
            except Exception as e:
                session.rollback()
                print(f"Ошибка при добавлении места работы: {e}")
            finally:
                session.close()

    def open_add_address(self):
        dialog = DialogAddAddress(self)
        if dialog.exec():
            session = Session()
            try:
                new_address = Address(address=dialog.title_input.text())
                session.add(new_address)
                session.commit()
                self.address_combo.clear()
                addresses = session.query(Address).all()
                for address in addresses:
                    self.address_combo.addItem(address.address, address.id)
                self.address_combo.setCurrentIndex(self.address_combo.findData(new_address.id))
            except Exception as e:
                session.rollback()
                print(f"Ошибка при добавлении адреса: {e}")
            finally:
                session.close()

class DialogAppeal(QDialog):
    def __init__(self, parent=None, appeal=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление обращения")
        layout = QFormLayout()
        self.appeal = appeal
        self.parent_window = parent
        self.reg_number_input = QLineEdit()
        self.applicant_combo = QComboBox()
        session = Session()
        applicants = session.query(Applicant).all()
        for applicant in applicants:
            self.applicant_combo.addItem(applicant.full_name, applicant.id)
        self.employee_combo = QComboBox()
        employees = session.query(Employee).all()
        for employee in employees:
            display_text = f"{employee.full_name} ({employee.post.title})" if employee.post else employee.full_name
            self.employee_combo.addItem(display_text, employee.id)
        self.description_input = QTextEdit()
        self.registration_date = QDateEdit()
        self.registration_date.setCalendarPopup(True)
        self.registration_date.setDate(QDate.currentDate())
        self.answer_date = QDateEdit()
        self.answer_date.setCalendarPopup(True)
        self.answer_date.setSpecialValueText("Не указано")
        self.answer_date.setMinimumDate(QDate(1900, 1, 1))
        self.answer_date.setDate(QDate(1900, 1, 1))
        self.answer_date.setDisplayFormat("dd-MM-yyyy")
        self.category_combo = QComboBox()
        categories = session.query(Category).all()
        for category in categories:
            self.category_combo.addItem(category.title, category.id)
        self.status_combo = QComboBox()
        statuses = session.query(Status).all()
        for status in statuses:
            self.status_combo.addItem(status.title, status.id)
        self.result_combo = QComboBox()
        results = session.query(Answer).all()
        for result in results:
            self.result_combo.addItem(result.title, result.id)
        if self.appeal:
            self.reg_number_input.setText(self.appeal.reg_number)
            self.applicant_combo.setCurrentIndex(self.applicant_combo.findData(self.appeal.applicant_id))
            self.employee_combo.setCurrentIndex(self.employee_combo.findData(self.appeal.employee_id))
            self.description_input.setText(self.appeal.description)
            self.registration_date.setDate(QDate(self.appeal.registration_date.year,
                                                self.appeal.registration_date.month,
                                                self.appeal.registration_date.day))
            if self.appeal.answer_date:
                self.answer_date.setDate(QDate(self.appeal.answer_date.year,
                                              self.appeal.answer_date.month,
                                              self.appeal.answer_date.day))
            else:
                self.answer_date.setDate(QDate(1900, 1, 1))
        layout.addRow("Рег. номер:", self.reg_number_input)
        layout.addRow("Заявитель:", self.applicant_combo)
        layout.addRow("Ответственный:", self.employee_combo)
        layout.addRow("Описание:", self.description_input)
        layout.addRow("Дата регистрации:", self.registration_date)
        layout.addRow("Дата ответа:", self.answer_date)
        layout.addRow("Категория:", self.category_combo)
        layout.addRow("Статус:", self.status_combo)
        layout.addRow("Результат:", self.result_combo)
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save_appeal)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        layout.addRow(save_btn, cancel_btn)
        self.setLayout(layout)
        session.close()

    def save_appeal(self):
        session = Session()
        try:
            if not self.reg_number_input.text().strip():
                raise ValueError("Регистрационный номер обязателен!")
            if not self.description_input.toPlainText().strip():
                raise ValueError("Описание обязательно!")
            answer_date = None
            selected_date = self.answer_date.date()
            if selected_date != QDate(1900, 1, 1):
                answer_date = selected_date.toPython()
            if self.appeal:
                self.appeal = session.merge(self.appeal)
                self.appeal.reg_number = self.reg_number_input.text().strip()
                self.appeal.applicant_id = self.applicant_combo.currentData()
                self.appeal.employee_id = self.employee_combo.currentData()
                self.appeal.description = self.description_input.toPlainText().strip()
                self.appeal.registration_date = self.registration_date.date().toPython()
                self.appeal.answer_date = answer_date
                self.appeal.category_id = self.category_combo.currentData()
                self.appeal.status_id = self.status_combo.currentData()
                self.appeal.result_id = self.result_combo.currentData()
            else:
                new_appeal = Appeal(
                    reg_number=self.reg_number_input.text().strip(),
                    applicant_id=self.applicant_combo.currentData(),
                    employee_id=self.employee_combo.currentData(),
                    description=self.description_input.toPlainText().strip(),
                    registration_date=self.registration_date.date().toPython(),
                    answer_date=answer_date,
                    category_id=self.category_combo.currentData(),
                    status_id=self.status_combo.currentData(),
                    result_id=self.result_combo.currentData()
                )
                session.add(new_appeal)
            session.commit()
            QMessageBox.information(self, "Успех", "Обращение сохранено!")
            if self.parent_window:
                self.parent_window.load_data()
            self.accept()
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))
        except SQLAlchemyError as e:
            session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {str(e)}")
        finally:
            session.close()

app = QApplication([])
app.setStyleSheet(get_stylesheet())
window = MainWindow()
window.show()
app.exec()
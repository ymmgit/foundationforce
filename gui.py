import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QComboBox, QStackedWidget)
from PyQt5.QtCore import Qt
from main import CraneDatabase, MastDatabase

import sys
import traceback

def exception_hook(exctype, value, tb):
    print(''.join(traceback.format_exception(exctype, value, tb)))
    sys.exit(1)

sys.excepthook = exception_hook

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crane and Mast Database Manager")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.main_menu = self.create_main_menu()
        self.crane_window = CraneWindow(self)
        self.mast_window = MastWindow(self)

        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.crane_window)
        self.central_widget.addWidget(self.mast_window)

    def create_main_menu(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.crane_btn = QPushButton("Manage Crane Data")
        self.mast_btn = QPushButton("Manage Mast Data")
        self.exit_btn = QPushButton("Exit")

        layout.addWidget(self.crane_btn)
        layout.addWidget(self.mast_btn)
        layout.addWidget(self.exit_btn)

        self.crane_btn.clicked.connect(self.open_crane_window)
        self.mast_btn.clicked.connect(self.open_mast_window)
        self.exit_btn.clicked.connect(self.close)

        return widget

    def open_crane_window(self):
        self.central_widget.setCurrentWidget(self.crane_window)

    def open_mast_window(self):
        self.central_widget.setCurrentWidget(self.mast_window)

    def back_to_main(self):
        self.central_widget.setCurrentWidget(self.main_menu)

class CraneWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Crane Database Manager")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Enter crane model name")
        self.layout.addWidget(self.model_input)

        self.create_btn = QPushButton("Create New Database")
        self.add_btn = QPushButton("Add/Update Data")
        self.retrieve_btn = QPushButton("Retrieve Data")
        self.delete_btn = QPushButton("Delete Database")
        self.back_btn = QPushButton("Back to Main Menu")

        self.layout.addWidget(self.create_btn)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.retrieve_btn)
        self.layout.addWidget(self.delete_btn)
        self.layout.addWidget(self.back_btn)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

        self.create_btn.clicked.connect(self.create_database)
        self.add_btn.clicked.connect(self.add_data)
        self.retrieve_btn.clicked.connect(self.retrieve_data)
        self.delete_btn.clicked.connect(self.delete_database)
        self.back_btn.clicked.connect(self.main_window.back_to_main)

        # Create stacked widget for different operations
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Create and add widgets for different operations
        self.add_data_widget = CraneDataInputWidget(self)
        self.retrieve_data_widget = CraneRetrieveWidget(self)

        self.stacked_widget.addWidget(self.add_data_widget)
        self.stacked_widget.addWidget(self.retrieve_data_widget)

        # Initially hide the stacked widget
        self.stacked_widget.hide()

    def create_database(self):
        model_name = self.model_input.text()
        if model_name:
            CraneDatabase(model_name)
            self.result_text.setText(f"Database for {model_name} created successfully.")
        else:
            self.result_text.setText("Please enter a model name.")

    def add_data(self):
        model_name = self.model_input.text()
        if model_name:
            self.add_data_widget.set_model_name(model_name)
            self.stacked_widget.setCurrentWidget(self.add_data_widget)
            self.stacked_widget.show()
            self.hide_main_buttons()
        else:
            self.result_text.setText("Please enter a model name.")

    def retrieve_data(self):
        model_name = self.model_input.text()
        if model_name:
            self.retrieve_data_widget.set_model_name(model_name)
            self.stacked_widget.setCurrentWidget(self.retrieve_data_widget)
            self.stacked_widget.show()
            self.hide_main_buttons()
        else:
            self.result_text.setText("Please enter a model name.")

    def delete_database(self):
        model_name = self.model_input.text()
        if model_name:
            db_name = f"CraneData/{model_name.lower().replace(' ', '_')}_crane.db"
            if os.path.exists(db_name):
                os.remove(db_name)
                self.result_text.setText(f"Database for {model_name} deleted successfully.")
            else:
                self.result_text.setText(f"Database for {model_name} not found.")
        else:
            self.result_text.setText("Please enter a model name.")

    def hide_main_buttons(self):
        self.model_input.hide()
        self.create_btn.hide()
        self.add_btn.hide()
        self.retrieve_btn.hide()
        self.delete_btn.hide()
        self.back_btn.hide()
        self.result_text.hide()

    def show_main_buttons(self):
        self.model_input.show()
        self.create_btn.show()
        self.add_btn.show()
        self.retrieve_btn.show()
        self.delete_btn.show()
        self.back_btn.show()
        self.result_text.show()
        self.stacked_widget.hide()

class CraneDataInputWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.inputs = {}
        fields = ["jib_length", "in_service_moment", "in_service_vertical_force", "in_service_horizontal_force",
                  "out_of_service_moment", "out_of_service_vertical_force", "out_of_service_horizontal_force",
                  "number_of_falls", "tip_load", "max_load_radius", "wind_area", "delta_h"]

        for field in fields:
            self.inputs[field] = QLineEdit()
            self.inputs[field].setPlaceholderText(field.replace("_", " ").title())
            layout.addWidget(self.inputs[field])

        self.submit_btn = QPushButton("Submit")
        layout.addWidget(self.submit_btn)
        self.submit_btn.clicked.connect(self.submit_data)

        self.back_btn = QPushButton("Back")
        layout.addWidget(self.back_btn)
        self.back_btn.clicked.connect(self.go_back)

    def set_model_name(self, model_name):
        self.model_name = model_name

    def submit_data(self):
        try:
            db = CraneDatabase(self.model_name)
            data = [float(self.inputs[field].text()) for field in self.inputs]
            db.add_data(*data)
            db.close()
            self.parent.result_text.setText("Data added successfully.")
            self.go_back()
            # Clear the input fields after successful submission
            for input_field in self.inputs.values():
                input_field.clear()
        except ValueError:
            self.parent.result_text.setText("Please enter valid numeric values for all fields.")

    def go_back(self):
        self.parent.show_main_buttons()

class CraneRetrieveWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.jib_length_input = QLineEdit()
        self.jib_length_input.setPlaceholderText("Enter jib length")
        layout.addWidget(self.jib_length_input)

        self.retrieve_btn = QPushButton("Retrieve")
        layout.addWidget(self.retrieve_btn)
        self.retrieve_btn.clicked.connect(self.retrieve_data)

    def set_model_name(self, model_name):
        self.model_name = model_name

    def retrieve_data(self):
        try:
            jib_length = float(self.jib_length_input.text())
            db = CraneDatabase(self.model_name)
            data = db.get_data(jib_length)
            db.close()

            if data:
                result = "\n".join([f"{field}: {value}" for field, value in zip(
                    ["Jib length", "In-service moment", "In-service vertical force", "In-service horizontal force",
                     "Out-of-service moment", "Out-of-service vertical force", "Out-of-service horizontal force",
                     "Number of falls", "Tip load", "Max load radius", "Wind area", "Delta_h"],
                    data
                )])
                self.parent.result_text.setText(result)
            else:
                self.parent.result_text.setText("No data found for the given jib length.")
            self.parent.stacked_widget.hide()
            self.parent.show_main_buttons()
        except ValueError:
            self.parent.result_text.setText("Please enter a valid numeric value for jib length.")

class MastWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Mast Database Manager")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.add_btn = QPushButton("Add/Update Mast Data")
        self.retrieve_btn = QPushButton("Retrieve Mast Data")
        self.back_btn = QPushButton("Back to Main Menu")

        layout.addWidget(self.add_btn)
        layout.addWidget(self.retrieve_btn)
        layout.addWidget(self.back_btn)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.add_btn.clicked.connect(self.add_data)
        self.retrieve_btn.clicked.connect(self.retrieve_data)
        self.back_btn.clicked.connect(self.main_window.back_to_main)

        # Create stacked widget for different operations
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create and add widgets for different operations
        self.add_data_widget = MastDataInputWidget(self)
        self.retrieve_data_widget = MastRetrieveWidget(self)

        self.stacked_widget.addWidget(self.add_data_widget)
        self.stacked_widget.addWidget(self.retrieve_data_widget)

        # Initially hide the stacked widget
        self.stacked_widget.hide()

    def add_data(self):
        self.stacked_widget.setCurrentWidget(self.add_data_widget)
        self.stacked_widget.show()
        self.hide_main_buttons()

    def retrieve_data(self):
        self.stacked_widget.setCurrentWidget(self.retrieve_data_widget)
        self.stacked_widget.show()
        self.hide_main_buttons()

    def hide_main_buttons(self):
        self.add_btn.hide()
        self.retrieve_btn.hide()
        self.back_btn.hide()
        self.result_text.hide()

    def show_main_buttons(self):
        self.add_btn.show()
        self.retrieve_btn.show()
        self.back_btn.show()
        self.result_text.show()
        self.stacked_widget.hide()

class MastDataInputWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.inputs = {}
        fields = ["mast_model", "self_weight", "mast_height", "mast_wind_area"]

        for field in fields:
            self.inputs[field] = QLineEdit()
            self.inputs[field].setPlaceholderText(field.replace("_", " ").title())
            layout.addWidget(self.inputs[field])

        self.submit_btn = QPushButton("Submit")
        layout.addWidget(self.submit_btn)
        self.submit_btn.clicked.connect(self.submit_data)

        self.back_btn = QPushButton("Back")
        layout.addWidget(self.back_btn)
        self.back_btn.clicked.connect(self.go_back)

    def submit_data(self):
        try:
            db = MastDatabase()
            mast_model = self.inputs["mast_model"].text()
            data = [float(self.inputs[field].text()) for field in ["self_weight", "mast_height", "mast_wind_area"]]
            db.add_data(mast_model, *data)
            db.close()
            self.parent.result_text.setText("Mast data added/updated successfully.")
            self.go_back()
            # Clear the input fields after successful submission
            for input_field in self.inputs.values():
                input_field.clear()
        except ValueError:
            self.parent.result_text.setText("Please enter valid numeric values for all fields except mast model.")

    def go_back(self):
        self.parent.show_main_buttons()

class MastRetrieveWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.mast_model_input = QLineEdit()
        self.mast_model_input.setPlaceholderText("Enter mast model")
        layout.addWidget(self.mast_model_input)

        self.retrieve_btn = QPushButton("Retrieve")
        layout.addWidget(self.retrieve_btn)
        self.retrieve_btn.clicked.connect(self.retrieve_data)

    def retrieve_data(self):
        mast_model = self.mast_model_input.text()
        db = MastDatabase()
        data = db.get_data(mast_model)
        db.close()

        if data:
            result = "\n".join([f"{field}: {value}" for field, value in zip(
                ["Mast model", "Self weight", "Mast height", "Mast wind area"],
                data
            )])
            self.parent.result_text.setText(result)
        else:
            self.parent.result_text.setText("No data found for the given mast model.")
        self.parent.stacked_widget.hide()
        self.parent.show_main_buttons()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
def get_stylesheet():
    return """
    QWidget {
        font-family: "Segoe UI", sans-serif;
        font-size: 13px;
        background-color: #f9f9f9;
        color: #333;
    }

    QPushButton {
        background-color: #e0e0e0;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 5px 12px;
    }
    QPushButton:hover {
        background-color: #d6d6d6;
    }
    QPushButton:pressed {
        background-color: #c8c8c8;
    }

    QLineEdit, QTextEdit, QComboBox, QDateEdit {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 4px;
        background-color: white;
    }

    QTableWidget {
        border: 1px solid #ccc;
        background-color: white;
        gridline-color: #ddd;
    }

    QHeaderView::section {
        background-color: #efefef;
        border: 1px solid #ccc;
        padding: 4px;
    }

    QMessageBox {
        background-color: #ffffff;
    }

    QToolBar {
        background: #efefef;
        spacing: 8px;
        padding: 4px;
        border-bottom: 1px solid #ccc;
    }

    QLabel {
        font-weight: normal;
    }

    QDialog {
        background-color: #ffffff;
        border-radius: 6px;
    }

    QFormLayout {
        margin-top: 10px;
    }

    QTableWidget::item:selected {
        background-color: #d0e6f6;
    }
    """

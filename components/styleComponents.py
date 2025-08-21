from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
    QLabel,
    QSpinBox,
    QCheckBox,
    QDoubleSpinBox,
)
from styles import Styles
from PySide6.QtCore import Qt
from components.donutProgressBar import DonutProgressBar


class UIComponents:
    """Styled UI components"""

    @staticmethod
    def create_header_label(text):
        label = QLabel(text)
        label.setStyleSheet(Styles.HEADER_LABEL)
        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(50)
        return label

    @staticmethod
    def create_label(text, value):
        label = QLabel(text)
        if value == "w":
            label.setStyleSheet(Styles.LABEL)
        if value == "b":
            label.setStyleSheet(Styles.SIDEBAR_LABEL)
        return label

    @staticmethod
    def create_input_field(placeholder=""):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(Styles.INPUT_FIELD)
        return input_field

    @staticmethod
    def create_button(text, callback=None):
        button = QPushButton(text)
        button.setStyleSheet(Styles.BUTTON)
        if callback:
            button.clicked.connect(callback)
        return button

    @staticmethod
    def create_spinbox(min_val=1, max_val=65535, default_val=1):
        spinbox = QSpinBox()
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setValue(default_val)
        spinbox.setStyleSheet(Styles.SPINBOX_FIELD)
        return spinbox

    @staticmethod
    def create_timer_spinbox(min_val=0.001, max_val=60, default_val=1):
        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setValue(default_val)
        spinbox.setDecimals(3)
        spinbox.setSingleStep(0.1)
        spinbox.setStyleSheet(Styles.SPINBOX_FIELD)
        return spinbox

    @staticmethod
    def create_checkbox(text, checked=False, callback=None):
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        checkbox.setStyleSheet(Styles.CHECKBOX)
        if callback:
            checkbox.stateChanged.connect(callback)
        return checkbox

    @staticmethod
    def create_progress_bar(start_color="#00FF00", end_color="#FF0000"):
        """customizable gradient donut-style circular progress bar"""
        return DonutProgressBar(start_color=start_color, end_color=end_color)

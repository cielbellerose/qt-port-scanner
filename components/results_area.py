from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QSizePolicy,
    QTextBrowser,
    QAbstractItemView,
    QFrame,
    QHeaderView,
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from styles import Styles
from components.styleComponents import UIComponents


class ResultsArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def set_progress(self, value):
        # progress bar value (0-100)
        self.progress_bar.setValue(value)

    def set_summary(self, text):
        self.summary_text_area.setPlainText(text)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.create_progress_info_area(layout)

        # container for results and summary
        results_container = QFrame()
        results_layout = QVBoxLayout(results_container)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(10)

        self.create_results_table(results_layout)
        self.create_summary_area(results_layout)

        layout.addWidget(results_container, 1)

    def reset_ui(self):
        self.results_table.setRowCount(0)
        self.info_text_area.clear()
        self.summary_text_area.clear()
        self.progress_bar.setValue(0)

    def create_progress_info_area(self, layout):
        # progress donut and text area horizontal layout
        widget = QWidget()
        text_layout = QHBoxLayout(widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(10)

        # top progress donut section
        self.progress_bar = UIComponents.create_progress_bar(Styles.CLOSED, Styles.OPEN)
        self.progress_bar.setVisible(True)
        self.progress_bar.setFixedSize(80, 80)
        text_layout.addWidget(self.progress_bar)

        # top text info section
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)
        info_layout.addWidget(UIComponents.create_label("Scan Information:", "w"))

        self.info_text_area = QTextBrowser()
        self.info_text_area.setPlaceholderText("")
        self.info_text_area.setStyleSheet(Styles.TEXT_BOX)
        self.info_text_area.setMaximumHeight(90)

        info_layout.addWidget(self.info_text_area)
        text_layout.addWidget(info_widget)

        layout.addWidget(widget)

    def create_results_table(self, layout):
        layout.addWidget(UIComponents.create_label("Results:", "w"))

        table_scroll = QScrollArea()
        table_scroll.setWidgetResizable(True)
        table_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setRowCount(1)
        self.results_table.setHorizontalHeaderLabels(
            ["Status", "Port", "State", "Service", "Response Time"]
        )

        # table settings
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setMinimumSectionSize(40)

        self.results_table.setColumnWidth(0, 60)
        self.results_table.setColumnWidth(1, 80)
        self.results_table.setColumnWidth(2, 80)
        self.results_table.setColumnWidth(3, 140)
        self.results_table.setColumnWidth(4, 120)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.setSortingEnabled(True)
        self.results_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )  # cannot edit

        self.results_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_scroll.setWidget(self.results_table)

        layout.addWidget(table_scroll, 1)

    def create_summary_area(self, layout):
        container = QWidget()
        container.setFixedHeight(140)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        container_layout.addWidget(UIComponents.create_label("Scan Summary:", "w"))

        self.summary_text_area = QTextBrowser()
        self.summary_text_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.summary_text_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.summary_text_area.setPlaceholderText("")
        self.summary_text_area.setStyleSheet(Styles.TEXT_BOX)

        container_layout.addWidget(self.summary_text_area)

        layout.addWidget(container)

    def add_scan_result(self, result, show_all):
        # add a single scan result to the table
        should_show = show_all or result["status"] in ["OPEN"]

        if not should_show:
            return

        status_type = {"OPEN": "✓", "CLOSED": "✘", "ERROR": "!"}.get(
            result["status"], "?"
        )

        row_position = self.results_table.rowCount()
        self.results_table.insertRow(row_position)

        # create and add items to row
        # 0 indexed columns
        self.results_table.setItem(row_position, 0, QTableWidgetItem(status_type))
        self.results_table.setItem(
            row_position, 1, QTableWidgetItem(str(result["port"]))
        )
        self.results_table.setItem(row_position, 2, QTableWidgetItem(result["status"]))
        self.results_table.setItem(row_position, 3, QTableWidgetItem(result["service"]))
        self.results_table.setItem(
            row_position, 4, QTableWidgetItem(result["response_time"])
        )

        # state column color styling
        status_item = self.results_table.item(row_position, 2)
        if result["status"] == "OPEN":
            status_item.setBackground(QColor(Styles.OPEN))
            status_item.setForeground(QColor(Styles.DARK_TEXT))
        elif result["status"] == "CLOSED":
            status_item.setBackground(QColor(Styles.CLOSED))
            status_item.setForeground(QColor(Styles.TEXT_COLOR))
        else:  # ERROR
            status_item.setBackground(QColor(Styles.TEXT_COLOR))
            status_item.setForeground(QColor(Styles.DARK_TEXT))

from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from styles import Styles
from .layout_manager import LayoutManager
from components.styleComponents import UIComponents


class Sidebar(QFrame):
    scan_clicked = Signal()
    stop_clicked = Signal()
    clear_clicked = Signal()
    show_all_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()

    def set_scan_state(self, scanning):
        # update button states based on scan status
        self.scan_button.setEnabled(not scanning)
        self.clear_button.setEnabled(not scanning)
        self.stop_button.setEnabled(scanning)
        self.show_all_checkbox.setEnabled(not scanning)

    def on_show_all_changed(self, state):
        self.show_all_changed.emit(state)

    def checkbox_state(self):
        if self.show_all_checkbox:
            return self.show_all_checkbox.checkState() == Qt.Checked
        return True

    def setup_ui(self):
        content = QWidget()
        content.setStyleSheet(Styles.SIDEBAR_BACKGROUND)
        layout = QVBoxLayout(content)

        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.create_target_section(layout)
        self.create_port_section(layout)
        self.create_options_section(layout)
        layout.addStretch(1)
        self.create_controls_section(layout)

        layout.addStretch()

        frame_layout = QVBoxLayout(self)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(content)

    def create_target_section(self, layout):
        self.target_input = UIComponents.create_input_field("Enter IP or domain")
        target_section = LayoutManager.create_sidebar_section(
            UIComponents.create_label("Target:", "b"), self.target_input
        )
        layout.addWidget(target_section)

    def create_port_section(self, layout):
        self.start_port = UIComponents.create_spinbox(1, 65535, 80)
        self.end_port = UIComponents.create_spinbox(1, 65535, 85)
        port_layout = LayoutManager.create_port_range_layout(
            self.start_port, self.end_port
        )
        port_section = LayoutManager.create_sidebar_section()
        port_section.layout().addLayout(port_layout)
        layout.addWidget(port_section)

    def create_options_section(self, layout):
        self.show_all_checkbox = UIComponents.create_checkbox(
            "Show all ports", checked=True, callback=self.on_show_all_changed
        )
        self.timeout_spinbox = UIComponents.create_timer_spinbox(0.0001, 30, 1)

        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(self.timeout_spinbox)
        timeout_layout.addWidget(UIComponents.create_label("sec Timeout:", "b"))

        options_section = LayoutManager.create_sidebar_section(
            self.show_all_checkbox,
        )
        options_section.layout().addLayout(timeout_layout)
        layout.addWidget(options_section)

    def create_controls_section(self, layout):
        self.scan_button = UIComponents.create_button(
            "Start Scan", self.scan_clicked.emit
        )
        self.stop_button = UIComponents.create_button(
            "Stop Scan", self.stop_clicked.emit
        )
        self.clear_button = UIComponents.create_button(
            "Clear Results", self.clear_clicked.emit
        )

        button_layout = LayoutManager.create_button_grid(
            self.scan_button, self.stop_button, self.clear_button
        )
        controls_section = LayoutManager.create_sidebar_section()
        controls_section.layout().addLayout(button_layout)
        layout.addWidget(controls_section)

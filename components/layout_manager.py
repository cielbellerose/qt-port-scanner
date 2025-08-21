from PySide6.QtWidgets import QVBoxLayout, QWidget
from components.styleComponents import UIComponents
from styles import Styles


class LayoutManager:
    @staticmethod
    def create_sidebar_section(*widgets):
        """Create the left sidebar for inputs and controls"""
        section = QWidget()
        section.setStyleSheet(Styles.SIDEBAR_BACKGROUND)
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(5)

        for widget in widgets:
            layout.addWidget(widget)
        return section

    @staticmethod
    def create_port_range_layout(start_port, end_port):
        """Create a layout for port range inputs"""
        layout = QVBoxLayout()

        # Start port
        layout.addWidget(UIComponents.create_label("Start Port:", "b"))
        layout.addWidget(start_port)

        # End port
        layout.addWidget(UIComponents.create_label("End Port:", "b"))
        layout.addWidget(end_port)

        return layout

    @staticmethod
    def create_button_grid(*buttons):
        """Create a grid layout for buttons"""
        layout = QVBoxLayout()
        layout.setSpacing(12)

        for i, button in enumerate(buttons):
            layout.addWidget(button)
            if i < len(buttons) - 1:
                layout.addSpacing(5)
        return layout

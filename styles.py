class Styles:
    """Styles for Port Scanner GUI application"""

    DARK_BG = "#1f1f1f"
    LIGHT_BG = "#4A7B9D"
    HEADER_BG = "#2c3e50"
    BORDER_COLOR = "black"

    INPUT_DARK = "#2b2b2b"
    INPUT_LIGHT = "#555555"

    OPEN = "#6ce5e8"
    CLOSED = "#2c3e50"

    TEXT_COLOR = "#ffffff"
    DARK_TEXT = "#000000"

    BORDER_SIZE = "1px"
    MAIN_WINDOW = """
        QMainWindow {
            background-color: {DARK_BG};
            font-family: Arial;
            font-size: 12px;
            color: #ffffff;
        }
    """

    MAIN_WIDGET = f"""
        QWidget#central_widget {{
            font-family: Arial;
            color: {TEXT_COLOR};
            margin: 5px;
        }}
        QWidget {{
            background-color: {DARK_BG};
            font-family: Arial;
            color: {TEXT_COLOR};
        }}
    """

    SIDEBAR_BACKGROUND = f"""
        QWidget {{
            background-color: {LIGHT_BG};
        }}
        QWidget#border {{
            background-color: {LIGHT_BG};
            border-left: {BORDER_SIZE} solid {BORDER_COLOR};
            border-right: {BORDER_SIZE} solid {BORDER_COLOR};
            border-bottom: {BORDER_SIZE} solid {BORDER_COLOR};
            border-top: none;
        }}
    """

    HEADER_LABEL = f"""
        QLabel {{
            font-size: 18px;
            font-weight: bold;
            color: {TEXT_COLOR};
            background-color: {HEADER_BG};
            padding: 12px;
            border: {BORDER_SIZE} solid {BORDER_COLOR};
            margin: 0px;
        }}
    """

    INPUT_FIELD = f"""
        QLineEdit {{
            background-color: {INPUT_DARK};
            border: 1px solid {INPUT_LIGHT};
            color: {TEXT_COLOR};
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
        }}
        QLineEdit:focus {{
            border-color: #000000;
            outline: none;
        }}
    """

    TEXT_BOX = """
        QTextBrowser {
            padding: 5px;
            font-family: Arial;
            font-size: 12px;
            border: transparent
        }
    """

    SPINBOX_FIELD = f"""
        QSpinBox, QDoubleSpinBox {{
            background-color: {INPUT_DARK};
            border: 1px solid {INPUT_LIGHT};
            color: #ffffff;
            border-radius: 8px;
            padding: 5px;
            font-size: 14px;
            max-width: 80px;
            min-width: 80px;
            min-height: 20px;
        }}
        QSpinBox::up-button, QDoubleSpinBox::up-button {{
            width: 16px;
            border-left: 1px solid {INPUT_LIGHT};
        }}
        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            width: 16px;
            border-left: 1px solid {INPUT_LIGHT};
            border-top: 1px solid {INPUT_LIGHT};
        }}
        QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
            width: 0px;
            height: 0px;
            border-left: 1px solid transparent;
            border-right: 1px solid transparent;
            border-bottom: 2px solid {INPUT_LIGHT};
        }}
        QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
            width: 0px;
            height: 0px;
            border-left: 1px solid transparent;
            border-right: 1px solid transparent;
            border-top: 2px solid {INPUT_LIGHT};
        }}
    """

    SIDEBAR_LABEL = """
        QLabel {
            color: black;
            font-size: 15px;
            font-weight: bold;
            margin: 5px 0px 2px 0px;
        }
    """

    LABEL = f"""
        QLabel {{
            color: {TEXT_COLOR}
            font-size: 15px;
            font-weight: bold;
            margin: 5px 0px 2px 0px;
        }}
    """

    CHECKBOX = """
        QCheckBox {
            color: black;
            font-size: 12px;
            font-weight: bold;
            margin: 5px 0px 2px 0px;
        }
    """

    BUTTON = f"""
        QPushButton {{
            background-color: {INPUT_DARK};
            color: #ffffff;
            padding: 5px;
        }}
        QPushButton:hover {{
            background-color: #3a3a3a;
        }}
        QPushButton:pressed {{
            background-color: #4a4a4a;
        }}
    """

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QFont, QColor


class DonutProgressBar(QWidget):
    def __init__(self, parent=None, start_color="#00FF00", end_color="#FF0000"):
        super().__init__(parent)
        self.value = 0
        self.minimum = 0
        self.maximum = 100

        # donut styling
        self.bg_color = QColor("#3A3A3A")
        self.text_color = QColor("#ffffff")
        self.start_color = QColor(start_color)
        self.end_color = QColor(end_color)
        self.line_width = 12

    def setValue(self, value):
        self.value = max(self.minimum, min(self.maximum, value))
        self.update()

    def get_progress_color(self, progress_ratio):
        # RGB of start and end colors
        start_r = self.start_color.red()
        start_g = self.start_color.green()
        start_b = self.start_color.blue()
        end_r = self.end_color.red()
        end_g = self.end_color.green()
        end_b = self.end_color.blue()

        # interpolate!
        r = int(start_r + (end_r - start_r) * progress_ratio)
        g = int(start_g + (end_g - start_g) * progress_ratio)
        b = int(start_b + (end_b - start_b) * progress_ratio)

        return QColor(r, g, b)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # smooth edges

        rect = self.rect()
        center = rect.center()
        padding = self.line_width // 2 + 2
        radius = min(rect.width(), rect.height()) // 2 - padding

        # draw background donut
        painter.setPen(QPen(self.bg_color, self.line_width, Qt.SolidLine, Qt.RoundCap))
        painter.drawEllipse(
            center.x() - radius, center.y() - radius, radius * 2, radius * 2
        )

        # calculate and draw progress
        if self.maximum > self.minimum:
            progress_ratio = (self.value - self.minimum) / (self.maximum - self.minimum)
            progress_angle = int(360 * progress_ratio)

            # fetch color based on progress
            progress_color = self.get_progress_color(progress_ratio)

            painter.setPen(
                QPen(progress_color, self.line_width, Qt.SolidLine, Qt.RoundCap)
            )
            painter.drawArc(
                center.x() - radius,
                center.y() - radius,
                radius * 2,
                radius * 2,
                90 * 16,
                -progress_angle * 16,
            )

        # progress percentage text
        painter.setPen(QPen(self.text_color))
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        if self.maximum > self.minimum:
            percentage = int(
                (self.value - self.minimum) / (self.maximum - self.minimum) * 100
            )
        else:
            percentage = 0
        painter.drawText(rect, Qt.AlignCenter, f"{percentage}%")

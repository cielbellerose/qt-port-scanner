from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
import sys
import signal
from PySide6.QtCore import Signal, QThread, QTimer, Qt
from components.sidebar import Sidebar
from components.results_area import ResultsArea
from portScanner import PortScanner
from styles import Styles
from datetime import datetime
from components.styleComponents import UIComponents


class ScanThread(QThread):
    result_ready = Signal(dict)  # single port scan result ready
    progress_update = Signal(int, int)  # (current, total)
    scan_finished = Signal(list)

    def __init__(self, target, start_port, end_port, timeout=1.0):
        super().__init__()
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.scanner = PortScanner(timeout)

    # connects to port scanning logic
    def run(self):
        def callback(result, current, total):
            # Update results table
            self.result_ready.emit(result)
            # Update progress bar
            self.progress_update.emit(current, total)

        results = self.scanner.scan_range(
            self.target, self.start_port, self.end_port, callback
        )
        self.scan_finished.emit(results)

    def stop(self):
        self.scanner.stop_scan()


class SimplePortScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scan_thread = None
        self.scan_results = []
        self.show_all_results = True

        self.setup_window()
        self.setup_ui()
        self.apply_styles()
        self.connect_signals()

        self.sidebar.set_scan_state(False)

    def setup_window(self):
        self.setWindowTitle("Port Scanner")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 500)

    def setup_ui(self):
        main_widget = QWidget()
        main_widget.setObjectName("central_widget")

        self.setCentralWidget(main_widget)
        header = UIComponents.create_header_label("Network Port Scanner")

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        self.results_area = ResultsArea(self)

        content_layout.addWidget(self.sidebar, 1)
        content_layout.addWidget(self.results_area, 2)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(header)  # Sticky header
        main_layout.addWidget(content_widget)

    def apply_styles(self):
        self.setStyleSheet(Styles.MAIN_WINDOW)
        self.centralWidget().setStyleSheet(Styles.MAIN_WIDGET)

    def connect_signals(self):
        self.sidebar.stop_clicked.connect(self.on_stop_clicked)
        self.sidebar.scan_clicked.connect(self.on_scan_clicked)
        self.sidebar.clear_clicked.connect(self.on_clear_clicked)
        self.sidebar.show_all_changed.connect(self.on_show_all_changed)

    def on_scan_clicked(self):
        target = self.sidebar.target_input.text().strip()
        start_port = self.sidebar.start_port.value()
        end_port = self.sidebar.end_port.value()
        timeout = self.sidebar.timeout_spinbox.value()

        if not target:
            QMessageBox.warning(self, "Warning", "Please enter a target!")
            return
        if start_port > end_port:
            QMessageBox.warning(
                self, "Error", "Start port cannot be greater than end port"
            )
            return

        # ensure checkbox state is read
        self.show_all_results = self.sidebar.checkbox_state()

        # reset
        self.results_area.reset_ui()
        self.scan_results = []

        self.sidebar.set_scan_state(True)

        self.scan_thread = ScanThread(target, start_port, end_port, timeout)
        self.scan_thread.result_ready.connect(self.on_results_ready)
        self.scan_thread.progress_update.connect(self.on_progress_update)
        self.scan_thread.scan_finished.connect(self.on_scan_finished)
        self.scan_thread.start()

        self.results_area.info_text_area.append(
            f"Port Range: {start_port} - {end_port}"
        )
        self.results_area.info_text_area.append(f"Timeout: {timeout:.3f}s")
        self.results_area.info_text_area.append(
            "Started at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        mode_text = (
            "Show All Results" if self.show_all_results else "Show Open Ports Only"
        )
        self.results_area.info_text_area.append(f"Mode: {mode_text}")

    def on_show_all_changed(self, state):
        self.show_all_results = state == Qt.Checked

    def on_stop_clicked(self):
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()

            # reset UI state
            self.results_area.set_progress(0)
            self.sidebar.set_scan_state(False)

            QMessageBox.warning(self, "Information", "SCAN STOPPED!")

    def on_clear_clicked(self):
        self.results_area.reset_ui()
        self.scan_results = []
        self.sidebar.set_scan_state(False)
        self.results_area.set_progress(0)
        self.results_area.results_table.setRowCount(1)

    def on_results_ready(self, result):
        # individual scan results
        self.scan_results.append(result)
        self.results_area.add_scan_result(result, self.show_all_results)
        QApplication.processEvents()

    def on_progress_update(self, current, total):
        progress = (current / total) * 100
        self.results_area.set_progress(int(progress))

    def on_scan_finished(self, results):
        self.sidebar.set_scan_state(False)

        summary = []
        open_ports = [r for r in results if r["status"] == "OPEN"]
        closed_ports = [r for r in results if r["status"] == "CLOSED"]
        error_ports = [r for r in results if r["status"] == "ERROR"]

        summary.append(f"Open ports: {len(open_ports)}")
        summary.append(f"Closed ports: {len(closed_ports)}")
        summary.append(f"Error ports: {len(error_ports)}")
        summary.append(f"Total scanned: {len(results)}")

        if open_ports:
            summary.append("\nOPEN PORTS FOUND:")
            for port in open_ports:
                summary.append(
                    f"  Port {port['port']}: {port['service']} - {port['response_time']}"
                )
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results_area.info_text_area.append(f"Completed at: {timestamp}")
        self.results_area.set_summary("\n".join(summary))

    # called automatically whenever window closes (^C or x)
    def closeEvent(self, event):
        try:
            # clean up
            if hasattr(self, "scanner_thread"):
                if self.scanner_thread.isRunning():
                    self.scanner_thread.terminate()
                    self.scanner_thread.wait()

            if hasattr(self, "timer"):
                self.timer.stop()
                self.timer.deleteLater()

            if hasattr(self, "other_resource"):
                self.other_resource.cleanup()

        except Exception as e:
            print(f"Cleanup error: {e}", file=sys.stderr)

        finally:
            print("\nClosing application...")
            event.accept()


def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Port Scanner")

        window = SimplePortScanner()
        window.show()

        # if this OS supports SIGINT
        if hasattr(signal, "SIGINT"):
            # handles ^C exit
            def signal_handler(signum, frame):
                if window.isVisible():
                    QTimer.singleShot(0, window.close)
                QTimer.singleShot(0, app.quit)

            signal.signal(signal.SIGINT, signal_handler)

            timer = QTimer()
            timer.timeout.connect(lambda: None)
            timer.start(100)

        exit_code = app.exec()
        return exit_code

    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

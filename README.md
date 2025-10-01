# Network Port Scanner

Port scanner built with Python and PySide6.  
TCP Connect Scanning with interactive GUI and real-time results

<img width="796" height="645" alt="portScannerGUI" src="https://github.com/user-attachments/assets/cafc0a4b-12ef-4ef5-b505-8c4ed2d73def" />

## Features
- **Real-time Results** – Table updates live as each port is scanned
- **Visual Progress** – Animated donut-style progress bar with color gradient
- **Flexible Filtering** – Toggle between showing all ports or only open ports
- **Service Detection** – Automatic identification of common services
- **Response Time Tracking** – Millisecond-precision latency measurement
- **Configurable Timeout** – Adjustable connection timeout (0.001-60 seconds)
- **Scan Management** – Start, stop, and clear operations

## 🛠️ Technologies Used
- PySide6 – Qt for Python framework
- Python socket library

## Installation
```bash
# Clone the repository
git clone https://github.com/cielbellerose/qt-port-scanner
cd qt-port-scanner

# Install dependencies
pip install PySide6

# Run the application
python main.py
```

## Usage
- Enter target IP address or domain name
- Select start and end ports (default 80-85)
- Configure timeout (default 1s)
- Chose display mode
- Click Start Scan
- Cancel at any time

## Project Structure

| File/Directory | Description |
|----------------|-------------|
| `main.py` | Application entry point and main window |
| `portScanner.py` | Core TCP scanning engine |
| `styles.py` | Centralized stylesheet definitions |
| `sidebar.py` | Left control panel (inputs/buttons) for user input |
| `results_area.py` | Results display (table/progress/summary) |
| `donutProgressBar.py` | Circular progress widget |
| `styleComponents.py` | UI component factory |
| `layout_manager.py` | Layout builders |
| `commonPorts.py` | Port-to-service mapping dictionary |

## Future Ideas
- Implement different scanning techniques such as UDP
- Include a button to export/save results

## License  
This project is licensed under the **MIT License**

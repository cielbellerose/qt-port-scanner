import socket
import time
from components.commonPorts import COMMON_PORTS

"""
Port Scanner for network port discovery
TCP Connect Scanning (similar to Nmap -sT) 
Completes full TCP handshake (SYN, SYN-ACK, ACK)
"""


class PortScanner:
    def __init__(self, timeout=1.0):
        self.results = []
        self.is_scanning = False
        self.timeout = timeout

    def scan_single_port(self, target, port, timeout=None):
        if timeout is None:
            timeout = self.timeout
        try:
            # AF_INET = IPv4
            # SOCK_STREAM = TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            start_time = time.time()
            # attempt connection to remove server with TCP handshake
            result = sock.connect_ex((target, port))
            end_time = time.time()

            # close with FIN packets
            sock.close()

            # result = 0 means connection successful (open port accepting connections)
            if result == 0:
                response_time = round((end_time - start_time) * 1000, 2)  # milliseconds
                return {
                    "port": port,
                    "status": "OPEN",
                    "response_time": f"{response_time}ms",
                    "service": self.get_port_name(port),
                }
            else:
                return {
                    "port": port,
                    "status": "CLOSED",
                    "response_time": "timeout",
                    "service": self.get_port_name(port),
                }

        except socket.gaierror:
            # invalid target
            return {
                "port": port,
                "status": "ERROR",
                "response_time": "hostname error",
                "service": self.get_port_name(port),
            }
        except Exception as e:
            return {
                "port": port,
                "status": "ERROR",
                "response_time": str(e),
                "service": self.get_port_name(port),
            }

    def get_port_name(self, port):
        # fetch port name from dictionary
        return COMMON_PORTS.get(port, "Unknown")

    def scan_range(self, target, start_port, end_port, callback=None):
        # scan specified range of ports
        self.results = []
        self.is_scanning = True

        for port in range(start_port, end_port + 1):
            if not self.is_scanning:
                break

            result = self.scan_single_port(target, port)
            self.results.append(result)

            if callback:
                callback(result, port - start_port + 1, end_port - start_port + 1)

        self.is_scanning = False
        return self.results

    def stop_scan(self):
        self.is_scanning = False

# ─── Tests : Cyber Automation Toolkit ────────────────────────────────────────
# Lancement : python -m unittest discover tests
import os
import socket
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from main import parse_ports                       # noqa: E402
from modules import log_monitor, port_scanner      # noqa: E402


class TestParsePorts(unittest.TestCase):
    def test_list_and_range(self):
        self.assertEqual(parse_ports("22, 80,8000-8002"), [22, 80, 8000, 8001, 8002])

    def test_ignores_garbage(self):
        self.assertEqual(parse_ports("abc,443"), [443])


class TestPortScanner(unittest.TestCase):
    def test_detects_local_listener(self):
        server = socket.socket()
        server.bind(("127.0.0.1", 0))
        server.listen()
        port = server.getsockname()[1]
        try:
            results = port_scanner.scan_ports("127.0.0.1", [port])
        finally:
            server.close()
        self.assertEqual([p["port"] for p in results["open"]], [port])

    def test_unknown_host(self):
        results = port_scanner.scan_ports("host.invalid", [80])
        self.assertEqual(results["open"], [])


class TestLogMonitor(unittest.TestCase):
    def test_sample_log(self):
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)  # le rapport est écrit dans tmp/reports
            try:
                results = log_monitor.analyze_log(os.path.join(ROOT, "samples", "auth_sample.log"))
                self.assertTrue(os.listdir("reports"))
            finally:
                os.chdir(cwd)
        stats = results["stats"]
        self.assertEqual(stats["Brute force SSH"], 6)
        self.assertEqual(stats["Accès root SSH"], 1)
        self.assertEqual(stats["Utilisateur inconnu"], 2)
        self.assertEqual(stats["Tentative su échouée"], 1)
        self.assertEqual(stats["Scan de ports détecté"], 1)


if __name__ == "__main__":
    unittest.main()

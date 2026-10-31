# ─── Cyber Automation Toolkit — Configuration ───────────────────────────────

import sys

# Sortie console en UTF-8 : évite un crash sous Windows quand la sortie
# est redirigée vers un fichier (cp1252 ne connaît pas "─", "█", etc.)
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

TOOLKIT_VERSION = "1.1.0"
AUTHOR          = "bonberoww"

# Timeouts (secondes)
PORT_SCAN_TIMEOUT  = 1
SSH_TIMEOUT        = 5
DNS_TIMEOUT        = 3

# Nombre de connexions simultanées pour le scan de ports
SCAN_THREADS = 50

# Ports communs à scanner par défaut
DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143,
                 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]

# Dossier de sortie des rapports
REPORT_DIR = "reports"

# Couleurs terminal
COLORS = {
    "ok"    : "GREEN",
    "warn"  : "YELLOW",
    "error" : "RED",
    "info"  : "CYAN",
}
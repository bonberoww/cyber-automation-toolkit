# ─── Cyber Automation Toolkit — Configuration ───────────────────────────────

TOOLKIT_VERSION = "1.0.0"
AUTHOR          = "bonberoww"

# Timeouts (secondes)
PORT_SCAN_TIMEOUT  = 1
SSH_TIMEOUT        = 5
DNS_TIMEOUT        = 3

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
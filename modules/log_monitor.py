# ─── Module : Log Monitor ────────────────────────────────────────────────────
import os
import re
import datetime
from colorama import Fore, Style, init
from config.settings import REPORT_DIR

init(autoreset=True)

# Patterns suspects à détecter
SUSPICIOUS_PATTERNS = {
    "Brute force SSH"        : r"Failed password for .+ from .+ port \d+",
    "Accès root SSH"         : r"Accepted password for root",
    "Connexion refusée"      : r"Connection refused",
    "Sudo utilisé"           : r"sudo:.+COMMAND=",
    "Utilisateur inconnu"    : r"Invalid user .+ from",
    "Scan de ports détecté"  : r"kernel.*IPTABLES.*DROP",
    "Tentative su échouée"   : r"su: FAILED SU",
    "Segmentation fault"     : r"segfault at",
    "Erreur auth PAM"        : r"PAM: Authentication failure",
    "Connexion SSH réussie"  : r"Accepted (password|publickey) for .+ from",
}


def analyze_log(filepath: str) -> dict:
    """
    Analyse un fichier log et détecte les patterns suspects.
    Fonctionne avec /var/log/auth.log, syslog, ou tout fichier texte.
    """
    results = {
        "file"      : filepath,
        "timestamp" : str(datetime.datetime.now()),
        "findings"  : [],
        "stats"     : {},
    }

    if not os.path.exists(filepath):
        print(f"{Fore.RED}[!] Fichier introuvable : {filepath}{Style.RESET_ALL}")
        return results

    print(f"\n{Fore.CYAN}[*] Analyse de : {filepath}{Style.RESET_ALL}\n")

    with open(filepath, "r", errors="ignore") as f:
        lines = f.readlines()

    print(f"{Fore.CYAN}[*] {len(lines)} lignes à analyser...{Style.RESET_ALL}\n")

    for i, line in enumerate(lines, 1):
        for label, pattern in SUSPICIOUS_PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                severity = get_severity(label)
                color    = get_color(severity)
                finding  = {
                    "line"    : i,
                    "label"   : label,
                    "severity": severity,
                    "content" : line.strip(),
                }
                results["findings"].append(finding)
                results["stats"][label] = results["stats"].get(label, 0) + 1
                print(f"  {color}[{severity:<8}] L{i:<6} {label}{Style.RESET_ALL}")
                print(f"           {Fore.WHITE}{line.strip()[:100]}{Style.RESET_ALL}\n")

    # ── Résumé ──
    print(f"\n{'─'*60}")
    print(f"{Fore.CYAN}[+] RÉSUMÉ — {len(results['findings'])} événement(s) suspect(s){Style.RESET_ALL}\n")
    for label, count in sorted(results["stats"].items(), key=lambda x: x[1], reverse=True):
        print(f"  {get_color(get_severity(label))}{count:>4}x  {label}{Style.RESET_ALL}")

    save_report(results)
    return results


def get_severity(label: str) -> str:
    critical = ["Brute force SSH", "Accès root SSH", "Tentative su échouée"]
    high     = ["Utilisateur inconnu", "Scan de ports détecté", "Erreur auth PAM"]
    if label in critical : return "CRITICAL"
    if label in high     : return "HIGH"
    return "INFO"


def get_color(severity: str) -> str:
    return {
        "CRITICAL": Fore.RED,
        "HIGH"    : Fore.YELLOW,
        "INFO"    : Fore.CYAN,
    }.get(severity, Fore.WHITE)


def save_report(results: dict) -> str:
    """Sauvegarde le rapport dans /reports."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    ts       = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{REPORT_DIR}/log_monitor_{ts}.txt"

    with open(filename, "w") as f:
        f.write(f"=== Log Monitor Report ===\n")
        f.write(f"File      : {results['file']}\n")
        f.write(f"Timestamp : {results['timestamp']}\n")
        f.write(f"Findings  : {len(results['findings'])}\n\n")
        f.write(f"── Stats ──\n")
        for label, count in results["stats"].items():
            f.write(f"  {count}x {label}\n")
        f.write(f"\n── Détail ──\n")
        for f_ in results["findings"]:
            f.write(f"  [L{f_['line']}] [{f_['severity']}] {f_['label']}\n")
            f.write(f"    {f_['content']}\n\n")

    print(f"{Fore.GREEN}[+] Rapport sauvegardé : {filename}{Style.RESET_ALL}")
    return filename
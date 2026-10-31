# ─── Module : Port Scanner ───────────────────────────────────────────────────
import socket
import datetime
import os
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from config.settings import DEFAULT_PORTS, PORT_SCAN_TIMEOUT, REPORT_DIR, SCAN_THREADS

init(autoreset=True)


def check_port(ip: str, port: int) -> bool:
    """Tente une connexion TCP complète (connect scan) sur un port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(PORT_SCAN_TIMEOUT)
        return sock.connect_ex((ip, port)) == 0


def scan_ports(target: str, ports: list = None) -> dict:
    """
    Scanne les ports d'une cible et retourne les ports ouverts.
    Les ports sont testés en parallèle (SCAN_THREADS connexions simultanées).
    """
    if ports is None:
        ports = DEFAULT_PORTS

    results = {"target": target, "open": [], "closed": [], "timestamp": str(datetime.datetime.now())}

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{Fore.RED}[!] Hôte introuvable : {target}{Style.RESET_ALL}")
        return results

    print(f"\n{Fore.CYAN}[*] Scan de {target} ({ip}) — {len(ports)} ports...{Style.RESET_ALL}")

    with ThreadPoolExecutor(max_workers=SCAN_THREADS) as pool:
        states = list(pool.map(lambda p: check_port(ip, p), ports))

    for port, is_open in zip(ports, states):
        if is_open:
            service = get_service_name(port)
            print(f"  {Fore.GREEN}[OPEN]  {port:<6} {service}{Style.RESET_ALL}")
            results["open"].append({"port": port, "service": service})
        else:
            results["closed"].append(port)

    print(f"\n{Fore.CYAN}[+] Résultat : {len(results['open'])} port(s) ouvert(s) sur {target}{Style.RESET_ALL}")
    return results


# Services absents de la base système (surtout sous Windows)
EXTRA_SERVICES = {
    3389: "ms-wbt-server (RDP)", 5000: "logstash / upnp", 5601: "kibana",
    5900: "vnc", 8080: "http-alt", 8443: "https-alt", 9200: "elasticsearch",
}


def get_service_name(port: int) -> str:
    """Retourne le nom du service associé au port."""
    try:
        return socket.getservbyport(port)
    except OSError:
        return EXTRA_SERVICES.get(port, "unknown")


def save_report(results: dict) -> str:
    """Sauvegarde le rapport dans /reports."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"{REPORT_DIR}/portscan_{results['target']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"=== Port Scan Report ===\n")
        f.write(f"Target    : {results['target']}\n")
        f.write(f"Timestamp : {results['timestamp']}\n")
        f.write(f"Open ports: {len(results['open'])}\n\n")
        for p in results["open"]:
            f.write(f"  [OPEN] {p['port']} / {p['service']}\n")

    print(f"{Fore.GREEN}[+] Rapport sauvegardé : {filename}{Style.RESET_ALL}")
    return filename

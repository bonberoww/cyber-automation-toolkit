# ─── Module : Port Scanner ───────────────────────────────────────────────────
import socket
import datetime
from colorama import Fore, Style, init
from config.settings import DEFAULT_PORTS, PORT_SCAN_TIMEOUT, REPORT_DIR
import os

init(autoreset=True)

def scan_ports(target: str, ports: list = None) -> dict:
    """
    Scanne les ports d'une cible et retourne les ports ouverts.
    """
    if ports is None:
        ports = DEFAULT_PORTS

    results = {"target": target, "open": [], "closed": [], "timestamp": str(datetime.datetime.now())}

    print(f"\n{Fore.CYAN}[*] Scan de {target} — {len(ports)} ports...{Style.RESET_ALL}")

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(PORT_SCAN_TIMEOUT)
            result = sock.connect_ex((target, port))
            sock.close()

            if result == 0:
                service = get_service_name(port)
                print(f"  {Fore.GREEN}[OPEN]  {port:<6} {service}{Style.RESET_ALL}")
                results["open"].append({"port": port, "service": service})
            else:
                results["closed"].append(port)

        except socket.gaierror:
            print(f"{Fore.RED}[!] Hôte introuvable : {target}{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}[!] Erreur port {port} : {e}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}[+] Résultat : {len(results['open'])} port(s) ouvert(s) sur {target}{Style.RESET_ALL}")
    return results


def get_service_name(port: int) -> str:
    """Retourne le nom du service associé au port."""
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"


def save_report(results: dict) -> str:
    """Sauvegarde le rapport dans /reports."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"{REPORT_DIR}/portscan_{results['target']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.write(f"=== Port Scan Report ===\n")
        f.write(f"Target    : {results['target']}\n")
        f.write(f"Timestamp : {results['timestamp']}\n")
        f.write(f"Open ports: {len(results['open'])}\n\n")
        for p in results["open"]:
            f.write(f"  [OPEN] {p['port']} / {p['service']}\n")

    print(f"{Fore.GREEN}[+] Rapport sauvegardé : {filename}{Style.RESET_ALL}")
    return filename
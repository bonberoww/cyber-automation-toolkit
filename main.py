# ─── Cyber Automation Toolkit ────────────────────────────────────────────────
# Author  : bonberoww
# GitHub  : https://github.com/bonberoww
# Version : 1.0.0
# Usage   : python main.py
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
from colorama import Fore, Style, init
from config.settings import TOOLKIT_VERSION, AUTHOR

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
  ██████╗ ██╗   ██╗██████╗ ███████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
 ██╔════╝ ╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
 ██║       ╚████╔╝ ██████╔╝█████╗  ██████╔╝       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
 ██║        ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
{Style.RESET_ALL}
{Fore.WHITE}  Cyber Automation Toolkit v{TOOLKIT_VERSION} — by {AUTHOR}{Style.RESET_ALL}
{Fore.YELLOW}  Usage légal uniquement — lab perso / machines autorisées{Style.RESET_ALL}
"""

MENU = f"""
{Fore.CYAN}  ┌─────────────────────────────────────────┐
  │           MODULES DISPONIBLES           │
  ├─────────────────────────────────────────┤
  │  {Fore.GREEN}1{Fore.CYAN}  →  Port Scanner                      │
  │  {Fore.GREEN}2{Fore.CYAN}  →  SSH Audit                         │
  │  {Fore.GREEN}3{Fore.CYAN}  →  DNS Enumeration                   │
  │  {Fore.GREEN}4{Fore.CYAN}  →  Log Monitor                       │
  │  {Fore.RED}0{Fore.CYAN}  →  Quitter                           │
  └─────────────────────────────────────────┘{Style.RESET_ALL}
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def prompt(label: str) -> str:
    return input(f"\n{Fore.CYAN}  [{label}] >{Style.RESET_ALL} ").strip()


def run_port_scanner():
    from modules.port_scanner import scan_ports, save_report
    target = prompt("Cible (IP ou domaine)")
    if not target:
        print(f"{Fore.RED}[!] Cible invalide{Style.RESET_ALL}")
        return
    custom = prompt("Ports custom ? (laisse vide pour défaut)")
    ports  = [int(p.strip()) for p in custom.split(",") if p.strip().isdigit()] or None
    results = scan_ports(target, ports)
    save = prompt("Sauvegarder le rapport ? (o/n)")
    if save.lower() == "o":
        save_report(results)


def run_ssh_audit():
    from modules.ssh_audit import audit_ssh
    target = prompt("Cible SSH (IP)")
    if not target:
        print(f"{Fore.RED}[!] Cible invalide{Style.RESET_ALL}")
        return
    port = prompt("Port SSH (défaut : 22)")
    port = int(port) if port.isdigit() else 22
    audit_ssh(target, port)


def run_dns_enum():
    from modules.dns_enum import enumerate_dns
    domain = prompt("Domaine cible (ex: example.com)")
    if not domain:
        print(f"{Fore.RED}[!] Domaine invalide{Style.RESET_ALL}")
        return
    brute = prompt("Bruteforce sous-domaines ? (o/n)")
    enumerate_dns(domain, bruteforce=brute.lower() == "o")


def run_log_monitor():
    from modules.log_monitor import analyze_log
    print(f"\n{Fore.CYAN}  Exemples : C:\\logs\\auth.log  /var/log/auth.log{Style.RESET_ALL}")
    filepath = prompt("Chemin du fichier log")
    if not filepath:
        print(f"{Fore.RED}[!] Chemin invalide{Style.RESET_ALL}")
        return
    analyze_log(filepath)


def main():
    clear()
    print(BANNER)

    while True:
        print(MENU)
        choice = prompt("Choix")

        if choice == "1":
            clear()
            run_port_scanner()
        elif choice == "2":
            clear()
            run_ssh_audit()
        elif choice == "3":
            clear()
            run_dns_enum()
        elif choice == "4":
            clear()
            run_log_monitor()
        elif choice == "0":
            print(f"\n{Fore.CYAN}  [*] Fermeture du toolkit. Stay safe.{Style.RESET_ALL}\n")
            sys.exit(0)
        else:
            print(f"{Fore.RED}  [!] Choix invalide{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}  [Entrée pour continuer...]{Style.RESET_ALL}")
        clear()
        print(BANNER)


if __name__ == "__main__":
    main()
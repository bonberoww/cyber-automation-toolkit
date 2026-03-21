# ─── Module : SSH Audit ──────────────────────────────────────────────────────
import paramiko
import datetime
import os
from colorama import Fore, Style, init
from config.settings import SSH_TIMEOUT, REPORT_DIR

init(autoreset=True)

COMMON_CREDENTIALS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "123456"),
    ("root", "root"),
    ("root", "toor"),
    ("root", "password"),
    ("user", "user"),
    ("user", "password"),
    ("pi", "raspberry"),
    ("ubuntu", "ubuntu"),
]

def audit_ssh(target: str, port: int = 22, wordlist: list = None) -> dict:
    """
    Teste les credentials SSH faibles sur une cible.
    USAGE LÉGAL UNIQUEMENT — machines dont vous êtes propriétaire ou lab perso.
    """
    creds = wordlist if wordlist else COMMON_CREDENTIALS
    results = {
        "target"     : target,
        "port"       : port,
        "timestamp"  : str(datetime.datetime.now()),
        "vulnerable" : [],
        "tested"     : 0,
    }

    print(f"\n{Fore.CYAN}[*] Audit SSH {target}:{port} — {len(creds)} credential(s) à tester{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] Usage légal uniquement — lab perso / machines autorisées{Style.RESET_ALL}\n")

    for username, password in creds:
        results["tested"] += 1
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                target,
                port=port,
                username=username,
                password=password,
                timeout=SSH_TIMEOUT,
                banner_timeout=SSH_TIMEOUT,
            )
            print(f"  {Fore.RED}[VULN]  {username}:{password} — ACCÈS OBTENU{Style.RESET_ALL}")
            results["vulnerable"].append({"username": username, "password": password})
            client.close()

        except paramiko.AuthenticationException:
            print(f"  {Fore.GREEN}[OK]    {username}:{password} — refusé{Style.RESET_ALL}")
        except paramiko.SSHException as e:
            print(f"  {Fore.YELLOW}[WARN]  SSH error : {e}{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"  {Fore.RED}[ERR]   {e}{Style.RESET_ALL}")
            break

    status = f"{len(results['vulnerable'])} credential(s) vulnérable(s) trouvé(s)"
    print(f"\n{Fore.CYAN}[+] Résultat : {status}{Style.RESET_ALL}")
    save_report(results)
    return results


def save_report(results: dict) -> str:
    """Sauvegarde le rapport SSH dans /reports."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"{REPORT_DIR}/ssh_audit_{results['target']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.write(f"=== SSH Audit Report ===\n")
        f.write(f"Target    : {results['target']}:{results['port']}\n")
        f.write(f"Timestamp : {results['timestamp']}\n")
        f.write(f"Tested    : {results['tested']} credentials\n")
        f.write(f"Vulnerable: {len(results['vulnerable'])}\n\n")
        for v in results["vulnerable"]:
            f.write(f"  [VULN] {v['username']} : {v['password']}\n")

    print(f"{Fore.GREEN}[+] Rapport sauvegardé : {filename}{Style.RESET_ALL}")
    return filename
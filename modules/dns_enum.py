# ─── Module : DNS Enumeration ────────────────────────────────────────────────
import dns.resolver
import datetime
import os
from colorama import Fore, Style, init
from config.settings import DNS_TIMEOUT, REPORT_DIR

init(autoreset=True)

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR"]

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "remote", "blog", "webmail", "server",
    "ns1", "ns2", "smtp", "secure", "vpn", "m", "shop", "dev",
    "api", "admin", "portal", "test", "staging", "app", "git",
]


def enumerate_dns(domain: str, bruteforce: bool = True) -> dict:
    """
    Enumère les enregistrements DNS d'un domaine.
    """
    results = {
        "domain"    : domain,
        "timestamp" : str(datetime.datetime.now()),
        "records"   : {},
        "subdomains": [],
    }

    resolver = dns.resolver.Resolver()
    resolver.lifetime = DNS_TIMEOUT

    print(f"\n{Fore.CYAN}[*] Enumération DNS : {domain}{Style.RESET_ALL}\n")

    # ── Enregistrements DNS classiques ──
    for rtype in RECORD_TYPES:
        try:
            answers = resolver.resolve(domain, rtype)
            records = [str(r) for r in answers]
            results["records"][rtype] = records
            for r in records:
                print(f"  {Fore.GREEN}[{rtype:<5}] {r}{Style.RESET_ALL}")
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            print(f"{Fore.RED}[!] Domaine introuvable : {domain}{Style.RESET_ALL}")
            return results
        except Exception:
            pass

    # ── Bruteforce sous-domaines ──
    if bruteforce:
        print(f"\n{Fore.CYAN}[*] Bruteforce sous-domaines ({len(COMMON_SUBDOMAINS)} tentatives)...{Style.RESET_ALL}\n")
        for sub in COMMON_SUBDOMAINS:
            fqdn = f"{sub}.{domain}"
            try:
                answers = resolver.resolve(fqdn, "A")
                ips = [str(r) for r in answers]
                print(f"  {Fore.GREEN}[FOUND] {fqdn:<35} → {', '.join(ips)}{Style.RESET_ALL}")
                results["subdomains"].append({"subdomain": fqdn, "ips": ips})
            except Exception:
                print(f"  {Fore.RED}[----]  {fqdn}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}[+] {len(results['subdomains'])} sous-domaine(s) trouvé(s){Style.RESET_ALL}")
    save_report(results)
    return results


def save_report(results: dict) -> str:
    """Sauvegarde le rapport DNS dans /reports."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"{REPORT_DIR}/dns_enum_{results['domain']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"=== DNS Enumeration Report ===\n")
        f.write(f"Domain    : {results['domain']}\n")
        f.write(f"Timestamp : {results['timestamp']}\n\n")
        f.write(f"── Records ──\n")
        for rtype, records in results["records"].items():
            for r in records:
                f.write(f"  [{rtype}] {r}\n")
        f.write(f"\n── Subdomains ──\n")
        for s in results["subdomains"]:
            f.write(f"  {s['subdomain']} → {', '.join(s['ips'])}\n")

    print(f"{Fore.GREEN}[+] Rapport sauvegardé : {filename}{Style.RESET_ALL}")
    return filename
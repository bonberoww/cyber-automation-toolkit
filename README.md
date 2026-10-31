# Cyber Automation Toolkit

> Toolbox Python modulaire pour automatiser des tâches de reconnaissance et d'analyse en lab.
> Usage légal uniquement : machines dont vous êtes propriétaire ou environnement de test autorisé.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Tests](https://img.shields.io/badge/tests-unittest-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

📄 **Write-up des tests en lab : [docs/WRITEUP.md](docs/WRITEUP.md)**

---

## Modules

| Module | Commande | Description |
|---|---|---|
| `port_scanner.py` | `scan` | Scan TCP (connect) multi-thread avec identification des services |
| `ssh_audit.py` | `ssh` | Test d'une liste de credentials SSH faibles |
| `dns_enum.py` | `dns` | Enregistrements DNS (A, AAAA, MX, NS, TXT, SOA…) et bruteforce de sous-domaines |
| `log_monitor.py` | `logs` | Détection d'événements suspects dans un `auth.log` / `syslog` |

Chaque module génère un rapport horodaté dans `reports/` (ignoré par git).

---

## Installation

```bash
git clone https://github.com/bonberoww/cyber-automation-toolkit.git
cd cyber-automation-toolkit
python -m venv .venv && .venv/bin/pip install -r requirements.txt   # Windows : .venv\Scripts\pip
```

---

## Utilisation

Menu interactif :

```bash
python main.py
```

Ligne de commande :

```bash
python main.py scan 192.168.56.20 -p 22,80,443,8000-8100
python main.py ssh 192.168.56.20 --port 22
python main.py dns example.com --brute
python main.py logs samples/auth_sample.log
```

Import dans un script :

```python
from modules.port_scanner import scan_ports
scan_ports("192.168.56.20", ports=[22, 80, 443])
```

---

## Tests

```bash
python -m unittest discover tests
```

Les tests couvrent le parsing des ports, la détection d'un port ouvert sur une socket locale, la gestion d'un hôte introuvable et l'analyse du log d'exemple `samples/auth_sample.log`.

---

## Structure

```
cyber-automation-toolkit/
├── main.py                 # menu interactif + mode CLI
├── requirements.txt
├── config/settings.py      # timeouts, ports par défaut, threads
├── modules/
│   ├── port_scanner.py
│   ├── ssh_audit.py
│   ├── dns_enum.py
│   └── log_monitor.py
├── samples/auth_sample.log # log d'exemple (IP de documentation RFC 5737)
├── tests/test_toolkit.py
├── reports/                # rapports générés (non versionnés)
└── docs/WRITEUP.md
```

---

## Limites

- Scan en *connect* TCP : visible dans les logs de la cible, pas de scan SYN ni UDP (pour ça, Nmap).
- L'audit SSH teste une petite liste intégrée de credentials, de façon séquentielle.
- Pas de détection de version ni de CVE.

---

## Avertissement légal

Ce toolkit est développé à des fins éducatives. Toute utilisation sur des systèmes sans autorisation explicite est illégale (art. 323-1 et suivants du Code pénal).

---

## Auteur

Alessandro Peys — [@bonberoww](https://github.com/bonberoww) · Master Cybersécurité, Sup de Vinci

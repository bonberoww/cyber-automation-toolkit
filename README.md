# Cyber Automation Toolkit

> Scripts Python pour automatiser les tâches de sécurité — lab perso & audit.  
> Usage légal uniquement — machines dont vous êtes propriétaire ou environnement de test.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-En%20développement-orange?style=flat-square)

---

## Modules

| Module | Description |
|---|---|
| `port_scanner.py` | Scan de ports TCP avec détection de services |
| `ssh_audit.py` | Audit de credentials SSH faibles |
| `dns_enum.py` | Enumération DNS + bruteforce sous-domaines |
| `log_monitor.py` | Analyse de logs système et détection d'événements suspects |

---

## Installation
```bash
git clone https://github.com/bonberoww/cyber-automation-toolkit.git
cd cyber-automation-toolkit
pip install -r requirements.txt
python main.py
```

---

## Structure
```
cyber-automation-toolkit/
│
├── main.py
├── requirements.txt
│
├── config/
│   └── settings.py
│
├── modules/
│   ├── port_scanner.py
│   ├── ssh_audit.py
│   ├── dns_enum.py
│   └── log_monitor.py
│
└── reports/
```

---

## Utilisation

Menu interactif :
```bash
python main.py
```

Import direct :
```python
from modules.port_scanner import scan_ports
scan_ports("192.168.1.1", ports=[22, 80, 443])
```

---

## Avertissement légal

Ce toolkit est développé à des fins éducatives et de recherche.  
Toute utilisation sur des systèmes sans autorisation explicite est illégale.  
L'auteur décline toute responsabilité en cas d'usage malveillant.

---

## Auteur

Alessandro Peys — [@bonberoww](https://github.com/bonberoww)  
Etudiant Master Cybersécurité — Sup de Vinci Paris
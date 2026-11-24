# Cyber Automation Toolkit

Quelques scripts Python pour automatiser des tâches simples de reconnaissance et d'analyse, à utiliser sur mes propres machines ou sur une cible autorisée.

Un exemple d'utilisation commenté est dans [docs/WRITEUP.md](docs/WRITEUP.md).

## Ce que fait chaque module

| Commande | Rôle |
|---|---|
| `scan` | Scan de ports TCP, en parallèle, avec le nom du service |
| `ssh` | Teste une petite liste d'identifiants faibles sur un serveur SSH |
| `dns` | Récupère les enregistrements DNS d'un domaine et teste des sous-domaines courants |
| `logs` | Repère les événements suspects dans un `auth.log` (brute force, accès root, `su` raté…) |

Chaque module écrit un rapport texte dans `reports/`.

## Installation

```bash
git clone https://github.com/bonberoww/cyber-automation-toolkit.git
cd cyber-automation-toolkit
python -m venv .venv && .venv/bin/pip install -r requirements.txt   # Windows : .venv\Scripts\pip
```

## Utilisation

Menu interactif : `python main.py`

En ligne de commande :

```bash
python main.py scan 192.168.56.20 -p 22,80,443
python main.py ssh 192.168.56.20
python main.py dns example.com --brute
python main.py logs samples/auth_sample.log
```

## Tests

```bash
python -m unittest discover tests
```

## Limites

- Le scan est de type « connect » : visible dans les logs de la cible. Pour du SYN ou de l'UDP, Nmap fait mieux.
- L'audit SSH ne teste qu'une petite liste intégrée, l'un après l'autre.
- Pas de détection de versions ni de CVE.

## Usage légal

Ne l'utiliser que sur des systèmes dont on est propriétaire ou qu'on a l'autorisation de tester.

## Auteur

Alessandro Peys, Master Cybersécurité (Sup de Vinci). Projet personnel, licence MIT.

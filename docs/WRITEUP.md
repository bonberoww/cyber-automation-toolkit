# Write-up — Utiliser le toolkit pour auditer son propre lab

**Projet :** Cyber Automation Toolkit · **Domaine :** reconnaissance / audit · **Date du test :** 31/10/2026
**Cible :** ma propre machine, qui fait tourner le [SIEM Home Lab](https://github.com/bonberoww/siem-home-lab)

---

## 1. Objectif

Utiliser le toolkit sur un cas concret plutôt que sur des cibles au hasard : **vérifier que mon SIEM lab n'est pas exposé sur le réseau local**, analyser un journal d'authentification et lire les enregistrements DNS d'un domaine.

Toutes les cibles m'appartiennent ou sont publiques et prévues pour ça (`example.com`).

## 2. Test 1 — Exposition réseau du SIEM lab

Par défaut, Docker publie les ports d'un conteneur sur **toutes les interfaces** (`0.0.0.0`). Elasticsearch (9200), Kibana (5601) et Logstash (5000) seraient donc joignables par n'importe quelle machine du réseau local (Wi-Fi partagé, réseau d'entreprise…).

J'ai lié les ports à `127.0.0.1` dans le `docker-compose.yml`, puis j'ai vérifié le résultat depuis les deux interfaces :

```bash
python main.py scan 127.0.0.1    -p 5000,5601,9200
python main.py scan 192.168.1.17 -p 5000,5601,9200
```

```
[*] Scan de 127.0.0.1 (127.0.0.1) — 3 ports...
  [OPEN]  5000   logstash / upnp
  [OPEN]  5601   kibana
  [OPEN]  9200   elasticsearch
[+] Résultat : 3 port(s) ouvert(s) sur 127.0.0.1

[+] Résultat : 0 port(s) ouvert(s) sur 192.168.1.17
```

**Conclusion :** les services du lab ne répondent plus qu'en local. C'est une mesure simple, mais c'est le type de défaut de configuration qu'on retrouve souvent sur des Elasticsearch exposés par erreur.

## 3. Test 2 — Analyse d'un auth.log

```bash
python main.py logs samples/auth_sample.log
```

```
[+] RÉSUMÉ — 13 événement(s) suspect(s)

     6x  Brute force SSH
     2x  Connexion SSH réussie
     2x  Utilisateur inconnu
     1x  Accès root SSH
     1x  Tentative su échouée
     1x  Scan de ports détecté
```

**Lecture :** 6 échecs sur `root` depuis `203.0.113.45`, puis une connexion root réussie **depuis la même IP**. Le mot de passe a très probablement été deviné. Le module compte chaque ligne séparément : c'est à l'analyste de faire cette corrélation (le SIEM lab, lui, l'automatise avec des règles).

## 4. Test 3 — Énumération DNS

```bash
python main.py dns example.com
```

```
[A    ] 172.66.147.243
[A    ] 104.20.23.154
[MX   ] 0 .
[NS   ] elliott.ns.cloudflare.com.
[TXT  ] "v=spf1 -all"
```

**Lecture :** `MX 0 .` (« null MX », RFC 7505) et `v=spf1 -all` signifient que le domaine **n'envoie ni ne reçoit d'e-mails**. C'est une bonne pratique contre l'usurpation : personne ne peut envoyer de mail légitime au nom de ce domaine. Le DNS est hébergé chez Cloudflare (NS).

## 5. Bugs trouvés en écrivant les tests

| Bug | Impact | Correction |
|---|---|---|
| La regex `su: FAILED SU` ne gérait pas le PID (`su[2230]: FAILED SU`) | Les élévations ratées n'étaient jamais détectées sur de vrais logs | Regex `su(\[\d+\])?: FAILED SU` + test unitaire |
| Rapports écrits sans encodage explicite | Plantage `UnicodeEncodeError` sous Windows (caractères `─`, `é`) | `encoding="utf-8"` sur toutes les écritures |
| Sortie console en cp1252 sous Windows | Plantage dès que la sortie est redirigée vers un fichier | `sys.stdout.reconfigure(encoding="utf-8")` |
| Scan séquentiel | 20 ports fermés filtrés = jusqu'à 20 s d'attente | Scan parallèle (`ThreadPoolExecutor`, 50 threads) |

Le bug `su` est le plus instructif : sans test sur un log réaliste, le module aurait affiché « 0 tentative su » en donnant une fausse impression de sécurité.

## 6. Ce que j'en retiens

- Un outil de détection doit être **testé sur des données dont on connaît la réponse**, sinon un faux négatif passe inaperçu.
- Scanner sa propre infrastructure régulièrement permet d'attraper les expositions involontaires (ports Docker, services de debug…).
- Le toolkit ne remplace pas Nmap ou un SIEM. Il m'a surtout appris comment ces outils fonctionnent en dessous.

## 7. Suite

- [ ] Ajouter un export JSON des rapports (réutilisable dans le SIEM lab)
- [ ] Banner grabbing sur les ports ouverts
- [ ] Wordlist SSH externe en option (`--wordlist`)

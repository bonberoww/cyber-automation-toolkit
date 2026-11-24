# Write-up : utiliser le toolkit sur mon propre lab

Test du 31/10/2026. Toutes les cibles m'appartiennent ou sont publiques et prévues pour ça (`example.com`).

## Test 1 : mon SIEM est-il exposé sur le réseau ?

Par défaut, Docker publie les ports d'un conteneur sur toutes les interfaces. Elasticsearch (9200), Kibana (5601) et Logstash (5000) de mon [SIEM Home Lab](https://github.com/bonberoww/siem-home-lab) auraient donc été joignables par n'importe quelle machine du réseau local.

J'ai lié les ports à `127.0.0.1` dans le `docker-compose.yml`, puis j'ai scanné la machine par ses deux adresses :

```bash
python main.py scan 127.0.0.1 -p 5000,5601,9200
python main.py scan <adresse-de-la-machine-sur-le-reseau> -p 5000,5601,9200
```

```
127.0.0.1 : 3 ports ouverts (5000, 5601, 9200)
adresse réseau : 0 port ouvert
```

Les services ne répondent plus qu'en local.

## Test 2 : analyse d'un auth.log

```bash
python main.py logs samples/auth_sample.log
```

```
13 événements suspects
  6x  Brute force SSH
  2x  Connexion SSH réussie
  2x  Utilisateur inconnu
  1x  Accès root SSH
  1x  Tentative su échouée
  1x  Scan de ports détecté
```

6 échecs sur `root` depuis la même IP, puis une connexion root réussie : le mot de passe a sûrement été deviné. Le module compte chaque ligne séparément, la corrélation reste à faire à la main (mon SIEM l'automatise avec des règles).

## Test 3 : énumération DNS

```bash
python main.py dns example.com
```

Le domaine a un enregistrement `MX 0 .` et un SPF `v=spf1 -all` : il n'envoie ni ne reçoit de mails, ce qui empêche d'usurper son nom. Le DNS est hébergé chez Cloudflare.

## Bugs trouvés en écrivant les tests

- La regex qui détecte les `su` ratés ne gérait pas le numéro de processus (`su[2230]:`), donc elle ne trouvait rien sur de vrais logs. Corrigée, avec un test.
- Les rapports plantaient sous Windows à cause des accents : encodage UTF-8 ajouté.
- La sortie console plantait aussi quand elle était redirigée vers un fichier : corrigé.
- Le scan de ports était trop lent, un port après l'autre : il est maintenant en parallèle avec 50 threads.

Le bug du `su` est le plus parlant : sans test sur un log réaliste, le module aurait affiché « 0 tentative » et donné une fausse impression de sécurité.

## Ce que j'en retiens

- Un outil de détection doit être testé sur des données dont on connaît la réponse.
- Scanner sa propre infrastructure permet de repérer les expositions oubliées.
- Le toolkit ne remplace pas Nmap. Il m'a surtout appris comment ces outils fonctionnent.

## Suite

- Export JSON des rapports.
- Récupération des bannières sur les ports ouverts.
- Liste de mots de passe SSH externe en option.

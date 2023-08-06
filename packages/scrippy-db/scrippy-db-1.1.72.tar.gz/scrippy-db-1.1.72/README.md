![Build Status](https://drone.mcos.nc/api/badges/scrippy/scrippy-db/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, mon ami le scrangourou](./scrippy-db.png "Scrippy, mon ami le scrangourou")

# `scrippy_db`

Client de bases de données générique pour le cadriciel [`Scrippy`](https://codeberg.org/scrippy).

## Prérequis

### Modules Python

#### Liste des modules nécessaires

Les modules listés ci-dessous seront automatiquement installés.

- psycopg2-binary
- cx-Oracle

## Installation

### Manuelle

```bash
git clone https://codeberg.org/scrippy/scrippy-db.git
cd scrippy-db.git
sudo python3 -m pip install -r requirements.txt
make install
```

### Avec `pip`

```bash
sudo pip3 install scrippy-db
```

### Utilisation

Le module `scrippy_db.db` propose l'objet `Db` dont l'objectif est d'offrir les fonctionnalités liées à l'utilisation d'une base de données.

La connexion à une base de données peut se faire soit en fournissant directement les paramètres de connexion (`username`, `host`, `database`, `port`, `password`) au constructeur soit en fournissant le _nom du service_ sur lequel se connecter.

Le paramètre `db_type` permet de spécifier le type de base de données (`postgres` ou `oracle`). La valeur par défaut de ce paramètre est `postgres`.

L'exécution d'une requête est effectuée avec la méthode `Db.execute()` qui accepte les paramètres suivants:
- `request`: La requête en elle même (obligatoire)
- `params`: Les paramètres de la requête dans l'ordre exact de leur apparition au sein de la requête (optionnel)
- `verbose`: Booléen indiquant si la requête et son résultat doivent apparaître dans le log. Le niveau de log doit positionné a minima à `info`.

Une requête peut comporter un ou plusieurs paramètres variables nécessitant l'adaptation de la requête à ces paramètres.

Dans un soucis de sécurité certaines pratiques sont **strictement** à proscrire et d'autres doivent impérativement être appliquées.

Les paramètres d'une requête doivent être passés dans un *tuple* à la méthode `Db.execute()` qui se chargera de vérifier la validité des vos paramètres.

 N'essayez **jamais** de gérer vous même l'interpolation des paramètres à l'intérieur de la requête

#### Exemple

Récupération de données et mise à jour conditionnelle de la base.

```python
from scrippy_db import db

db_user = "harry.fink"
db_password = "dead_parrot"
db_host = "flying.circus"
db_port = "5432"
db_base = "monty_python"
app_name = "spanish_inquisition"
app_version "0.42.0"
app_status = "Deployed"

date = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')

with db.Db(username=db_user, host=db_host, port=db_port, database=db_base,  password=db_password) as database:
  # Vérification de l'état de l'application
  req = "select app_status, app_version, date from apps where app_name=%s;"
  params = (app_name,)
  current_status = database.execute(req, params, verbose=True)
  if current_status != None:
    # L'application est déjà enregistrée, on affiche son statut actuel
    # On met à jour son statut
    req = "insert into apps (app_name, app_version, app_status, date) values (%s, %s, %s, %s);"
    params = (app_name, app_version, app_status, date)
    result = database.execute(req, params, verbose=True)
  else:
    # L'application n'a jamais été enregistrée, on enregistre l'application et son statut.
    req = "insert into apps (app_name, app_version, app_status, date) values (%s, %s, %s, %s);"
    params = (app_name, app_version, app_status, date)
    result = database.execute(req, params, verbose=True)
```

![Build Status](https://drone.mcos.nc/api/badges/scrippy/scrippy-template/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)


![Scrippy, mon ami le scrangourou](./scrippy-template.png "Scrippy, mon ami le scrangourou")

# `scrippy_template`

Gestion simplifiée des fichiers modèles pour le cadriciel [`Scrippy`](https://codeberg.org/scrippy).

## Prérequis

### Modules Python

#### Liste des modules nécessaires

Les modules listés ci-dessous seront automatiquement installés.

- jinja2

## Installation

### Manuelle

```bash
git clone https://codeberg.org/scrippy/scrippy-template.git
cd scrippy-template.git
sudo python3 -m pip install -r requirements.txt
make install
```

### Avec `pip`

```bash
sudo pip3 install scrippy-template
```

### Utilisation

Ce module permet la génération de document à partir de fichiers modèles à partir du moteur de rendu *[jinja2](http://jinja.pocoo.org/)*

Pour être utilisables les fichiers modèles devront être situés dans le répertoire défini par le paramètre `base_path` passé en argument à l'objet `template.Renderer`.

Afin de gérer l'interpolation de variables le fichier modèle DOIT accepter un dictionnaire nommé `params` comme paramètre.

Les paramètres spécifiques à l'environnement _Jinja2_ peuvent être modifiés au travers de l'attribut `env` de l'objet `template.Renderer`.

Ce dictionnaire devra contenir l'ensemble des variables nécessaires au rendu complet du fichier modèle.

Le rendu du fichier modèle est obtenu à partir de l'objet `template.Renderer` dont l'instanciation nécessite le nom d'un fichier modèle ainsi que le chemin de base dans lequel chercher le fichier modèle.

Les paramètres spécifiques à l'environnement _Jinja2_ peuvent être modifiés au travers de l'attribut `env` de l'objet `template.Renderer`.

Par convention les fichiers modèles utilisés par le cadriciel _Scrippy_ sont rangés dans le répertoire défini par le paramètre de configuration `env::templatedirdir` (voir la configuration du [cadriciel _Scrippy_](https://codeberg.org/scrippy) dans [la documentation](https://codeberg.org/scrippy/scrippy-core) idoine).

Un modèle est un fichier texte simple dont certains passages dûment balisés seront interpolés par les variables passées en paramètres.

La méthode `Renderer.render()` renvoie le rendu du fichier modèle.

Les variables doivent être fournies au fichier modèle sous la forme d'un dictionnaire nommé `params`.

Le dictionnaire sera transmis au fichier modèle qui sera chargé de faire l'interpolation des variables qu'il contient.

Les fichiers modèles peuvent inclure:
- des structures de contrôle
- des boucles

#### Fichier modèle simple

Avec le fichier modèle suivant nommé *template_test.mod* et placé dans le répertoire `/var/lib/scrippy/templates`:

```txt
Bonjour {{params.user}}

Vous recevez cet e-mail car vous faites partie des administrateurs fonctionnels de l'application {{params.app}}.

L'exécution du script {{params.script}} du {{params.date}} s'est terminé sur le code d'erreur suivant:
- {{params.error.code}}: {{params.error.msg}}

--
Cordialement.
{{params.sender}}
```

L'utilisation du fichier modèle se fera de la manière suivante:

```python
import datetime
from scrippy_template import template

params = {"user": "Harry Fink",
          "app": "Flying Circus",
          "script": "dead_parrot.py",
          "date": datetime.datetime.now().strftime("%d/%m/%Y"),
          "error": {"code": 42,
                    "msg": "It’s not pinin’! It’s passed on! This parrot is no more!"},
          "sender": "Luiggi Vercotti", }

base_path = '/var/lib/scrippy/templates'
template_file = 'template.j2'
renderer = template.Renderer(base_path, template_file)

print(renderer.render(params))

```

Avec les valeurs par défaut le message affiché en fin de script contiendra:

```txt
Bonjour Harry Fink

Vous recevez cet e-mail car vous faites partie des administrateurs fonctionnels de l'application Flying Circus.

L'exécution du script dead_parrot.py du 15/09/2019 s'est terminé sur le code d'erreur suivant:
- 42: It’s not pinin’! It’s passed on! This parrot is no more!

--
Cordialement.
Luigi Vercotti
```

#### Fichier modèle avec structures de contrôle

```python
params = {"user": "Harry Fink",
          "app": "Flying Circus",
          "script": "dead_parrot.py",
          "date": datetime.datetime.now().strftime("%d/%m/%Y"),
          "num_error": 42,
          "sender": "Luiggi Vercotti", }
```

```txt
Bonjour {{params.user}}

Vous recevez cet e-mail car vous faites partie des administrateurs fonctionnels de l'application {{params.app}}.

L'exécution du script {{params.script}} du {{params.date}} s'est terminé:
{% if params.num_errors == 0 %}
- Sans erreur
{% else %}
- avec {{params.num_errors}} erreur(s)
{% endif %}

--
Cordialement.
{{params.sender}}
```

#### Fichier modèle avec boucle

```python
params = {"user": "Harry Fink",
          "app": "Flying Circus",
          "script": "dead_parrot.py",
          "date": datetime.datetime.now().strftime("%d/%m/%Y"),
          'errors': [{'code': 2, 'msg': "It's not pinin’! It's passed on! This parrot is no more!"},
                     {'code': 3, 'msg': "Ohh! The cat's eaten it."}],
          "sender": "Luiggi Vercotti", }
```

```txt
Bonjour {{params.user}}

Vous recevez cet e-mail car vous faites partie des administrateurs fonctionnels de l'application {{params.app}}.

L'exécution du script {{params.script}} du {{params.date}} s'est terminé avec les erreurs suivantes:
{% for error in params.errors %}
  {{ error.code }}: {{ error.msg}}
{% endfor %}

--
Cordialement.
{{params.sender}}
```

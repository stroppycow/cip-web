# Outil pour la consultation de l'index des professions

## Description
Lors de la rénovation de la nomenclature des professions et des catégories socio-professionnelle, un protocole de codage construit autour d'un index-numérique a été élaboré. Cet index est une table en deux dimensions construite par les expert de la nomenclature croisant des libellés de profession (en ligne) et des valeurs de variables annexes pertinentes pour coder les profession (statut, classification professionnelle, taille de l'entreprise) en colonne. A chaque case, se trouve un code PCS 2020.
Cette application permet de consulter l'index des professions issu de manière interractive.
Dans un premier temps, l'utilisateur peut à partir d'un libellé renseigné spontannément retrouver un libellé de cet index qui s'approche le plus.
Une fois un écho sélectionné, il peut lire les différents codes PCS 2020 associés selon les valeurs des variables annexes via un arbre.
Il peut également récupérer la description du poste de la nomenclature pour une combiansion de variables annexes donnée.

## Utilisation
### Instalation du logiciel et des dépendances
Cette application est écrite en python à partir du framework Django. Elle nécessite une version de python supérieure à 3.7 et les dépendances listées dans le fichier `requirements.txt`. Celles-ci peuvent être installées avec `pip install -r -requirements`. 
Elle interroge un service Elasticsearch qui permet de stocker et rechercher les différents documents (index des profession + postes de la nomenclature PCS 2020).

### Lancement de l'application
Avant de lancer cette application, la variable d'environnement `ELK_HOST` doit renseigner l'adresse d'accès au service Elasticsearch( par exemple, `ELK_HOST=localhost:9200` si elasticsearch est installé en local et accessible via le port 9200)
L'application peut ensuite être lancée avec la commande `python manage.py runserver` ou `python3 manage.py runserver`.

### Utilisation de l'API
Une API Rest est disponible pour bénéficier des fonctionnalités d'autocomplétion. Le swagger peut être consulté au chemin `/api/swagger-ui/`. 

### Utilisation des pages web
A documenter

## Méthodologie
A documenter

## Tester l'application
L'application peut être testée à l'adresse https://pcs2020.kub.sspcloud.fr/

## Livrable
Une image docker `git-registry.lab.sspcloud.fr/codification-automatique/consultation-index-pcs-2020/cip-web` est disponible.

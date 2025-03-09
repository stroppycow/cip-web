# Outil pour la consultation de l'index des professions

## Description
Lors de la rénovation de la nomenclature des professions et des catégories socio-professionnelles[^1], un protocole de codage construit autour d'un index-numérique a été élaboré. Cet index est une table en deux dimensions construite par les experts de la nomenclature croisant des libellés de profession (en ligne) et des valeurs de variables annexes en colonne, pertinentes pour coder les professions (statut, classification professionnelle, taille de l'entreprise). À chaque case se trouve un code PCS 2020.

Cette application permet de consulter l'index des professions de manière interractive. Dans un premier temps, l'utilisateur peut, à partir d'un libellé renseigné spontannément, retrouver un libellé de l'index qui s'en approche le plus.
Une fois un écho sélectionné, il peut lire les différents codes PCS 2020 associés selon les valeurs des variables annexes via un arbre.
Il peut également récupérer la description du poste de la nomenclature correspondant à la combiansion de variables annexes souhaitée.

## Utilisation
### Instalation du logiciel et des dépendances
Cette application est écrite en python à partir du framework Django. Elle nécessite une version de python supérieure à 3.7 et les dépendances listées dans le fichier `requirements.txt`. Celles-ci peuvent être installées avec `pip install -r -requirements`. 
Elle interroge un service Elasticsearch qui permet de stocker et rechercher les différents documents (index des professions et postes de la nomenclature PCS 2020).

### Lancement de l'application
Avant de lancer cette application, la variable d'environnement `ELK_HOST` doit renseigner l'adresse d'accès au service Elasticsearch( par exemple, `ELK_HOST=localhost:9200` si elasticsearch est installé en local et accessible via le port 9200)
L'application peut ensuite être lancée avec la commande `python manage.py runserver` ou `python3 manage.py runserver`.

### Utilisation de l'API
Une API Rest est disponible pour accéder aux fonctionnalités d'autocomplétion et de recherche dans l'index. Le swagger de cette API peut être consulté via le chemin `/api/swagger-ui/`. 

### Utilisation des pages web
A documenter

## Méthodologie
A documenter

## Tester l'application
L'application peut être testée à l'adresse https://pcs2020.kub.sspcloud.fr/

## Livrable
Une image docker hébergée sur dockerhub est disponible : `stroppycow/cip-web`.

[^1]: [AMOSSE Thomas, CHARDON Olivier, EIDELMAN Alexis, La rénovation de la nomenclature socioprofessionnelle (2018-2019), Rapport du groupe de travail du Cnis, Décembre 2019](https://www.cnis.fr/wp-content/uploads/2018/01/Rapport-n%C2%B0-156.pdf)

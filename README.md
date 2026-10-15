# Opération Salon Fantôme

> « Si vous lisez ces lignes, c’est que le salon a déjà disparu.
> Je m’appelle Jack Query. Kevin m’a laissé les archives, mais Mickael a déjà effacé une partie de ses traces. »

## Votre mission

Kevin, le maître des salons, est la victime d’un vol. Le salon privé Orbite a été masqué et son dossier confidentiel a été exporté.

Vous devez prouver :

1. quel salon a disparu ;
2. quel compte privilégié a été utilisé ;
3. qui a commis le vol.

Mickael est le voleur. Anthony possédait les privilèges utilisés. Lisa et Lydie sont des passantes ou des victimes dont les témoignages permettent de reconstituer la chronologie.

Vous devez lire les six dossiers de [game/dossiers.md](game/dossiers.md) dans l’ordre. Chaque requête doit utiliser au maximum un JOIN. Vous devez écrire une nouvelle requête lorsque vous avez besoin d’une nouvelle relation.

## Avant d’entrer dans les archives

Vous devez disposer de Python 3, SQLite 3, d’un terminal et d’une équipe capable de partager le terminal de l’enquêteur.

Vous ne devez modifier aucun fichier SQL pendant la partie.

## Le premier pas

Vous devez vous placer à la racine du projet, puis lancer :

~~~bash
python3 main.py
~~~

Vous devez ensuite ouvrir la base :

~~~bash
sqlite3 database/game.db
~~~

Vous devez commencer par afficher les tables :

~~~sql
.tables
.schema
~~~

Vous devez travailler en équipe, noter les preuves et ne pas conclure à partir d’un seul message.

## Validation finale

Quand vous pensez avoir retrouvé les trois éléments, vous devez quitter SQLite et lancer :

~~~bash
python3 main.py --answer 'SALON|COMPTE|VOLEUR'
~~~

Remplacez la valeur par votre preuve complète, dans cet ordre. Une mauvaise preuve vous demandera de vérifier les indices. Une preuve correcte vous permettra de contacter Kevin.

> « Lisa et Lydie ont vu les traces. Anthony avait la clé. Mickael a volé le dossier. À vous de le prouver. »
>
> — Jack Query

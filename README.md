# Opération Salon Fantôme

> « Si vous lisez ces lignes, vous savez déjà que le 🏕️ Campement 7 a été supprimé.
> Je m’appelle Jack Query. Votre mission n’est pas de retrouver le salon. Votre mission est de trouver le voleur. »

## Votre mission

Kevin, le maître des salons, vous prévient : le Campement 7 a été supprimé et son dossier confidentiel a été volé.

Vous connaissez donc la scène dès le début. Vous devez prouver :

1. quel compte privilégié a été compromis ;
2. qui a utilisé ce compte pour voler le dossier.

Les salons présents dans les archives sont :

- 📡 La grande salle ;
- 🔥 Le Feu de camp ;
- 👐 Besoin d’aide ;
- 🏕️ Campement 1 ;
- 🏕️ Campement 2 ;
- 🏕️ Campement 3 ;
- 🏕️ Campement 7, le salon supprimé.

Mickael est le voleur. Anthony possédait les privilèges utilisés. Lisa et Lydie sont des passantes ou des victimes dont les témoignages permettent de reconstituer la chronologie.

Vous devez lire les six dossiers de [game/dossiers.md](game/dossiers.md) dans l’ordre. Chaque requête doit utiliser au maximum un JOIN. Vous devez aussi utiliser COUNT, GROUP BY et HAVING pour repérer le pic d’activité autour du salon supprimé.

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

Quand vous pensez avoir identifié le compte compromis et le voleur, vous devez quitter SQLite et lancer :

~~~bash
python3 main.py --answer 'COMPTE|VOLEUR'
~~~

Remplacez la valeur par votre preuve complète, dans cet ordre. Une preuve correcte permettra de contacter Kevin.

> « Le salon a disparu. La question est : qui avait la clé, et qui s’en est servi ? »
>
> — Jack Query

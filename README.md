# Opération Salon Fantôme

> « Si vous lisez ces lignes, c’est que le salon a déjà disparu.
> Je m’appelle Jack Query. Je vous laisse une base de données, quelques traces et une question : saurez-vous retrouver ce qui a été effacé ? »

## Votre mission

Le salon vocal préféré de votre équipe s'est volatilisé. Pas supprimé. Pas détruit. Simplement… déplacé.

J'ai dispersé les archives dans une base de données : messages, membres, événements et anciennes traces de salons. Certaines pistes vous aideront. D'autres ont été placées là pour vous faire perdre du temps.

Vous devez désigner un enquêteur. Il prendra les commandes et partagera son terminal. Les autres membres de l'équipe devront l'aider en observant les résultats, en proposant des requêtes et en reliant les indices.

Vous devez retrouver le salon disparu et reconstituer le mot de passe qui permettra de clôturer l'affaire.

Vous devez lire les six dossiers de l'enquête dans [game/dossiers.md](game/dossiers.md), dans l'ordre. Vous devrez ensuite construire vos propres requêtes SQL.

## Avant d'entrer dans les archives

Vous devez disposer de Python 3, SQLite 3, d'un terminal, de VS Code ou d'un éditeur de texte, et d'une équipe capable de partager le terminal de l'enquêteur.

Vous ne devez vous connecter à aucun service externe. L'enquête est entièrement contenue dans ce dépôt.

## Le premier pas

Vous devez vous placer à la racine du projet, puis lancer le dossier :

```bash
python3 main.py
```

Vous devez ensuite ouvrir la base de données :

```bash
sqlite3 database/game.db
```

Une fois dans SQLite, vous devez commencer par afficher les tables disponibles :

```sql
.tables
```

Vous devez ensuite observer la structure de la base avec `.schema`. Vous pourrez alors explorer, filtrer, trier et relier les informations entre elles.

## Règles de l'enquête

- Vous devez travailler en équipe et partager chaque découverte.
- Vous ne devez pas modifier les fichiers SQL pendant la partie.
- Vous devez noter les fragments et leur ordre.
- Vous devez vous méfier des fausses pistes.
- Vous devez chercher les relations entre les tables : une information isolée ne suffira pas.

## Validation finale

Vous devez lancer la validation uniquement lorsque vous pensez avoir reconstitué le mot de passe :

```bash
python3 main.py --flag 'VOTRE_PROPOSITION'
```

Si votre proposition est incorrecte, vous devez vérifier vos fragments et recommencer. Si elle est correcte, vous devez contacter Kevin, le maître des salons : le dossier sera alors clôturé.

> « Les salons ne disparaissent jamais vraiment. Ils changent seulement d’endroit. À vous de trouver lequel. »
>
> — Jack Query

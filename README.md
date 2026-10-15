# Opération Salon Fantôme

> « Si vous lisez ces lignes, c’est que le salon a déjà disparu.
> Je m’appelle Jack Query. Je vous laisse une base de données, quelques traces et une question : saurez-vous retrouver ce qui a été effacé ? »

## Votre mission

Le salon vocal préféré de votre équipe s'est volatilisé. Pas supprimé. Pas détruit. Simplement… déplacé.

J'ai dispersé les archives dans une base de données : messages, membres, événements et anciennes traces de salons. Certaines pistes vous aideront. D'autres ont été placées là pour vous faire perdre du temps.

Désignez un enquêteur. Il prendra les commandes et partagera son terminal. Les autres membres de l'équipe seront ses yeux, sa mémoire et son instinct.

Votre objectif : retrouver le salon disparu et reconstituer le mot de passe qui permettra de clôturer l'affaire.

Les six dossiers de l'enquête se trouvent dans [game/dossiers.md](game/dossiers.md). Lisez-les dans l'ordre, puis construisez vos propres requêtes.

## Avant d'entrer dans les archives

Vous aurez besoin de Python 3, SQLite 3, un terminal, VS Code ou un éditeur de texte, et d'une équipe capable de partager le terminal de l'enquêteur.

Aucune connexion à Discord ni à un service externe n'est nécessaire.

## Le premier pas

Depuis la racine du projet :

```bash
python3 main.py
sqlite3 database/game.db
```

Commencez par observer la structure avec `.tables` et `.schema`. Explorez, filtrez, triez et reliez les informations entre elles.

## Règles de l'enquête

- Travaillez en équipe et partagez chaque découverte.
- Ne modifiez pas les fichiers SQL pendant la partie.
- Notez les fragments et leur ordre.
- Méfiez-vous des fausses pistes.
- Une information seule ne suffira pas : cherchez les relations.

## Validation finale

Quand votre équipe pense avoir reconstitué le mot de passe :

```bash
python3 main.py --flag 'VOTRE_PROPOSITION'
```

Une mauvaise proposition permet de recommencer. Une réponse correcte clôture le dossier et vous indique de contacter Kevin, le maître des salons.

> « Les salons ne disparaissent jamais vraiment. Ils changent seulement d’endroit. À vous de trouver lequel. »
>
> — Jack Query

# Opération Salon Fantôme

> « Si vous lisez ces lignes, c’est que le salon a déjà disparu.
> Je m’appelle Jack Query. Je vous laisse une base de données, quelques traces et une question : saurez-vous retrouver ce qui a été effacé ? »

## Votre mission

Le salon vocal préféré de votre équipe s'est volatilisé. Pas supprimé. Pas détruit. Simplement… déplacé.

J'ai dispersé les archives dans une base de données : messages, membres, événements et anciennes traces de salons. Certaines pistes vous aideront. D'autres ont été placées là pour vous faire perdre du temps.

Désignez un enquêteur. Il prendra les commandes et partagera son terminal. Les autres membres de l'équipe seront ses yeux, sa mémoire et son instinct. Observez les relations entre les informations, confrontez vos hypothèses et avancez dossier après dossier.

Votre objectif est simple à formuler, mais moins simple à accomplir : retrouver le salon disparu et reconstituer le mot de passe qui permettra de clôturer l'affaire.

> « Ne faites confiance à aucune information isolée. Une trace ne devient un indice que lorsqu’elle rencontre une autre trace. »
>
> — Jack Query

## Avant d'entrer dans les archives

Vous aurez besoin de :

- Python 3 ;
- SQLite 3 ;
- un terminal ;
- VS Code ou un éditeur de texte ;
- une équipe capable de partager le terminal de l'enquêteur.

Aucune connexion à Discord ni à un service externe n'est nécessaire. Tout ce dont vous avez besoin se trouve dans ce dépôt.

## Le premier pas

Depuis la racine du projet, lancez le dossier :

```bash
python3 main.py
```

La base d'archives se trouve ici :

```text
database/game.db
```

Pour interroger directement les archives :

```bash
sqlite3 database/game.db
```

Vous pouvez commencer par observer la structure :

```sql
.tables
.schema
```

Ensuite, écrivez vos propres requêtes. Les six dossiers de l'enquête vous demanderont d'explorer, filtrer, trier et surtout relier les informations entre elles.

## Règles de l'enquête

- Travaillez en équipe et partagez chaque découverte.
- Ne modifiez pas les fichiers SQL pendant la partie.
- Notez les fragments et l'ordre dans lequel vous les retrouvez.
- Méfiez-vous des fausses pistes.
- Une information seule ne suffira pas : cherchez les relations.
- Ne cherchez pas une solution externe. L'enquête est conçue pour être résolue depuis ce dépôt.
- Prenez le temps de vérifier vos hypothèses avant de les considérer comme certaines.

## Lorsque vous pensez avoir la réponse

Quand votre équipe pense avoir reconstitué le mot de passe, soumettez votre proposition :

```bash
python3 main.py --flag 'VOTRE_PROPOSITION'
```

Une mauvaise proposition ne met pas fin à l'enquête. Revenez à vos notes, vérifiez vos jointures et recommencez.

Si votre réponse est correcte, le dossier sera clôturé et Jack Query vous indiquera quoi faire ensuite.

> « Les salons ne disparaissent jamais vraiment. Ils changent seulement d’endroit.
> À vous de trouver lequel. »
>
> — Jack Query

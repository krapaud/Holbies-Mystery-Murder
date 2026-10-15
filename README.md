# Opération Salon Fantôme

Le salon vocal préféré de l'équipe a disparu. Jack Query a dispersé les indices dans des archives. Votre équipe choisit un enquêteur qui partage son terminal ; les autres participants l'aident à analyser les résultats.

## Pré-requis

- VS Code ou un éditeur de texte ;
- Python 3 ;
- SQLite en ligne de commande (`sqlite3`).

## Démarrer

Depuis la racine du projet :

```bash
python3 main.py
sqlite3 database/game.db
```

Explorez le schéma et les tables avec les commandes SQLite. Les six dossiers demandent de relier les archives, d'écarter les fausses pistes et de remettre les résultats dans l'ordre. Les jointures sont nécessaires pour obtenir les fragments.

Quand l'équipe pense avoir reconstitué le flag :

```bash
python3 main.py --flag 'VOTRE_FLAG'
```

Une erreur permet de réessayer sans réinitialiser l'enquête. Une réussite affiche une félicitation et demande de contacter Kevin, le maître des salons.

## Règles du jeu

- Ne modifiez pas les fichiers SQL pendant l'enquête.
- N'utilisez pas de solution externe : le dépôt est conçu pour être autonome.
- Les réponses ne sont pas données dans ce README.

# Architecture

La base SQLite est le cœur du jeu. `database/schema.sql` définit les relations, `database/seed.sql` fournit les archives fictives, `game/investigation_shell.py` fournit une console SQL en lecture seule avec narration de Jack Query, et un validateur terminal compare la saisie sans afficher le flag. Aucun service réseau n’est utilisé.

Flux : équipe -> `python3 main.py` -> base de travail ignorée par Git -> console SQL narrée; équipe -> validateur -> résultat correct ou erreur réessayable.

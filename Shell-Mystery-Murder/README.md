# Shell Mystery Murder

## Votre mission

Le projet étudiant **Northstar** devait être livré aujourd'hui. Quelques
minutes avant la présentation, `release/release-candidate.tar.gz` disparaît
et une branche de livraison apparaît dans le dépôt.

Vous êtes l'équipe chargée de reprendre l'enquête. Six dossiers racontent
l'affaire par fragments : témoignages, droits, contrôles, déplacements et
journaux techniques. Déterminez ce qui s'est passé, qui pouvait agir et qui
doit répondre de l'incident. Travaillez en équipe, sans modifier les preuves.

## Compétences mobilisées

Navigation, recherche, filtres, tri, redirections, variables, expansions,
permissions, branches, commits et différences Git. Docker, `.bashrc` et
`.profile` ne sont pas nécessaires.

## Parcours conseillé

1. Commencez par `dossiers/` et ouvrez les dossiers dans l'ordre de votre choix.
2. Relevez les noms, heures, sessions, branches et chemins.
3. Retrouvez les traces correspondantes dans `evidence/`.
4. Croisez au moins trois familles de preuves.
5. Écartez les actions légitimes avant de conclure.
6. Rédigez `investigation-report.md`.

## Rapport attendu

Votre rapport doit contenir une chronologie, les commandes utiles, les fausses
pistes écartées, trois preuves indépendantes et une conclusion argumentée.

```bash
cd Shell-Mystery-Murder
find dossiers evidence -type f -print | sort
```

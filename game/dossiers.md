# Les dossiers de Jack Query

Chaque dossier donne une direction, jamais la requête complète. L'enquêteur partage son terminal et l'équipe vérifie les hypothèses.

> « Vous n'êtes pas seuls dans ces archives. Si vous bloquez, lisez le message d'aide de chaque dossier. Je vous guiderai, mais je ne ferai pas l'enquête à votre place. » — Jack Query

## Dossier 1 — Les portes du réseau

« Avant de suivre une personne, regardez les lieux où elle pouvait se cacher. Les noms ne disent pas toujours la vérité. »

Inventoriez les salons et comparez leur type avec les traces d'activité qui leur sont associées. Repérez les lieux suspects sans conclure trop vite.

**Message d'aide de Jack :** Vous devez commencer par découvrir les tables avec `.tables`, puis observer leurs colonnes avec `.schema`. Cherchez d'abord les salons, pas encore le mot de passe.

## Dossier 2 — Ceux qui avaient les clés

« Un salon n'est jamais seulement un nom. Cherchez ceux qui y entraient, ceux qui y restaient et ceux qui apparaissaient au mauvais moment. »

Reliez les salons aux membres, puis confrontez les rôles et les auteurs des messages. Un membre intéressant n'est pas forcément celui qui parle le plus.

**Message d'aide de Jack :** Vous devez relier les tables avec la colonne qui identifie le salon. Regardez aussi les rôles et les dates avant de choisir un suspect.

## Dossier 3 — Les messages qui ne devaient pas rester

« Un message isolé raconte rarement toute la vérité. Replacez les paroles dans leur salon et face à leur auteur. »

Croisez messages, salons et membres. Certaines lignes ne sont que du contexte ou une fausse piste ; cherchez ce qui mérite d'être confirmé par les événements.

**Message d'aide de Jack :** Vous devez utiliser les messages pour trouver une piste, puis la confirmer avec la table des événements. Une phrase seule ne constitue pas une preuve.

## Dossier 4 — Les traces laissées après coup

« Les messages racontent ce que quelqu'un voulait montrer. Les événements racontent parfois ce qui s'est réellement passé. »

Confrontez les événements aux messages précédents. Comparez les dates, les types d'action, les personnes et les salons.

**Message d'aide de Jack :** Vous devez comparer les horodatages. Une action arrivée après un message peut confirmer ou contredire ce que vous venez de lire.

## Dossier 5 — Les pièces du témoignage

« Aucun indice ne devrait suffire à lui seul. Cherchez les traces qui se répondent. »

Reliez les indices aux messages et aux événements, puis vérifiez leur contexte avec les salons et les membres. Écartez ce qui ne respecte pas la chronologie.

**Message d'aide de Jack :** Vous devez examiner la table `clues`. Les lignes de type `decoy` sont des fausses pistes. Conservez seulement les fragments utiles et regardez leur ordre.

## Dossier 6 — Le salon qui refuse de mourir

« Le salon n'est caché ni dans une seule table, ni dans un seul témoignage. Réunissez les traces qui résistent à la comparaison. »

Reprenez les relations utiles, respectez l'ordre établi et assemblez seulement les informations confirmées. Quand l'équipe pense avoir terminé, utilisez le validateur.

**Message d'aide de Jack :** Vous devez relier `clues`, `messages` et `events` avec des `JOIN`, puis trier les fragments avec `fragment_order`. N'utilisez pas une ligne isolée et ne devinez pas l'ordre.

## Validation finale

Quand l'équipe pense avoir terminé, quittez SQLite et lancez :

```bash
python3 main.py --flag 'VOTRE_PROPOSITION'
```

Une mauvaise réponse permet de recommencer. Une réponse correcte affiche le message de réussite et demande de contacter Kevin, le maître des salons.

> « Si vous trouvez le bon salon, contactez Kevin, le maître des salons. » — Jack Query

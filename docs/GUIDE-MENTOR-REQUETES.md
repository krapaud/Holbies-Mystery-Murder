# Guide mentor — Opération Salon Fantôme

Ce document est réservé au mentor. Le dossier `docs/` est ignoré par Git.

## Voix de Jack Query

Après les résultats, Jack réagit au type d’archive consulté : il reconnaît une trace, une parole, une autorisation ou un événement, puis commente les recoupements entre deux archives. Une recherche vide déclenche une réaction liée au registre interrogé. Ses répliques ne nomment jamais le coupable et ne remplacent pas les indices du mentor.

## Histoire et vérité

- Kevin est la victime et le propriétaire du 🏕️ Campement 7.
- Anthony possède le privilège `manage` sur ce salon.
- Mickael est le voleur et a utilisé les droits d’Anthony.
- Lisa et Lydie sont passantes ou victimes.
- Nora, Samir et Zoé sont des témoins secondaires sans connaissance du vol.

## Étape 1 — Confirmer la scène connue

```sql
SELECT channel_id, channel_name, status
FROM channels
WHERE status != 'active';
```

Attendu : le Campement 7 est connu comme salon supprimé. Il ne faut plus demander aux étudiants de le découvrir comme une énigme.

Indice PNJ : « Le salon annoncé par Kevin figure dans les archives. Relevez son identifiant et son état actuel. »

Résultat de référence : `channel_id = 7`, `status = hidden`. Corriger la narration si les étudiants croient devoir découvrir la suppression : Kevin l’annonce dès le départ.

## Étape 2 — Comparer les volumes avec HAVING

Cette étape doit produire une comparaison, pas filtrer jusqu’à ne laisser que le Campement 7. Les étudiants regroupent les journaux par salon, conservent les groupes ayant au moins deux traces, puis classent les volumes du plus élevé au plus faible. La requête reste sans jointure : l’identifiant se recoupe avec celui relevé à l’étape 1.

```sql
SELECT channel_id, COUNT(*) AS trace_count
FROM access_logs
GROUP BY channel_id
HAVING COUNT(*) >= 2
ORDER BY trace_count DESC, channel_id;
```

Attendu avec le seed actuel, dans cet ordre : Campement 7 (`channel_id = 7`) avec 4 traces, puis les salons 1, 2, 3 et 4 avec 2 traces chacun. Les salons 5 et 6 n’atteignent pas le seuil et ne figurent donc pas dans le résultat. L’écart désigne une piste à examiner, pas une preuve de vol. Les étudiants doivent pouvoir expliquer que `HAVING` filtre les groupes après leur agrégation, contrairement à `WHERE` qui filtre des lignes avant le regroupement.

Indice PNJ : « Le relevé ne raconte pas encore les actes. Comparez les volumes, puis rapprochez l’identifiant qui se détache de la scène que Kevin vous a signalée. »

## Étape 3 — Trouver le privilège

```sql
SELECT member_id, channel_id, privilege, granted_at
FROM access_grants
WHERE privilege = 'manage'
  AND channel_id = 7;
```

Attendu : Anthony possède le privilège de gestion sur le Campement 7.

Pour afficher le nom du compte avec une seule jointure :

```sql
SELECT m.display_name, g.privilege, g.channel_id, g.granted_at
FROM access_grants AS g
JOIN members AS m ON m.member_id = g.member_id
WHERE g.privilege = 'manage'
  AND g.channel_id = 7;
```

Indice PNJ : « Celui qui possède la clé n’est pas forcément celui qui l’a utilisée. »

## Étape 4 — Lire les témoignages

```sql
SELECT message_id, channel_id, member_id, sent_at, body, evidence_tag
FROM messages
WHERE evidence_tag LIKE 'TEMOIN-%'
ORDER BY sent_at;
```

Attendu : dix déclarations, visibles dans une seule chronologie. Kevin confirme que le propriétaire du badge nie avoir exporté le dossier. Les étudiants doivent associer les auteurs aux noms, puis distinguer les observations utiles des propos sans information sur le vol.

Pour afficher les noms avec une seule jointure :

```sql
SELECT m.display_name, msg.sent_at, msg.body, msg.evidence_tag
FROM messages AS msg
JOIN members AS m ON m.member_id = msg.member_id
WHERE msg.evidence_tag LIKE 'TEMOIN-%'
ORDER BY msg.sent_at;
```

Attendu : Lisa rapporte une silhouette aperçue à plusieurs endroits. Lydie observe un badge ressemblant à celui d’Anthony, mais ne reconnait pas son porteur. Nora, Samir et Zoé posent des questions ordinaires sans information sur le vol.

Lecture détaillée pour le mentor : Lisa situe une silhouette à Campement 1 puis à Besoin d’aide, sans distinguer le visage. Elle la revoit à Besoin d’aide et remarque qu’elle change de direction en voyant du monde. Lydie voit au Feu de camp un badge semblable à celui d’Anthony, puis passe par Campement 2. Elle n’a pas vu Anthony quitter son poste pendant son propre passage. Kevin rapporte ensuite que le propriétaire du badge nie l’export. Nora cherche la salle de pause, Samir son chargeur et Zoé son carnet. Ces trois derniers messages n’apportent rien à l’enquête.

Indice PNJ : « Une déclaration parle d’un badge, une autre d’une silhouette. Vérifiez leurs heures et leurs déplacements avant de les relier. »

## Étape 5 — Identifier l’utilisation frauduleuse

```sql
SELECT credential_owner_id, actor_id, action, occurred_at, device, details
FROM access_logs
WHERE channel_id = 7
ORDER BY occurred_at;
```

Attendu : l’export et l’archivage du Campement 7 sont réalisés avec le compte d’Anthony par un autre identifiant, celui de Mickael.

Pour afficher le nom de l’auteur avec une seule jointure :

```sql
SELECT a.action, a.occurred_at, m.display_name AS actor
FROM access_logs AS a
JOIN members AS m ON m.member_id = a.actor_id
WHERE a.channel_id = 7
  AND a.action IN ('export', 'archive')
ORDER BY a.occurred_at;
```

Indice PNJ : « Comparez credential_owner_id et actor_id. La différence est la preuve du détournement. »

## Étape 6 — Écarter le faux message

Cette étape complète le dossier 6 : confronter le message publié après le vol aux heures des actions et au témoignage tardif de Kevin.

```sql
SELECT member_id, sent_at, body, evidence_tag
FROM messages
WHERE evidence_tag = 'DECOY';
```

Attendu : le message apparaît à 08:58, après l’export et le masquage du salon. Il affirme que la recherche est terminée, ce qui ne concorde pas avec les traces précédentes. Ce décalage est un élément à interpréter, pas une preuve suffisante à lui seul.

Pour confronter la chronologie technique sans jointure supplémentaire :

```sql
SELECT event_type, occurred_at, details
FROM events
WHERE channel_id = 7
ORDER BY occurred_at;
```

Attendu : le journal confirme l’ouverture du salon à 08:31, l’attribution du privilège à 08:32 et l’événement de vol à 08:52. Kevin constate que le salon est masqué à 08:53. Les équipes doivent rapprocher ces heures des journaux d’accès, des déclarations des témoins et du message tardif. La conclusion doit s’appuyer sur plusieurs sources, pas sur le seul message `DECOY`.

Indice PNJ : « Le message le plus bruyant n’est pas forcément la preuve la plus ancienne. »

## Validation finale

Pour vérifier les deux identités sans dépasser la limite d’une jointure par requête, lancer les deux recherches séparément.

Compte dont les droits sont enregistrés pour l’export :

```sql
SELECT m.display_name AS credential_owner
FROM access_logs AS a
JOIN members AS m ON m.member_id = a.credential_owner_id
WHERE a.channel_id = 7 AND a.action = 'export';
```

Personne enregistrée comme exécutante de l’export :

```sql
SELECT m.display_name AS actor
FROM access_logs AS a
JOIN members AS m ON m.member_id = a.actor_id
WHERE a.channel_id = 7 AND a.action = 'export';
```

Les étudiants doivent produire :

```text
COMPTE|VOLEUR
```

Attendu mentor :

```text
ANTHONY|MICKAEL
```

Test d’échec :

```bash
python3 main.py --answer 'ANTHONY|LISA'
```

Test de réussite : utiliser la preuve attendue ci-dessus.

## Règle pédagogique

Chaque requête étudiante doit contenir zéro ou un seul `JOIN`. Une nouvelle relation implique une nouvelle requête. Ne donnez pas directement la preuve finale : donnez seulement l’indice de l’étape en cours.

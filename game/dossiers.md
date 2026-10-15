# Les dossiers de Jack Query

> « Vous savez déjà que le 🏕️ Campement 7 a été supprimé. Kevin veut autre chose : savoir qui a utilisé une clé légitime pour commettre le vol. » — Jack Query

Le salon supprimé n’est pas à retrouver. Vous devez identifier le compte privilégié compromis et le véritable voleur. Une requête ne doit utiliser qu’un seul JOIN.

## Dossier 1 — La scène connue

Le Campement 7 est le salon supprimé. Vous devez retrouver les traces qui s’y rapportent et noter son channel_id pour vos recherches.

**Indice de Jack :** le statut hidden confirme la scène, mais ne constitue pas la réponse. La question est : qui a pu agir dans ce salon ?

## Dossier 2 — Le pic d’activité

Vous devez compter les accès enregistrés pour chaque salon et repérer le groupe qui contient au moins trois traces.

~~~sql
SELECT channel_id, COUNT(*) AS trace_count
FROM access_logs
GROUP BY channel_id
HAVING COUNT(*) >= 3;
~~~

Cette requête doit faire apparaître le Campement 7 avec quatre traces. Elle sert à repérer le pic d’activité suspect.

**Indice de Jack :** COUNT vous dit combien de traces existent. HAVING vous permet de conserver uniquement les groupes assez importants.

## Dossier 3 — Le compte privilégié

Anthony possédait les droits manage sur le Campement 7. Vous devez prouver que son compte était suffisamment puissant pour permettre le vol.

**Indice de Jack :** la table access_grants contient les autorisations. Le propriétaire d’une clé n’est pas automatiquement le voleur.

## Dossier 4 — Les témoignages

Lisa et Lydie sont des passantes ou des victimes. Elles n’ont pas volé le salon. Leurs messages donnent des horaires et décrivent le badge utilisé.

**Indice de Jack :** vous devez relier un message à son auteur avec une seule jointure si vous avez besoin du nom. Ne faites pas parler les témoignages hors de leur chronologie.

## Dossier 5 — L’identité derrière la clé

Vous devez comparer credential_owner_id et actor_id dans access_logs.

- credential_owner_id désigne le compte dont les droits sont utilisés ;
- actor_id désigne la personne qui réalise l’action.

**Indice de Jack :** si les deux identifiants sont différents lors de l’export, le compte a été détourné.

## Dossier 6 — Le coupable

Mickael est le véritable voleur. Vous devez le prouver grâce à l’action export, aux horaires et au compte d’Anthony.

Vous devez produire uniquement :

~~~text
COMPTE|VOLEUR
~~~

**Indice de Jack :** Anthony avait la clé. Mickael l’a utilisée.

## Validation

Quittez SQLite puis lancez :

~~~bash
python3 main.py --answer 'COMPTE|VOLEUR'
~~~

Une preuve correcte identifie le compte compromis et le voleur. Kevin vous indiquera alors la suite.

> « Le salon a disparu, mais le voleur a laissé sa trace. » — Jack Query

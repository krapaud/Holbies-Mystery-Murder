# Les dossiers de Jack Query

> « Vous savez déjà que le 🏕️ Campement 7 a été supprimé. Kevin veut autre chose : savoir qui a utilisé une clé légitime pour commettre le vol. » — Jack Query

Le salon supprimé n’est pas à retrouver. Vous devez identifier le compte privilégié compromis et le véritable voleur. Une requête ne doit utiliser qu’un seul JOIN.

## Dossier 1 — La scène connue

Le Campement 7 est le salon supprimé. Vous devez retrouver les traces qui s’y rapportent et noter son channel_id pour vos recherches.

**Indice de Jack :** le statut hidden confirme la scène, mais ne constitue pas la réponse. La question est : qui a pu agir dans ce salon ?

## Dossier 2 — Le pic d’activité

Vous devez comparer le volume d’accès enregistré pour chaque salon et repérer le groupe qui contient au moins trois traces.

Vous devez produire une requête qui regroupe les accès par channel_id, compte le nombre de traces et filtre les groupes après le regroupement.

**Indice de Jack :** utilisez une fonction d’agrégation pour compter, regroupez les lignes par salon, puis utilisez le filtre adapté aux résultats agrégés. Le Campement 7 doit apparaître avec quatre traces.

## Dossier 3 — Le compte privilégié

Vous devez identifier, dans access_grants, le compte qui possède le privilège manage sur le Campement 7 et noter son member_id.

**Indice de Jack :** la table access_grants contient les autorisations. Le propriétaire d’une clé n’est pas automatiquement le voleur.

## Dossier 4 — Les témoignages

Deux témoins ou victimes ont laissé des messages. Ils n’ont pas volé le salon. Leurs messages donnent des horaires et décrivent le badge utilisé.

**Indice de Jack :** vous devez relier un message à son auteur avec une seule jointure si vous avez besoin du nom. Ne faites pas parler les témoignages hors de leur chronologie.

## Dossier 5 — L’identité derrière la clé

Vous devez comparer credential_owner_id et actor_id dans access_logs.

- credential_owner_id désigne le compte dont les droits sont utilisés ;
- actor_id désigne la personne qui réalise l’action.

**Indice de Jack :** si les deux identifiants sont différents lors de l’export, le compte a été détourné.

## Dossier 6 — Le coupable

Vous devez identifier la personne indiquée par actor_id lors de l’action export du Campement 7. Croisez cette trace avec les horaires, les témoignages et l’action archive.

Vous devez produire uniquement :

~~~text
COMPTE|VOLEUR
~~~

**Indice de Jack :** le propriétaire de la clé n’est pas celui qui l’a utilisée.

## Validation

Quittez SQLite puis lancez :

~~~bash
python3 main.py --answer 'COMPTE|VOLEUR'
~~~

Une preuve correcte identifie le compte compromis et le voleur. Kevin vous indiquera alors la suite.

> « Le salon a disparu, mais le voleur a laissé sa trace. » — Jack Query

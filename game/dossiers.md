# Les dossiers de Jack Query

> « Kevin a perdu le salon Orbite. Mickael a volé son contenu. Mais il n’a pas forcé la porte : il a utilisé un accès qui appartenait à quelqu’un d’autre. À vous de retrouver les preuves. » — Jack Query

Vous devez enquêter dans l’ordre. Une requête ne doit utiliser qu’un seul JOIN. Si vous avez besoin d’une nouvelle relation, vous devez écrire une nouvelle requête.

## Dossier 1 — Le salon disparu

Kevin est la victime. Vous devez retrouver le salon qu’il avait créé et déterminer son état actuel.

**Indice de Jack :** commencez avec la table channels. Cherchez le salon dont le statut est hidden.

## Dossier 2 — Le salon qui parle le plus

Tous les salons ne présentent pas le même nombre de traces. Vous devez compter les accès enregistrés pour chaque salon et ne conserver que celui qui possède au moins trois traces.

**Indice de Jack :** vous devez utiliser COUNT, GROUP BY et HAVING. Le filtre HAVING s’applique après le regroupement.

La forme attendue est :

~~~sql
SELECT channel_id, COUNT(*) AS trace_count
FROM access_logs
GROUP BY channel_id
HAVING COUNT(*) >= 3;
~~~

Le résultat doit vous ramener vers le salon Orbite. Vous devez conserver son channel_id pour la suite.

## Dossier 3 — Le compte privilégié

Anthony possédait des droits élevés pour aider Kevin. Vous devez retrouver le privilège accordé, le salon concerné et la date de l’autorisation.

**Indice de Jack :** la table access_grants contient les autorisations. Ne confondez pas le propriétaire du compte avec l’auteur du vol.

## Dossier 4 — Les témoins

Lisa et Lydie sont des passantes ou des victimes. Elles n’ont pas volé le salon, mais leurs messages donnent deux éléments de la chronologie.

**Indice de Jack :** utilisez messages et filtrez sur le nom de l’auteur. Une seule jointure suffit pour relier un message à son salon ou à son auteur.

## Dossier 5 — La trace d’accès

Vous devez comparer les connexions d’Anthony avec les actions effectuées grâce à ses droits.

**Indice de Jack :** dans access_logs, comparez credential_owner_id et actor_id. Si ces identifiants ne désignent pas la même personne, l’accès a été utilisé par quelqu’un d’autre.

## Dossier 6 — Le faux témoignage et la preuve finale

Mickael a publié un message pour brouiller les pistes. Vous devez l’écarter, puis réunir trois informations :

1. le nom du salon disparu ;
2. le compte privilégié utilisé ;
3. le voleur.

Vous devez conserver cet ordre et produire la preuve finale au format :

~~~text
SALON|COMPTE|VOLEUR
~~~

**Indice de Jack :** le voleur est la personne indiquée par actor_id dans l’accès d’export du dossier. Anthony est le propriétaire du compte utilisé, pas le voleur.

## Validation

Quittez SQLite puis lancez :

~~~bash
python3 main.py --answer 'SALON|COMPTE|VOLEUR'
~~~

Une preuve incomplète vous renverra vers les indices. Une preuve correcte permettra de contacter Kevin.

> « Lisa et Lydie ont vu des morceaux de la vérité. Anthony avait la clé. Mickael a franchi la porte. » — Jack Query

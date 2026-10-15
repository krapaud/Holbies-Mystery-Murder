# Les dossiers de Jack Query

> « Kevin a perdu le salon Orbite. Mickael a volé son contenu. Mais il n’a pas forcé la porte : il a utilisé un accès qui appartenait à quelqu’un d’autre. À vous de retrouver les preuves. » — Jack Query

Vous devez enquêter dans l’ordre. Une requête ne doit utiliser qu’un seul JOIN. Si vous avez besoin d’une nouvelle relation, vous devez écrire une nouvelle requête.

## Dossier 1 — Le salon disparu

Kevin est la victime. Vous devez retrouver le salon qu’il avait créé et déterminer son état actuel.

**Indice de Jack :** commencez avec la table channels. Cherchez le salon dont le statut est hidden.

## Dossier 2 — Le compte privilégié

Anthony possédait des droits élevés pour aider Kevin. Vous devez retrouver le privilège accordé, le salon concerné et la date de l’autorisation.

**Indice de Jack :** la table access_grants contient les autorisations. Ne confondez pas le propriétaire du compte avec l’auteur du vol.

## Dossier 3 — Les témoins

Lisa et Lydie sont des passantes ou des victimes. Elles n’ont pas volé le salon, mais leurs messages donnent deux éléments de la chronologie.

**Indice de Jack :** utilisez messages et filtrez sur le nom de l’auteur. Une seule jointure suffit pour relier un message à son salon ou à son auteur.

## Dossier 4 — La trace d’accès

Vous devez comparer les connexions d’Anthony avec les actions effectuées grâce à ses droits.

**Indice de Jack :** dans access_logs, comparez credential_owner_id et actor_id. Si ces identifiants ne désignent pas la même personne, l’accès a été utilisé par quelqu’un d’autre.

## Dossier 5 — Le faux témoignage

Mickael a publié un message pour brouiller les pistes. Vous devez le comparer aux événements et aux journaux d’accès.

**Indice de Jack :** une fausse piste contient une action de renommage et le mot DECOY. Ne la confondez pas avec l’export du dossier.

## Dossier 6 — La preuve finale

Vous devez réunir trois informations :

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

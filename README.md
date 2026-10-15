# Opération Salon Fantôme

> « Si vous lisez ces lignes, vous savez déjà que le 🏕️ Campement 7 a été supprimé.
> Je m’appelle Jack Query. Votre mission n’est pas de retrouver le salon. Votre mission est de trouver le voleur. »

## Votre mission

Kevin, le maître des salons, vous prévient : le Campement 7 a été supprimé et son dossier confidentiel a été volé.

Vous connaissez donc la scène dès le début. Vous devez prouver :

1. quel compte privilégié a été compromis ;
2. qui a utilisé ce compte pour voler le dossier.

Les archives contiennent les salons suivants :

- 📡 La grande salle ;
- 🔥 Le Feu de camp ;
- 👐 Besoin d’aide ;
- 🏕️ Campement 1 ;
- 🏕️ Campement 2 ;
- 🏕️ Campement 3 ;
- 🏕️ Campement 7, le salon supprimé.

Plusieurs personnes apparaissent dans les archives. Certaines sont des témoins ou des victimes. Une autre personne possédait les privilèges nécessaires, tandis que l’auteur du vol a utilisé ces droits. À vous de reconstruire la chronologie sans vous fier à une seule déclaration.

## Avant d’entrer dans les archives

Vous devez disposer de Python 3, SQLite 3, d’un terminal et d’une équipe capable de partager le terminal de l’enquêteur.

Vous ne devez modifier aucun fichier SQL pendant la partie.

## Le premier pas

Vous devez vous placer à la racine du projet, puis lancer :

~~~bash
python3 main.py
~~~

Vous devez ensuite ouvrir la base :

~~~bash
sqlite3 database/game.db
~~~

Vous devez commencer par afficher les tables :

~~~sql
.tables
.schema
~~~

Vous devez travailler en équipe, noter les preuves et ne pas conclure à partir d’un seul message.

## Les dossiers de Jack Query

> « Vous savez déjà que le 🏕️ Campement 7 a été supprimé. Kevin veut autre chose : savoir qui a utilisé une clé légitime pour commettre le vol. » — Jack Query

Le salon supprimé n’est pas à retrouver. Vous devez identifier le compte privilégié compromis et le véritable voleur. Une requête ne doit utiliser qu’un seul JOIN.

### Dossier 1 — La scène connue

Le Campement 7 est le salon supprimé. Vous devez retrouver les traces qui s’y rapportent et noter son channel_id pour vos recherches.

**Indice de Jack :** le statut hidden confirme la scène, mais ne constitue pas la réponse. La question est : qui a pu agir dans ce salon ?

### Dossier 2 — Le pic d’activité

Vous devez comparer le volume d’accès enregistré pour chaque salon et repérer le groupe qui contient au moins trois traces.

Vous devez produire une requête qui regroupe les accès par channel_id, compte le nombre de traces et filtre les groupes après le regroupement.

**Indice de Jack :** utilisez une fonction d’agrégation pour compter, regroupez les lignes par salon, puis utilisez le filtre adapté aux résultats agrégés. Le Campement 7 doit apparaître avec quatre traces, mais d’autres salons contiennent aussi des accès isolés.

### Dossier 3 — Le compte privilégié

Vous devez identifier, dans access_grants, le compte qui possède le privilège manage sur le Campement 7 et noter son member_id.

**Indice de Jack :** la table access_grants contient les autorisations. Le propriétaire d’une clé n’est pas automatiquement le voleur.

### Dossier 4 — Les témoignages et la chronologie

Deux témoins ou victimes ont laissé plusieurs messages dans des salons différents. Les archives ont anonymisé leurs repères temporels avec les tags `TIMELINE-A` et `TIMELINE-B`.

Vous devez retrouver ces messages grâce à `evidence_tag`, identifier leurs auteurs avec une seule jointure, puis comparer `sent_at` avec les événements et les connexions enregistrées. Leurs déplacements permettent de vérifier ce qui est possible ou impossible.

Vous devez conserver les heures dans votre chronologie et noter quel témoignage confirme ou contredit chaque hypothèse.

**Indice de Jack :** commencez par les tags temporels, puis faites parler les auteurs. Un témoin ne prouve pas seul l’identité du voleur : il sert à valider la chronologie.

### Dossier 5 — L’identité derrière la clé

Vous devez comparer credential_owner_id et actor_id dans access_logs. Vérifiez aussi que l’action suspecte correspond bien à l’horaire de l’export, et distinguez les connexions normales des actions effectuées sur Campement 7.

- credential_owner_id désigne le compte dont les droits sont utilisés ;
- actor_id désigne la personne qui réalise l’action.

**Indice de Jack :** si les deux identifiants sont différents lors de l’export, le compte a été détourné. Une connexion légitime ailleurs ne prouve pas que son propriétaire a réalisé l’export.

### Dossier 6 — Le coupable

Vous devez identifier la personne indiquée par actor_id lors de l’action export du Campement 7. Croisez cette trace avec :

- le privilège accordé ;
- l’horaire de l’export et du masquage ;
- les témoignages ;
- l’action publiée ensuite pour brouiller les pistes.

Vous devez réunir au moins trois éléments indépendants avant de conclure.

Vous devez produire uniquement :

~~~text
COMPTE|VOLEUR
~~~

**Indice de Jack :** le propriétaire de la clé n’est pas celui qui l’a utilisée. Le message publié après le vol peut être une diversion.

## Validation finale

Quand vous pensez avoir identifié le compte compromis et le voleur, vous devez quitter SQLite et lancer :

~~~bash
python3 main.py --answer 'COMPTE|VOLEUR'
~~~

Remplacez la valeur par votre preuve complète, dans cet ordre. Une preuve correcte permettra de contacter Kevin.

> « Le salon a disparu, mais le voleur a laissé sa trace. » — Jack Query

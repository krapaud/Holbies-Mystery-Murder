# Opération Salon Fantôme

![Affiche de l’Opération Salon Fantôme](assets/operation-salon-fantome-discord.png)

> « Le 🏕️ Campement 7 a disparu avec le dossier confidentiel de Kevin. Vous savez ce qui manque. Découvrez qui s’en est emparé et comment. »
>
> Jack Query

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

Choisissez un enquêteur qui partage son terminal avec l’équipe. Relevez ensemble les heures, les lieux et les identifiants qui soutiennent chaque hypothèse.

## Avant d’entrer dans les archives

Vous devez disposer de Python 3, SQLite 3, d’un terminal et d’une équipe capable de partager le terminal de l’enquêteur.

Vous ne devez modifier aucun fichier SQL pendant la partie.

## Maintenance du kit de travail

Le dépôt conserve sa configuration du kit partagé dans `.workspace.toml`. Le workflow GitHub [`Update workspace kit`](.github/workflows/update-workspace-kit.yml) vérifie périodiquement la version disponible et propose une mise à jour dans une branche et une pull request dédiées vers `dev`. La mise à jour ne modifie pas directement `main` et ne doit pas être exécutée pendant une partie.

## Le premier pas

Vous devez vous placer à la racine du projet, puis lancer :

~~~bash
python3 main.py
~~~

La console d’enquête s’ouvre automatiquement. Vous devez commencer par afficher les tables et leur structure :

~~~sql
.tables
.schema
~~~

Vous devez terminer chaque requête SQL par un point-virgule. Une requête peut être saisie sur plusieurs lignes. La console affiche les résultats puis une remarque de Jack Query, y compris lorsque la recherche échoue ou ne retourne aucune ligne. Cette remarque vous aide à poursuivre sans livrer la réponse.

Vous pouvez afficher le schéma d’une seule table avec `.schema nom_de_table`, consulter l’aide avec `.help` et quitter avec `.exit`. Vous devez saisir chaque commande commençant par un point séparément. La console reconstruit une copie de travail ignorée par Git à chaque démarrage et n’autorise que les recherches `SELECT`, même si une requête tente d’attacher une autre base. Chaque requête peut relier au plus deux sources, quelle que soit la syntaxe de jointure utilisée. Vous ne devez modifier aucun fichier SQL ni les archives.

Vous devez travailler en équipe, noter les preuves et ne pas conclure à partir d’un seul message.

## Les dossiers de Jack Query

> « Chaque archive ne raconte qu’un morceau de l’histoire. Vérifiez les heures avant de croire les déclarations. »

Vous pouvez consulter toutes les archives, mais chaque requête doit contenir au maximum une jointure. La console refuse aussi les jointures implicites, afin que la limite reste la même quelle que soit la syntaxe SQL utilisée. Conservez vos résultats pour confronter les déclarations aux traces techniques.

### Dossier 1 : La scène connue

Retrouvez le Campement 7 dans les archives. Notez l’identifiant qui permet de le suivre dans les autres dossiers ainsi que son état actuel.

**Jack Query :** « Le salon a laissé des traces avant de disparaître. Commencez par établir son identité dans les archives. »

### Dossier 2 : Le pic d’activité

Comparez les traces techniques de connexion et d’action enregistrées pour chaque salon. Ne mélangez pas ces journaux avec les messages de discussion ou les événements : ils répondent à d’autres questions. Repérez le salon qui concentre une activité inhabituelle autour de l’incident.

Notez le volume observé et les heures concernées. Distinguez les passages ordinaires des actions qui ont pu toucher au dossier.

**Jack Query :** « Rassemblez les traces par salon et comparez leur nombre. Les archives vous laisseront filtrer les groupes après le comptage. »

### Dossier 3 : Le compte privilégié

Retrouvez qui disposait du niveau d’autorisation nécessaire sur le salon concerné. Notez son identité et l’heure à laquelle ce droit lui a été accordé.

**Jack Query :** « Les autorisations sont consignées séparément des membres. Reliez les deux archives pour mettre un nom sur l’identifiant. »

### Dossier 4 : Les témoignages et la chronologie

Retrouvez toutes les déclarations enregistrées autour de l’incident et rassemblez-les dans une seule chronologie. Les archives contiennent des déclarations utiles et d’autres qui n’apportent aucun renseignement sur le vol.

Associez chaque déclaration à son auteur avec au maximum une jointure. Comparez ensuite les heures et les lieux déclarés avec les autres traces.

Pour chaque témoin, notez ce qu’il a personnellement vu ou entendu, ce qu’il suppose et ce que les traces confirment. Une présence au bon endroit ne suffit pas à prouver qu’une personne a vu le vol.

Gardez une chronologie avec les heures, les lieux et les observations exploitables. Vous en aurez besoin pour vérifier les actions du dossier suivant.

**Jack Query :** « Les déclarations partagent un motif dans leurs repères. Servez-vous-en pour les retrouver, puis placez les messages sur une ligne du temps. Distinguez les faits observés des suppositions. »

### Dossier 5 : L’identité derrière la clé

Retrouvez les actions qui portent sur le dossier. Notez leurs heures et les identités qui leur sont associées, puis vérifiez quelle action a suivi.


**Jack Query :** « Les traces de l’export mentionnent plus d’une identité. Vérifiez le rôle de chacune avant d’accuser quelqu’un. »

### Dossier 6 : Le coupable

Formulez votre conclusion à partir de plusieurs traces indépendantes. Vérifiez :

- qui pouvait accéder au salon ;
- qui a déclenché les actions sur le dossier et à quel moment ;
- les déclarations compatibles avec cette chronologie ;
- le message publié après l’incident.

Vous devez réunir au moins trois éléments indépendants avant de conclure.

Les archives contiennent volontairement plusieurs exports légitimes ou parasites. L’événement de vol indique le constat de Kevin, mais pas directement l’identité de l’auteur. Vous devez donc relier le salon, le compte privilégié, l’action technique et son acteur avant de conclure.

Vous devez produire uniquement :

~~~text
COMPTE|VOLEUR
~~~

**Jack Query :** « Votre preuve finale contient deux noms, dans l’ordre compte utilisé puis auteur de l’action. Confirmez-les avec les heures, les autorisations et les témoignages. »

## Validation finale

Quand vous pensez avoir identifié le compte compromis et le voleur, vous devez quitter la console avec `.exit`, puis lancer :

~~~bash
python3 main.py --answer 'COMPTE|VOLEUR'
~~~

Remplacez la valeur par votre preuve complète, dans cet ordre. Une preuve correcte permettra de contacter Kevin.

> « Le salon a disparu, mais le voleur a laissé sa trace. » Jack Query.

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

Vous devez terminer chaque requête SQL par un point-virgule. Une requête peut être saisie sur plusieurs lignes. La console présente l’enquête dans un écran dédié et sépare visuellement les extraits d’archives, les erreurs et les réactions de Jack Query. Elle ajoute une palette de couleurs dans les terminaux compatibles, sans colorer les preuves SQL. Les couleurs sont désactivées lors d’une sortie redirigée ou si la variable d’environnement `NO_COLOR` est définie. Les résultats complets restent affichés, même lorsqu’une valeur dépasse la largeur du terminal. Jack Query réagit aux éléments réellement retournés : le salon masqué, le relevé agrégé, les autorisations, les déclarations, les journaux d’action et les messages tardifs. Une recherche vide ne lui fait pas conclure qu’une piste n’existe pas ; il vous prévient que les critères peuvent être trop stricts. Ses répliques font avancer la scène sans nommer le coupable.

Vous pouvez afficher le schéma d’une seule table avec `.schema nom_de_table`, consulter l’aide avec `.help`, annuler une requête multiligne inachevée avec `.cancel` et quitter avec `.exit`. Vous devez saisir chaque commande commençant par un point séparément. La console reconstruit une copie de travail ignorée par Git à chaque démarrage et n’autorise que les recherches `SELECT`, même si une requête tente d’attacher une autre base. Chaque requête peut relier au plus deux sources, quelle que soit la syntaxe de jointure utilisée. Vous ne devez modifier aucun fichier SQL ni les archives.

Vous devez travailler en équipe, noter les preuves et ne pas conclure à partir d’un seul message.

## Les dossiers de Jack Query

> « Chaque archive ne raconte qu’un morceau de l’histoire. Vérifiez les heures avant de croire les déclarations. »

Vous pouvez consulter toutes les archives, mais chaque requête doit contenir au maximum une jointure. La console refuse aussi les jointures implicites, afin que la limite reste la même quelle que soit la syntaxe SQL utilisée. Conservez vos résultats pour confronter les déclarations aux traces techniques.

### Dossier 1 : La scène connue

Retrouvez le Campement 7 dans les archives. Notez l’identifiant qui permet de le suivre dans les autres dossiers ainsi que son état actuel.

**Jack Query :** « Kevin m’avait prévenu pour le Campement 7. Au moins, nous savons où regarder ; les archives devraient garder une trace de son identité. »

### Dossier 2 : Comparer les traces

Comparez le nombre de traces techniques de connexion et d’action enregistrées pour les salons qui dépassent un même seuil d’activité. Ne mélangez pas ces journaux avec les messages de discussion ou les événements : ils répondent à d’autres questions. Repérez l’écart le plus marqué, puis reliez l’identifiant du salon aux archives de la scène.

Notez les volumes et les identifiants qui apparaissent. À ce stade, une concentration de traces désigne un lieu à examiner, pas une preuve de vol. Il faudra encore distinguer les connexions des actions et confronter les heures aux autres dossiers.

**Jack Query :** « Plusieurs salons franchissent votre seuil. Celui qui se détache attire mon attention, mais un relevé d’accès ne raconte pas ce qui s’est passé. Il nous faudra les heures et les actes. »

### Dossier 3 : Le compte privilégié

Retrouvez qui disposait du niveau d’autorisation nécessaire sur le salon concerné. Notez son identité et l’heure à laquelle ce droit lui a été accordé.

**Jack Query :** « Un droit de gestion a été accordé avant l’incident. Cela nous dit qui pouvait agir, pas qui l’a fait. Je garderais cette distinction en tête. »

### Dossier 4 : Les témoignages et la chronologie

Retrouvez toutes les déclarations enregistrées autour de l’incident et rassemblez-les dans une seule chronologie. Les archives contiennent des déclarations utiles et d’autres qui n’apportent aucun renseignement sur le vol.

Associez chaque déclaration à son auteur avec au maximum une jointure. Comparez ensuite les heures et les lieux déclarés avec les autres traces.

Pour chaque témoin, notez ce qu’il a personnellement vu ou entendu, ce qu’il suppose et ce que les traces confirment. Une présence au bon endroit ne suffit pas à prouver qu’une personne a vu le vol.

Gardez une chronologie avec les heures, les lieux et les observations exploitables. Vous en aurez besoin pour vérifier les actions du dossier suivant.

**Jack Query :** « J’entends des souvenirs, des hésitations, même des conversations sans rapport avec le vol. Une silhouette n’est pas un visage, un badge n’est pas une personne. »

### Dossier 5 : L’identité derrière la clé

Retrouvez les actions qui portent sur le dossier. Notez leurs heures et les identités qui leur sont associées, puis vérifiez quelle action a suivi.

**Jack Query :** « Voilà les gestes consignés autour du Campement 7 : les heures, les actions et les identifiants. Cette fois, les journaux parlent d’actes, pas de souvenirs. »

### Dossier 6 : Le coupable

Formulez votre conclusion à partir de plusieurs traces indépendantes. Vérifiez :

- qui pouvait accéder au salon ;
- qui a déclenché les actions sur le dossier et à quel moment ;
- ce que le journal des événements confirme sur la chronologie ;
- les déclarations compatibles avec cette chronologie ;
- le message publié après l’incident.

Vous devez réunir au moins trois éléments indépendants avant de conclure.

Vous devez produire uniquement :

~~~text
COMPTE|VOLEUR
~~~

**Jack Query :** « Ce message est arrivé après les faits. Je ne sais pas encore s’il éclaire l’affaire ou s’il cherche à l’embrouiller ; faisons-le parler avec les heures. »

## Validation finale

Quand vous pensez avoir identifié le compte compromis et le voleur, vous devez quitter la console avec `.exit`, puis lancer :

~~~bash
python3 main.py --answer 'COMPTE|VOLEUR'
~~~

Remplacez la valeur par votre preuve complète, dans cet ordre. Une preuve correcte permettra de contacter Kevin.

Après la recherche du compte associé, Jack Query murmure : « Le compte dont les droits ont servi apparaît dans le registre. Il me manque encore la personne qui a déclenché l’export. » Après la recherche de l’acteur, il ajoute : « J’ai le nom associé à l’action. Un nom seul ne suffit pas ; les droits, les heures et les déclarations doivent tenir ensemble. »

> « Le salon a disparu, mais le voleur a laissé sa trace. » Jack Query.

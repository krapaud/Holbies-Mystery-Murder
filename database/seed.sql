PRAGMA foreign_keys = ON;
BEGIN;

INSERT INTO channels VALUES
(1,'📡 La grande salle','voice','active','2026-10-14 08:00:00'),
(2,'🔥 Le Feu de camp','voice','active','2026-10-14 08:05:00'),
(3,'👐 Besoin d’aide','voice','active','2026-10-14 08:10:00'),
(4,'🏕️ Campement 1','voice','active','2026-10-14 08:15:00'),
(5,'🏕️ Campement 2','voice','active','2026-10-14 08:20:00'),
(6,'🏕️ Campement 3','voice','active','2026-10-14 08:25:00'),
(7,'🏕️ Campement 7','voice','hidden','2026-10-14 08:30:00');

INSERT INTO members (member_id, display_name, joined_at) VALUES
(1,'Kevin','2026-10-14 08:01:00'),
(2,'Anthony','2026-10-14 08:02:00'),
(3,'Mickael','2026-10-14 08:03:00'),
(4,'Lisa','2026-10-14 08:04:00'),
(5,'Lydie','2026-10-14 08:06:00');

INSERT INTO messages (message_id, channel_id, member_id, sent_at, body, evidence_tag) VALUES
(1,1,1,'2026-10-14 08:35:00','Le Campement 7 contient le dossier que je devais remettre a Kevin.','KEVIN'),
(2,3,4,'2026-10-14 08:39:00','J ai vu une silhouette quitter Besoin d aide avec un badge qui n etait pas le sien.','LISA'),
(3,2,5,'2026-10-14 08:42:00','Le badge utilise portait les droits d Anthony.','LYDIE'),
(4,1,1,'2026-10-14 08:46:00','Si le Campement 7 disparait, cherchez la trace du compte privilegie.','TRACE'),
(5,2,4,'2026-10-14 08:51:00','La personne portait un blouson avec une initiale M.','INITIAL'),
(6,3,5,'2026-10-14 08:54:00','Je n ai jamais vu Anthony quitter son poste ce matin-la.','TEMOIN'),
(7,1,3,'2026-10-14 08:58:00','Le dossier est a moi maintenant.','DECOY'),
(8,4,4,'2026-10-14 08:36:00','J ai croise quelqu un pres des campements avant mon passage au salon d aide.','LISA-TIME'),
(9,5,5,'2026-10-14 08:44:00','Le badge a ete utilise apres le passage de la personne autorisee.','LYDIE-TIME'),
(10,1,1,'2026-10-14 09:03:00','Le proprietaire du badge affirme ne pas avoir exporte le dossier.','KEVIN-FOLLOWUP');

INSERT INTO events (event_id, channel_id, member_id, event_type, occurred_at, details, evidence_tag) VALUES
(1,7,1,'create','2026-10-14 08:31:00','Kevin ouvre Campement 7 pour deposer le dossier.','START'),
(2,7,2,'permission','2026-10-14 08:32:00','Un membre recoit le privilege manage pour aider Kevin.','PRIV'),
(3,3,4,'join','2026-10-14 08:38:00','Une temoin entre dans Besoin d aide pour remettre un message.','LISA'),
(4,2,5,'join','2026-10-14 08:41:00','Une passante passe par Le Feu de camp et entend une alerte.','LYDIE'),
(5,7,3,'theft','2026-10-14 08:52:00','Le contenu de Campement 7 est exporte puis le salon est masque.','THEFT'),
(6,1,1,'archive','2026-10-14 08:53:00','Kevin constate que Campement 7 est devenu invisible.','HIDDEN'),
(7,1,3,'rename','2026-10-14 08:57:00','Un membre publie un faux message dans La grande salle.','DECOY'),
(8,4,4,'join','2026-10-14 08:35:30','Une membre rejoint Campement 1 avant de parler dans Besoin d aide.','LISA-TIME'),
(9,5,5,'join','2026-10-14 08:43:30','Une membre rejoint Campement 2 avant de rejoindre Le Feu de camp.','LYDIE-TIME'),
(10,1,1,'message','2026-10-14 09:03:00','Kevin ajoute un dernier témoignage après sa vérification.','KEVIN-FOLLOWUP');

INSERT INTO access_grants (grant_id, channel_id, member_id, privilege, granted_at, granted_by) VALUES
(1,7,2,'manage','2026-10-14 08:32:00',1),
(2,1,1,'read','2026-10-14 08:33:00',1),
(3,3,4,'read','2026-10-14 08:34:00',1),
(4,2,5,'read','2026-10-14 08:35:00',1);

INSERT INTO access_logs (log_id, channel_id, credential_owner_id, actor_id, occurred_at, action, device, details) VALUES
(1,7,2,2,'2026-10-14 08:32:30','login','poste-02','Le proprietaire ouvre sa session de gestion.'),
(2,7,2,3,'2026-10-14 08:51:00','export','poste-07','Export du dossier confidentiel avec les droits du proprietaire.'),
(3,7,2,3,'2026-10-14 08:52:00','archive','poste-07','Masquage de Campement 7 apres export.'),
(4,1,1,3,'2026-10-14 08:57:00','rename','poste-07','Publication du faux message dans La grande salle.'),
(5,7,2,2,'2026-10-14 09:02:00','login','poste-02','Le proprietaire revient et decouvre Campement 7 masque.'),
(6,3,4,4,'2026-10-14 08:37:30','login','poste-04','Une temoin ouvre une session de lecture.'),
(7,2,5,5,'2026-10-14 08:40:30','login','poste-05','Une passante ouvre une session de lecture.'),
(8,4,1,4,'2026-10-14 08:36:00','login','poste-04','Une session de lecture est ouverte sur un autre campement.'),
(9,5,1,5,'2026-10-14 08:44:30','login','poste-05','Une session de lecture est ouverte sur un autre campement.'),
(10,1,1,1,'2026-10-14 08:45:00','login','poste-01','Kevin consulte la grande salle.');

INSERT INTO clues (clue_id, message_id, event_id, clue_kind, dossier) VALUES
(1,1,1,'lead',1),
(2,4,2,'lead',2),
(3,3,2,'lead',3),
(4,2,3,'lead',4),
(5,5,5,'lead',5),
(6,7,7,'decoy',5),
(7,6,6,'lead',6),
(8,8,8,'lead',4),
(9,9,9,'lead',5),
(10,10,10,'lead',6);

COMMIT;

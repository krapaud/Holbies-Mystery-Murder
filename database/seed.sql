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

INSERT INTO members VALUES
(1,'Kevin','victim','2026-10-14 08:01:00'),
(2,'Anthony','privileged','2026-10-14 08:02:00'),
(3,'Mickael','thief','2026-10-14 08:03:00'),
(4,'Lisa','witness','2026-10-14 08:04:00'),
(5,'Lydie','witness','2026-10-14 08:06:00');

INSERT INTO messages (message_id, channel_id, member_id, sent_at, body, evidence_tag) VALUES
(1,1,1,'2026-10-14 08:35:00','Le Campement 7 contient le dossier que je devais remettre a Kevin.','KEVIN'),
(2,3,4,'2026-10-14 08:39:00','J ai vu une silhouette quitter Besoin d aide avec un badge qui n etait pas le sien.','LISA'),
(3,2,5,'2026-10-14 08:42:00','Le badge utilise portait les droits d Anthony.','LYDIE'),
(4,1,1,'2026-10-14 08:46:00','Si le Campement 7 disparait, cherchez la trace du compte privilegie.','TRACE'),
(5,2,4,'2026-10-14 08:51:00','La personne portait un blouson avec une initiale M.','INITIAL'),
(6,3,5,'2026-10-14 08:54:00','Je n ai jamais vu Anthony quitter son poste ce matin-la.','TEMOIN'),
(7,1,3,'2026-10-14 08:58:00','Le dossier est a moi maintenant.','DECOY');

INSERT INTO events (event_id, channel_id, member_id, event_type, occurred_at, details, evidence_tag) VALUES
(1,7,1,'create','2026-10-14 08:31:00','Kevin ouvre Campement 7 pour deposer le dossier.','START'),
(2,7,2,'permission','2026-10-14 08:32:00','Anthony recoit le privilege manage pour aider Kevin.','PRIV'),
(3,3,4,'join','2026-10-14 08:38:00','Lisa entre dans Besoin d aide pour remettre un message.','LISA'),
(4,2,5,'join','2026-10-14 08:41:00','Lydie passe par Le Feu de camp et entend une alerte.','LYDIE'),
(5,7,3,'theft','2026-10-14 08:52:00','Le contenu de Campement 7 est exporte puis le salon est masque.','THEFT'),
(6,1,1,'archive','2026-10-14 08:53:00','Kevin constate que Campement 7 est devenu invisible.','HIDDEN'),
(7,1,3,'rename','2026-10-14 08:57:00','Mickael publie un faux message dans La grande salle.','DECOY');

INSERT INTO access_grants (grant_id, channel_id, member_id, privilege, granted_at, granted_by) VALUES
(1,7,2,'manage','2026-10-14 08:32:00',1),
(2,1,1,'read','2026-10-14 08:33:00',1),
(3,3,4,'read','2026-10-14 08:34:00',1),
(4,2,5,'read','2026-10-14 08:35:00',1);

INSERT INTO access_logs (log_id, channel_id, credential_owner_id, actor_id, occurred_at, action, device, details) VALUES
(1,7,2,2,'2026-10-14 08:32:30','login','poste-02','Anthony ouvre sa session de gestion.'),
(2,7,2,3,'2026-10-14 08:51:00','export','poste-07','Export du dossier confidentiel avec les droits d Anthony.'),
(3,7,2,3,'2026-10-14 08:52:00','archive','poste-07','Masquage de Campement 7 apres export.'),
(4,1,1,3,'2026-10-14 08:57:00','rename','poste-07','Publication du faux message dans La grande salle.'),
(5,7,2,2,'2026-10-14 09:02:00','login','poste-02','Anthony revient et decouvre Campement 7 masque.');

INSERT INTO clues (clue_id, message_id, event_id, clue_kind, dossier) VALUES
(1,1,1,'lead',1),
(2,4,2,'lead',2),
(3,3,2,'lead',3),
(4,2,3,'lead',4),
(5,5,5,'lead',5),
(6,7,7,'decoy',5),
(7,6,6,'lead',6);

COMMIT;

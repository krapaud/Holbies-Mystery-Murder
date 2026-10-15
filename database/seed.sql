PRAGMA foreign_keys = ON;
BEGIN;

INSERT INTO channels VALUES
(1,'salon-orbite','voice','hidden','2026-10-14 08:00:00'),
(2,'quartier-general','text','active','2026-10-14 08:05:00'),
(3,'couloir-7','voice','active','2026-10-14 08:10:00'),
(4,'archives-securisees','text','archived','2026-10-14 08:15:00');

INSERT INTO members VALUES
(1,'Kevin','victim','2026-10-14 08:01:00'),
(2,'Anthony','privileged','2026-10-14 08:02:00'),
(3,'Mickael','thief','2026-10-14 08:03:00'),
(4,'Lisa','witness','2026-10-14 08:04:00'),
(5,'Lydie','witness','2026-10-14 08:06:00');

INSERT INTO messages (message_id, channel_id, member_id, sent_at, body, evidence_tag) VALUES
(1,2,1,'2026-10-14 08:20:00','Le salon Orbite contient le dossier que je devais remettre a Kevin.','KEVIN'),
(2,3,4,'2026-10-14 08:24:00','J ai vu une silhouette quitter le couloir avec un badge qui n etait pas le sien.','LISA'),
(3,2,5,'2026-10-14 08:27:00','Le badge utilise portait les droits d Anthony.','LYDIE'),
(4,4,1,'2026-10-14 08:31:00','Si le salon disparait, cherchez la trace du compte privilegie.','TRACE'),
(5,3,4,'2026-10-14 08:36:00','La personne portait un blouson avec une initiale M.','INITIAL'),
(6,2,5,'2026-10-14 08:42:00','Je n ai jamais vu Anthony quitter son poste ce matin-la.','TEMOIN'),
(7,4,3,'2026-10-14 08:45:00','Le dossier est a moi maintenant.','DECOY');

INSERT INTO events (event_id, channel_id, member_id, event_type, occurred_at, details, evidence_tag) VALUES
(1,1,1,'create','2026-10-14 08:01:00','Kevin ouvre le salon prive pour deposer le dossier.','START'),
(2,1,2,'permission','2026-10-14 08:05:00','Anthony recoit le privilege manage pour aider Kevin.','PRIV'),
(3,1,4,'join','2026-10-14 08:21:00','Lisa entre dans le salon pour remettre un message.','LISA'),
(4,1,5,'join','2026-10-14 08:23:00','Lydie passe devant le salon et entend une alerte.','LYDIE'),
(5,1,3,'theft','2026-10-14 08:39:00','Le contenu du salon est exporte puis le salon est masque.','THEFT'),
(6,1,1,'archive','2026-10-14 08:40:00','Kevin constate que le salon est devenu invisible.','HIDDEN'),
(7,2,3,'rename','2026-10-14 08:44:00','Mickael publie un faux message pour brouiller les pistes.','DECOY');

INSERT INTO access_grants (grant_id, channel_id, member_id, privilege, granted_at, granted_by) VALUES
(1,1,2,'manage','2026-10-14 08:05:00',1),
(2,2,1,'read','2026-10-14 08:06:00',1),
(3,3,4,'read','2026-10-14 08:10:00',1),
(4,4,5,'read','2026-10-14 08:15:00',1);

INSERT INTO access_logs (log_id, channel_id, credential_owner_id, actor_id, occurred_at, action, device, details) VALUES
(1,1,2,2,'2026-10-14 08:05:30','login','poste-02','Anthony ouvre sa session de gestion.'),
(2,1,2,3,'2026-10-14 08:38:00','export','poste-07','Export du dossier confidentiel avec les droits d Anthony.'),
(3,1,2,3,'2026-10-14 08:39:00','archive','poste-07','Masquage du salon apres export.'),
(4,2,1,3,'2026-10-14 08:44:00','rename','poste-07','Publication du faux message dans le quartier general.'),
(5,1,2,2,'2026-10-14 08:50:00','login','poste-02','Anthony revient et decouvre le salon masque.');

INSERT INTO clues (clue_id, message_id, event_id, clue_kind, dossier) VALUES
(1,1,1,'lead',1),
(2,4,2,'lead',2),
(3,3,2,'lead',3),
(4,2,3,'lead',4),
(5,5,5,'lead',5),
(6,7,7,'decoy',5),
(7,6,6,'lead',6);

COMMIT;

PRAGMA foreign_keys = ON;
BEGIN;

INSERT INTO channels VALUES
(1,'📡 La grande salle','voice','active','2026-10-14 08:00:00'),
(2,'🔥 Le Feu de camp','voice','active','2026-10-14 08:05:00'),
(3,'👐 Besoin d’aide','voice','active','2026-10-14 08:10:00'),
(4,'🏕️ Campement 1','voice','active','2026-10-14 08:15:00'),
(5,'🏕️ Campement 2','voice','active','2026-10-14 08:20:00'),
(6,'🏕️ Campement 3','voice','active','2026-10-14 08:25:00'),
(7,'🕳️ Salon fantôme','voice','hidden','2026-10-14 08:30:00');

INSERT INTO members (member_id, display_name, joined_at) VALUES
(1,'Kevin','2026-10-14 08:01:00'),
(2,'Anthony','2026-10-14 08:02:00'),
(3,'Mickael','2026-10-14 08:03:00'),
(4,'Lisa','2026-10-14 08:04:00'),
(5,'Lydie','2026-10-14 08:06:00');

INSERT INTO channel_name_history
  (history_id, channel_id, channel_name, valid_from, valid_until, changed_by, reason)
VALUES
(1,7,'🏕️ Campement 7','2026-10-14 08:30:00','2026-10-14 08:57:00',1,'Kevin ouvre le salon pour déposer le dossier.'),
(2,7,'🕳️ Salon fantôme','2026-10-14 08:57:00',NULL,3,'Le salon masqué est renommé après la disparition du dossier.');

INSERT INTO messages (message_id, channel_id, member_id, sent_at, body, evidence_tag) VALUES
(1,1,1,'2026-10-14 08:35:00','Le Campement 7 contient le dossier que je devais remettre a Kevin.','KEVIN'),
(2,3,4,'2026-10-14 08:39:00','J ai vu une silhouette quitter Besoin d aide avec un badge. Je n ai pas distingue son visage.','TEMOIN-02'),
(3,2,5,'2026-10-14 08:42:00','Une personne est passee au Feu de camp avec un badge semblable a celui d Anthony. Je ne sais pas qui c etait.','TEMOIN-03'),
(4,1,1,'2026-10-14 08:46:00','Si le Campement 7 disparait, cherchez la trace du compte privilegie.','TRACE'),
(5,3,4,'2026-10-14 08:51:00','J ai revu la meme silhouette. Elle a change de direction en voyant du monde, mais je n ai toujours pas distingue son visage.','TEMOIN-05'),
(6,2,5,'2026-10-14 08:54:00','Je n ai pas vu Anthony quitter son poste pendant mon passage. Je ne peux pas parler du reste de la matinee.','TEMOIN-06'),
(7,1,3,'2026-10-14 08:58:00','La recherche est terminée. Inutile de revenir sur le salon.','DECOY'),
(8,4,4,'2026-10-14 08:36:00','Je traversais Campement 1. Je n ai pas vu le visage de la personne pres du couloir.','TEMOIN-08'),
(9,5,5,'2026-10-14 08:44:00','Je suis passee par Campement 2 apres Le Feu de camp. Je n ai pas revu le porteur du badge.','TEMOIN-09'),
(10,1,1,'2026-10-14 09:03:00','Le proprietaire du badge affirme ne pas avoir exporte le dossier.','TEMOIN-10');

INSERT INTO events (event_id, channel_id, member_id, event_type, occurred_at, details, evidence_tag) VALUES
(1,7,1,'create','2026-10-14 08:31:00','Kevin ouvre Campement 7 pour deposer le dossier.','START'),
(2,7,2,'permission','2026-10-14 08:32:00','Un membre recoit le privilege manage pour aider Kevin.','PRIV'),
(3,3,4,'join','2026-10-14 08:38:00','Lisa rejoint Besoin d aide.','TEMOIN-02'),
(4,2,5,'join','2026-10-14 08:41:00','Lydie rejoint Le Feu de camp.','TEMOIN-03'),
(5,7,1,'theft','2026-10-14 08:52:00','Kevin constate qu une exportation a precede le masquage de Campement 7.','THEFT'),
(6,1,1,'archive','2026-10-14 08:53:00','Kevin constate que Campement 7 est devenu invisible.','HIDDEN'),
(7,7,3,'rename','2026-10-14 08:57:00','Le salon masqué est renommé Salon fantôme après la disparition du dossier.','DECOY'),
(8,4,4,'join','2026-10-14 08:35:30','Lisa rejoint Campement 1.','TEMOIN-08'),
(9,5,5,'join','2026-10-14 08:43:30','Lydie rejoint Campement 2 apres son passage au Feu de camp.','TEMOIN-09'),
(10,1,1,'join','2026-10-14 09:03:00','Kevin ajoute un dernier témoignage après sa vérification.','TEMOIN-10'),
(14,3,4,'join','2026-10-14 08:50:30','Lisa rejoint Besoin d aide.','TEMOIN-05');

INSERT INTO access_grants (grant_id, channel_id, member_id, privilege, granted_at, granted_by) VALUES
(1,7,2,'manage','2026-10-14 08:32:00',1),
(2,1,1,'read','2026-10-14 08:33:00',1),
(3,3,4,'read','2026-10-14 08:34:00',1),
(4,2,5,'read','2026-10-14 08:35:00',1);

INSERT INTO access_logs (log_id, channel_id, credential_owner_id, actor_id, occurred_at, action, device, details) VALUES
(1,7,2,2,'2026-10-14 08:32:30','login','poste-02','Le proprietaire ouvre sa session de gestion.'),
(2,7,2,3,'2026-10-14 08:51:00','export','poste-07','Export du dossier confidentiel avec les droits du proprietaire.'),
(3,7,2,3,'2026-10-14 08:52:00','archive','poste-07','Masquage de Campement 7 apres export.'),
(4,7,2,3,'2026-10-14 08:57:00','rename','poste-07','Le compte de Kevin renomme Campement 7 en Salon fantôme après son masquage.'),
(5,7,2,2,'2026-10-14 09:02:00','login','poste-02','Le proprietaire revient et decouvre Campement 7 masque.'),
(6,3,4,4,'2026-10-14 08:37:30','login','poste-04','Une temoin ouvre une session de lecture.'),
(7,2,5,5,'2026-10-14 08:40:30','login','poste-05','Une passante ouvre une session de lecture.'),
(8,4,4,4,'2026-10-14 08:36:00','login','poste-04','Lisa ouvre une session de lecture sur Campement 1.'),
(9,5,5,5,'2026-10-14 08:43:45','login','poste-05','Lydie ouvre une session de lecture sur Campement 2.'),
(10,1,1,1,'2026-10-14 08:45:00','login','poste-01','Kevin consulte la grande salle.'),
(17,7,4,4,'2026-10-14 08:44:30','export','poste-04','Lisa exporte une copie de travail de Campement 7 avant son masquage.'),
(14,3,4,4,'2026-10-14 08:50:30','login','poste-04','Lisa ouvre une session de lecture sur Besoin d aide.');

INSERT INTO members (member_id, display_name, joined_at) VALUES
(6,'Nora','2026-10-14 08:07:00'),
(7,'Samir','2026-10-14 08:08:00'),
(8,'Zoe','2026-10-14 08:09:00');

INSERT INTO messages (message_id, channel_id, member_id, sent_at, body, evidence_tag) VALUES
(11,4,6,'2026-10-14 08:33:00','Quelqu un sait si la salle de pause est encore ouverte ?','TEMOIN-11'),
(12,6,7,'2026-10-14 08:47:00','Quelqu un a vu mon chargeur ? Je crois l avoir laisse au Campement 3.','TEMOIN-12'),
(13,2,8,'2026-10-14 08:49:00','Quelqu un a vu mon carnet ? Je crois l avoir oublie dans un campement.','TEMOIN-13');

INSERT INTO events (event_id, channel_id, member_id, event_type, occurred_at, details, evidence_tag) VALUES
(11,4,6,'join','2026-10-14 08:32:30','Nora rejoint Campement 1.','TEMOIN-11'),
(12,6,7,'join','2026-10-14 08:46:30','Samir rejoint Campement 3.','TEMOIN-12'),
(13,2,8,'join','2026-10-14 08:48:30','Zoe rejoint Le Feu de camp.','TEMOIN-13');

INSERT INTO access_logs (log_id, channel_id, credential_owner_id, actor_id, occurred_at, action, device, details) VALUES
(11,4,6,6,'2026-10-14 08:32:30','login','poste-06','Nora ouvre une session de lecture sur Campement 1.'),
(12,6,7,7,'2026-10-14 08:46:30','login','poste-08','Samir ouvre une session de lecture sur Campement 3.'),
(13,2,8,8,'2026-10-14 08:48:30','login','poste-09','Zoe ouvre une session de lecture sur Le Feu de camp.');

INSERT INTO access_logs (log_id, channel_id, credential_owner_id, actor_id, occurred_at, action, device, details) VALUES
(15,3,4,4,'2026-10-14 08:49:30','export','poste-04','Lisa exporte un extrait de discussion pour préparer son témoignage.'),
(16,2,5,5,'2026-10-14 08:50:00','export','poste-05','Lydie exporte une copie de travail du Feu de camp.');

COMMIT;

PRAGMA foreign_keys = ON;
BEGIN;
INSERT INTO channels VALUES
(1,'salon-lanterne','voice','2026-10-12 18:10:00'),
(2,'archives-bleues','text','2026-10-12 18:12:00'),
(3,'couloir-7','voice','2026-10-13 08:20:00'),
(4,'quartier-general','text','2026-10-13 08:25:00'),
(5,'salle-des-cartes','voice','2026-10-13 09:00:00'),
(6,'salon-absent','voice','2026-10-13 09:15:00');
INSERT INTO members VALUES
(1,'Mina Vale','member','2026-10-12 18:11:00'),
(2,'Theo Moss','moderator','2026-10-12 18:11:30'),
(3,'Iris North','member','2026-10-12 18:13:00'),
(4,'Noa Reed','guest','2026-10-13 08:21:00'),
(5,'Sacha Bell','member','2026-10-13 08:26:00'),
(6,'Kevin','moderator','2026-10-13 08:30:00'),
(7,'Lio Park','member','2026-10-13 08:40:00');
INSERT INTO messages (message_id,channel_id,member_id,sent_at,body,evidence_piece) VALUES
(1,2,1,'2026-10-12 19:00:00','La lanterne a ete deplacee avant le silence.','br'),
(2,2,3,'2026-10-12 19:04:00','Le registre indique une porte qui ne figure plus sur le plan.','vei'),
(3,4,2,'2026-10-13 08:31:00','Ne suivez pas le premier nom dans la liste des invites.','mi'),
(4,4,5,'2026-10-13 08:37:00','J ai entendu une reponse apres la fermeture.','sil'),
(5,6,6,'2026-10-13 09:18:00','Le salon n est pas vide, il est seulement hors de vue.','iv'),
(6,1,7,'2026-10-13 09:20:00','Le vieux titre ressemble a une piste, mais ce n est qu un leurre.',NULL),
(7,5,4,'2026-10-13 09:25:00','La clef de secours etait dans la salle des cartes.',NULL);
INSERT INTO events (event_id,channel_id,member_id,event_type,occurred_at,details,evidence_piece) VALUES
(1,1,2,'rename','2026-10-12 18:55:00','nom remplace par un alias',NULL),
(2,2,1,'join','2026-10-12 18:59:00','connexion depuis le poste nord','ume'),
(3,2,3,'permission','2026-10-12 19:03:00','lecture temporaire accordee','lle'),
(4,4,2,'permission','2026-10-13 08:30:00','moderation active','nuit'),
(5,4,5,'join','2026-10-13 08:36:00','connexion depuis le poste est','lage'),
(6,6,6,'archive','2026-10-13 09:17:00','canal masque mais conserve','oire'),
(7,1,7,'leave','2026-10-13 09:19:00','deconnexion apres alerte',NULL),
(8,5,4,'join','2026-10-13 09:24:00','invite temporaire',NULL);
INSERT INTO clues (clue_id,message_id,event_id,fragment_order,clue_kind) VALUES
(1,1,2,1,'fragment'),(2,2,3,2,'fragment'),(3,3,4,3,'fragment'),
(4,4,5,4,'fragment'),(5,5,6,5,'fragment'),(6,6,7,NULL,'decoy'),(7,7,8,NULL,'decoy');
COMMIT;
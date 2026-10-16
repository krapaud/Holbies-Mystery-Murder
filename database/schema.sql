PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS clues;
DROP TABLE IF EXISTS access_logs;
DROP TABLE IF EXISTS access_grants;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS channels;

CREATE TABLE channels (
  channel_id INTEGER PRIMARY KEY,
  channel_name TEXT NOT NULL UNIQUE,
  channel_type TEXT NOT NULL CHECK (channel_type IN ('voice', 'text')),
  status TEXT NOT NULL CHECK (status IN ('active', 'hidden', 'archived')),
  created_at TEXT NOT NULL
);

CREATE TABLE members (
  member_id INTEGER PRIMARY KEY,
  display_name TEXT NOT NULL UNIQUE,
  joined_at TEXT NOT NULL
);

CREATE TABLE messages (
  message_id INTEGER PRIMARY KEY,
  channel_id INTEGER NOT NULL,
  member_id INTEGER NOT NULL,
  sent_at TEXT NOT NULL,
  body TEXT NOT NULL,
  evidence_tag TEXT,
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
  FOREIGN KEY (member_id) REFERENCES members(member_id)
);

CREATE TABLE events (
  event_id INTEGER PRIMARY KEY,
  channel_id INTEGER NOT NULL,
  member_id INTEGER NOT NULL,
  event_type TEXT NOT NULL CHECK (event_type IN ('create', 'rename', 'permission', 'join', 'leave', 'archive', 'theft')),
  occurred_at TEXT NOT NULL,
  details TEXT NOT NULL,
  evidence_tag TEXT,
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
  FOREIGN KEY (member_id) REFERENCES members(member_id)
);

CREATE TABLE access_grants (
  grant_id INTEGER PRIMARY KEY,
  channel_id INTEGER NOT NULL,
  member_id INTEGER NOT NULL,
  privilege TEXT NOT NULL CHECK (privilege IN ('read', 'moderate', 'manage')),
  granted_at TEXT NOT NULL,
  granted_by INTEGER NOT NULL,
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
  FOREIGN KEY (member_id) REFERENCES members(member_id),
  FOREIGN KEY (granted_by) REFERENCES members(member_id)
);

CREATE TABLE access_logs (
  log_id INTEGER PRIMARY KEY,
  channel_id INTEGER NOT NULL,
  credential_owner_id INTEGER NOT NULL,
  actor_id INTEGER NOT NULL,
  occurred_at TEXT NOT NULL,
  action TEXT NOT NULL CHECK (action IN ('login', 'rename', 'export', 'archive')),
  device TEXT NOT NULL,
  details TEXT NOT NULL,
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
  FOREIGN KEY (credential_owner_id) REFERENCES members(member_id),
  FOREIGN KEY (actor_id) REFERENCES members(member_id)
);

CREATE INDEX idx_access_logs_time ON access_logs(occurred_at);

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS clues;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS channels;

CREATE TABLE channels (
  channel_id INTEGER PRIMARY KEY,
  channel_name TEXT NOT NULL UNIQUE,
  channel_type TEXT NOT NULL CHECK (channel_type IN ('voice', 'text')),
  created_at TEXT NOT NULL
);
CREATE TABLE members (
  member_id INTEGER PRIMARY KEY,
  display_name TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL CHECK (role IN ('member', 'moderator', 'guest')),
  joined_at TEXT NOT NULL
);
CREATE TABLE messages (
  message_id INTEGER PRIMARY KEY,
  channel_id INTEGER NOT NULL,
  member_id INTEGER NOT NULL,
  sent_at TEXT NOT NULL,
  body TEXT NOT NULL,
  evidence_piece TEXT,
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
  FOREIGN KEY (member_id) REFERENCES members(member_id)
);
CREATE TABLE events (
  event_id INTEGER PRIMARY KEY,
  channel_id INTEGER NOT NULL,
  member_id INTEGER NOT NULL,
  event_type TEXT NOT NULL CHECK (event_type IN ('rename', 'permission', 'join', 'leave', 'archive')),
  occurred_at TEXT NOT NULL,
  details TEXT NOT NULL,
  evidence_piece TEXT,
  FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
  FOREIGN KEY (member_id) REFERENCES members(member_id)
);
CREATE TABLE clues (
  clue_id INTEGER PRIMARY KEY,
  message_id INTEGER NOT NULL,
  event_id INTEGER NOT NULL,
  fragment_order INTEGER,
  clue_kind TEXT NOT NULL CHECK (clue_kind IN ('fragment', 'decoy')),
  FOREIGN KEY (message_id) REFERENCES messages(message_id),
  FOREIGN KEY (event_id) REFERENCES events(event_id),
  CHECK ((clue_kind = 'fragment' AND fragment_order BETWEEN 1 AND 5)
      OR (clue_kind = 'decoy' AND fragment_order IS NULL))
);
CREATE INDEX idx_clues_kind_order ON clues(clue_kind, fragment_order);
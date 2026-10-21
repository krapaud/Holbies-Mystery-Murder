"""Tests for student game startup and database regeneration."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from main import build_database


class GameStartupTests(unittest.TestCase):
    def test_restarting_game_rebuilds_the_student_database(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "game.db"

            build_database(database)
            with sqlite3.connect(database) as connection:
                initial_count = connection.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
                connection.execute("DELETE FROM messages")
                connection.commit()

            build_database(database)

            with sqlite3.connect(database) as connection:
                restarted_count = connection.execute("SELECT COUNT(*) FROM messages").fetchone()[0]

        self.assertGreater(initial_count, 0)
        self.assertEqual(restarted_count, initial_count)

    def test_theft_event_requires_technical_trace_to_identify_actor(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "game.db"
            build_database(database)

            with sqlite3.connect(database) as connection:
                event_member = connection.execute(
                    "SELECT member_id FROM events WHERE event_type = 'theft' AND channel_id = 7"
                ).fetchone()[0]
                target_exports = connection.execute(
                    "SELECT COUNT(*) FROM access_logs WHERE action = 'export' AND channel_id = 7"
                ).fetchone()[0]
                all_exports = connection.execute(
                    "SELECT COUNT(*) FROM access_logs WHERE action = 'export'"
                ).fetchone()[0]

        self.assertEqual(event_member, 1)
        self.assertEqual(target_exports, 2)
        self.assertGreater(all_exports, target_exports)

    def test_campement_7_rename_keeps_identity_and_history(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "game.db"
            build_database(database)

            with sqlite3.connect(database) as connection:
                current_name = connection.execute(
                    "SELECT channel_name FROM channels WHERE channel_id = 7"
                ).fetchone()[0]
                names = connection.execute(
                    "SELECT channel_name FROM channel_name_history "
                    "WHERE channel_id = 7 ORDER BY valid_from"
                ).fetchall()
                rename = connection.execute(
                    "SELECT channel_id, credential_owner_id, actor_id, occurred_at FROM access_logs "
                    "WHERE action = 'rename'"
                ).fetchone()
                event_actor = connection.execute(
                    "SELECT member_id FROM events WHERE event_type = 'rename' AND channel_id = 7"
                ).fetchone()[0]

        self.assertEqual(current_name, "🕳️ Salon fantôme")
        self.assertEqual([row[0] for row in names], ["🏕️ Campement 7", "🕳️ Salon fantôme"])
        self.assertEqual(rename, (7, 2, 3, "2026-10-14 08:57:00"))
        self.assertEqual(event_actor, 2)

    def test_authorized_export_is_a_credible_decoy(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "game.db"
            build_database(database)

            with sqlite3.connect(database) as connection:
                decoy = connection.execute(
                    "SELECT actor_id FROM access_logs "
                    "WHERE channel_id = 7 AND action = 'export' AND actor_id = 4"
                ).fetchone()
                grant = connection.execute(
                    "SELECT privilege FROM access_grants "
                    "WHERE channel_id = 7 AND member_id = 4"
                ).fetchone()

        self.assertEqual(decoy, (4,))
        self.assertEqual(grant, ("read",))


if __name__ == "__main__":
    unittest.main()

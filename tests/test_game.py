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


if __name__ == "__main__":
    unittest.main()

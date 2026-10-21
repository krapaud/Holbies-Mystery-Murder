"""Contract tests for the student-facing SQL investigation console."""

import io
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from game.investigation_shell import _print_narration, run_sql_console


class InvestigationShellTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Path(self.temp_dir.name) / "investigation.sqlite3"
        with sqlite3.connect(self.database) as connection:
            connection.executescript(
                """
                CREATE TABLE alpha (id INTEGER PRIMARY KEY, label TEXT);
                CREATE TABLE beta (id INTEGER PRIMARY KEY, alpha_id INTEGER, note TEXT);
                CREATE TABLE gamma (id INTEGER PRIMARY KEY, beta_id INTEGER);
                CREATE TABLE messages (id INTEGER PRIMARY KEY, body TEXT);
                CREATE TABLE events (id INTEGER PRIMARY KEY, detail TEXT);
                INSERT INTO alpha VALUES (1, 'archive-readable');
                INSERT INTO beta VALUES (1, 1, 'second-archive');
                INSERT INTO gamma VALUES (1, 1);
                INSERT INTO messages VALUES (1, 'ordinary witness note');
                INSERT INTO events VALUES (1, 'ordinary timeline event');
                """
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_console(self, *commands):
        output = io.StringIO()
        with patch("builtins.input", side_effect=(*commands, ".exit")), redirect_stdout(output):
            status = run_sql_console(self.database)
        return status, output.getvalue()

    def test_allows_one_explicit_join_and_rejects_two(self):
        status, output = self.run_console(
            "SELECT alpha.label, beta.note FROM alpha "
            "JOIN beta ON beta.alpha_id = alpha.id;",
            "SELECT alpha.label FROM alpha "
            "JOIN beta ON beta.alpha_id = alpha.id "
            "JOIN gamma ON gamma.beta_id = beta.id;",
        )

        self.assertEqual(status, 0)
        self.assertIn("archive-readable", output)
        self.assertIn("une seule jointure au maximum", output)
        self.assertEqual(output.count("archive-readable"), 1)

    def test_rejects_two_implicit_join_separators(self):
        status, output = self.run_console(
            "SELECT a.label FROM alpha AS a, beta AS b, gamma AS g;"
        )

        self.assertEqual(status, 0)
        self.assertIn("une seule jointure au maximum", output)
        self.assertNotIn("archive-readable", output)

    def test_rejects_implicit_join_after_explicit_join_condition(self):
        status, output = self.run_console(
            "SELECT a.label FROM alpha AS a JOIN beta AS b "
            "ON b.alpha_id = a.id, gamma AS g;"
        )

        self.assertEqual(status, 0)
        self.assertIn("une seule jointure au maximum", output)
        self.assertNotIn("archive-readable", output)

    def test_counts_only_real_joins_not_text_in_comments_or_literals(self):
        status, output = self.run_console(
            "SELECT label, 'JOIN ghost' AS hint FROM alpha "
            "JOIN beta ON beta.alpha_id = alpha.id /* JOIN ignored */;"
        )

        self.assertEqual(status, 0)
        self.assertIn("archive-readable", output)
        self.assertNotIn("une seule jointure au maximum", output)

    def test_allows_one_join_inside_nested_select(self):
        status, output = self.run_console(
            "SELECT label FROM alpha WHERE id IN ("
            "SELECT beta.alpha_id FROM beta JOIN gamma ON gamma.beta_id = beta.id);"
        )

        self.assertEqual(status, 0)
        self.assertIn("archive-readable", output)
        self.assertNotIn("une seule jointure au maximum", output)

    def test_stops_counting_from_sources_at_join_conditions(self):
        status, output = self.run_console(
            "SELECT a.label FROM alpha AS a JOIN beta AS b "
            "ON b.alpha_id = a.id AND a.id = 1;"
        )

        self.assertEqual(status, 0)
        self.assertIn("archive-readable", output)
        self.assertNotIn("une seule jointure au maximum", output)

    def test_allows_a_readable_select(self):
        status, output = self.run_console("SELECT label FROM alpha WHERE id = 1;")

        self.assertEqual(status, 0)
        self.assertIn("archive-readable", output)
        self.assertIn("(1 ligne(s))", output)

    def test_refuses_attach_update_and_commit_through_file_alias(self):
        alias = str(self.database).replace("'", "''")
        status, output = self.run_console(
            f"ATTACH DATABASE '{alias}' AS mirror;",
            "UPDATE mirror.alpha SET label = 'tampered' WHERE id = 1;",
            "COMMIT;",
        )

        self.assertEqual(status, 0)
        self.assertGreaterEqual(output.count("Archive illisible :"), 3)
        self.assertIn("not authorized", output)
        with sqlite3.connect(self.database) as connection:
            label = connection.execute("SELECT label FROM alpha WHERE id = 1").fetchone()[0]
        self.assertEqual(label, "archive-readable")

    def test_empty_result_is_reported_without_crashing(self):
        status, output = self.run_console("SELECT label FROM alpha WHERE id = 99;")

        self.assertEqual(status, 0)
        self.assertIn("(0 ligne(s))", output)
        self.assertIn("Aucune ligne ne répond à ce filtre", output)

    def test_blank_line_then_exit_is_safe(self):
        status, output = self.run_console("", ".exit")

        self.assertEqual(status, 0)
        self.assertIn("Console d’enquête prête", output)

    def test_multi_table_query_gets_generic_cross_archive_narration(self):
        status, output = self.run_console(
            "SELECT messages.body, events.detail FROM messages "
            "JOIN events ON events.id = messages.id;"
        )

        self.assertEqual(status, 0)
        self.assertIn("Plusieurs archives se recoupent", output)
        self.assertNotIn("Une déclaration donne un point de vue", output)
        self.assertNotIn("Les événements fixent des faits dans le temps", output)

    def test_narration_uses_tables_read_not_table_words_in_sql(self):
        status, output = self.run_console(
            "SELECT detail FROM events WHERE 'messages' = 'messages';"
        )

        self.assertEqual(status, 0)
        self.assertIn("ordinary timeline event", output)
        self.assertIn("Les événements fixent des faits dans le temps", output)
        self.assertNotIn("Une déclaration donne un point de vue", output)

    def test_narration_is_yellow_when_color_is_forced(self):
        with patch.dict("os.environ", {"FORCE_COLOR": "1"}, clear=True):
            status, output = self.run_console("SELECT detail FROM events;")

        self.assertEqual(status, 0)
        self.assertIn("\033[33m[Jack Query] Les événements fixent des faits dans le temps.", output)
        self.assertIn("\033[0m", output)

    def test_no_color_environment_disables_forced_narration_color(self):
        with patch.dict("os.environ", {"FORCE_COLOR": "1", "NO_COLOR": "1"}, clear=True):
            status, output = self.run_console("SELECT detail FROM events;")

        self.assertEqual(status, 0)
        self.assertIn("[Jack Query] Les événements fixent des faits dans le temps.", output)
        self.assertNotIn("\033[33m", output)

    def test_tty_gets_color_without_force_color(self):
        class TTYStream(io.StringIO):
            def isatty(self):
                return True

        output = TTYStream()
        with patch.dict("os.environ", {}, clear=True):
            with patch("game.investigation_shell.sys.stdout", output):
                _print_narration("Dialogue de test")

        self.assertIn("\033[33m[Jack Query] Dialogue de test\033[0m", output.getvalue())

    def test_redirected_output_stays_plain_without_force_color(self):
        output = io.StringIO()
        with patch.dict("os.environ", {}, clear=True):
            with patch("game.investigation_shell.sys.stdout", output):
                _print_narration("Dialogue de test")

        self.assertEqual(output.getvalue(), "[Jack Query] Dialogue de test\n")

    def test_empty_no_color_does_not_disable_tty_color(self):
        class TTYStream(io.StringIO):
            def isatty(self):
                return True

        output = TTYStream()
        with patch.dict("os.environ", {"NO_COLOR": ""}, clear=True):
            with patch("game.investigation_shell.sys.stdout", output):
                _print_narration("Dialogue de test")

        self.assertIn("\033[33m[Jack Query] Dialogue de test\033[0m", output.getvalue())

    def test_force_color_zero_does_not_color_redirected_output(self):
        output = io.StringIO()
        with patch.dict("os.environ", {"FORCE_COLOR": "0"}, clear=True):
            with patch("game.investigation_shell.sys.stdout", output):
                _print_narration("Dialogue de test")

        self.assertEqual(output.getvalue(), "[Jack Query] Dialogue de test\n")


if __name__ == "__main__":
    unittest.main()

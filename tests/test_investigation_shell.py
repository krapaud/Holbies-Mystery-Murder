"""Contract tests for the student-facing SQL investigation console."""

import io
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game.investigation_shell import run_sql_console


class TerminalBuffer(io.StringIO):
    def isatty(self):
        return True


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
                CREATE TABLE messages (id INTEGER PRIMARY KEY, body TEXT, sent_at TEXT, evidence_tag TEXT);
                CREATE TABLE events (id INTEGER PRIMARY KEY, detail TEXT);
                CREATE TABLE channels (channel_id INTEGER PRIMARY KEY, channel_name TEXT);
                CREATE TABLE members (id INTEGER PRIMARY KEY, display_name TEXT);
                CREATE TABLE access_grants (id INTEGER PRIMARY KEY, member_id INTEGER, privilege TEXT);
                CREATE TABLE access_logs (id INTEGER PRIMARY KEY, action TEXT, credential_owner_id INTEGER, actor_id INTEGER, occurred_at TEXT);
                INSERT INTO alpha VALUES (1, 'archive-readable');
                INSERT INTO beta VALUES (1, 1, 'second-archive');
                INSERT INTO gamma VALUES (1, 1);
                INSERT INTO messages VALUES (1, 'ordinary witness note', '2026-01-01', 'TEMOIN-02');
                INSERT INTO messages VALUES (2, 'Le dossier est a moi maintenant.', '2026-01-02', 'DECOY');
                INSERT INTO events VALUES (1, 'ordinary timeline event');
                INSERT INTO channels VALUES (1, 'camp');
                INSERT INTO members VALUES (1, 'investigator');
                INSERT INTO access_grants VALUES (1, 1, 'manage');
                INSERT INTO access_logs VALUES (1, 'login', 1, 1, '2026-01-01');
                """
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_console(self, *commands, terminal=False, no_color=False, database=None):
        output = TerminalBuffer() if terminal else io.StringIO()
        environment = {"NO_COLOR": "1"} if no_color else {}
        self.prompts = []
        commands_to_return = iter((*commands, ".exit"))

        def receive_input(prompt=""):
            self.prompts.append(prompt)
            return next(commands_to_return)

        with patch("builtins.input", side_effect=receive_input), patch("sys.stdout", output), patch.dict(
            os.environ, environment, clear=True
        ):
            status = run_sql_console(database or self.database)
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
        self.assertIn("une seule jointure par requête", output)
        self.assertEqual(output.count("archive-readable"), 1)

    def test_rejects_two_implicit_join_separators(self):
        status, output = self.run_console(
            "SELECT a.label FROM alpha AS a, beta AS b, gamma AS g;"
        )

        self.assertEqual(status, 0)
        self.assertIn("une seule jointure par requête", output)
        self.assertNotIn("archive-readable", output)

    def test_rejects_implicit_join_after_explicit_join_condition(self):
        status, output = self.run_console(
            "SELECT a.label FROM alpha AS a JOIN beta AS b "
            "ON b.alpha_id = a.id, gamma AS g;"
        )

        self.assertEqual(status, 0)
        self.assertIn("une seule jointure par requête", output)
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
        self.assertIn("1 résultat(s) dans cette archive", output)

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
        self.assertIn("0 résultat(s) dans cette archive", output)
        self.assertIn("Je ne trouve rien de concluant", output)

    def test_blank_line_then_exit_is_safe(self):
        status, output = self.run_console("", ".exit")

        self.assertEqual(status, 0)
        self.assertIn("Le terminal est à vous", output)

    def test_multi_table_query_gets_generic_cross_archive_narration(self):
        status, output = self.run_console(
            "SELECT messages.body, events.detail FROM messages "
            "JOIN events ON events.id = messages.id;"
        )

        self.assertEqual(status, 0)
        self.assertIn("faire parler deux registres à la fois", output)
        self.assertNotIn("Une déclaration donne un point de vue", output)
        self.assertNotIn("Les événements fixent des faits dans le temps", output)

    def test_narration_uses_tables_read_not_table_words_in_sql(self):
        status, output = self.run_console(
            "SELECT detail FROM events WHERE 'messages' = 'messages';"
        )

        self.assertEqual(status, 0)
        self.assertIn("ordinary timeline event", output)
        self.assertIn("Une trace apparaît dans le journal des événements", output)
        self.assertNotIn("Une déclaration donne un point de vue", output)

    def test_each_archive_gets_a_reaction_about_its_result(self):
        status, output = self.run_console(
            "SELECT channel_name FROM channels;",
            "SELECT body FROM messages;",
            "SELECT detail FROM events;",
            "SELECT privilege FROM access_grants;",
            "SELECT action FROM access_logs;",
            "SELECT display_name FROM members;",
        )

        self.assertEqual(status, 0)
        self.assertIn("piste vient de remonter du registre des salons", output)
        self.assertIn("Les messages viennent de parler", output)
        self.assertIn("trace apparaît dans le journal des événements", output)
        self.assertIn("Un droit de gestion a été accordé avant l’incident", output)
        self.assertIn("journal vient de livrer une trace", output)
        self.assertIn("indice remonte du registre des membres", output)
        self.assertNotIn("Notez ce résultat", output)

    def test_empty_result_reaction_refers_to_the_archive_queried(self):
        status, output = self.run_console("SELECT body FROM messages WHERE id = 999;")

        self.assertEqual(status, 0)
        self.assertIn("Les témoins ne se sont pas tus", output)
        self.assertNotIn("Essayez autrement", output)

    def test_join_reaction_refers_to_the_clue_without_giving_away_the_answer(self):
        status, output = self.run_console(
            "SELECT members.display_name, access_grants.privilege "
            "FROM access_grants JOIN members "
            "ON members.id = access_grants.member_id;"
        )

        self.assertEqual(status, 0)
        self.assertIn("Le droit a maintenant un nom", output)
        self.assertNotIn("Mickael", output)

    def test_final_access_log_reaction_explains_the_two_identities_without_naming_them(self):
        status, output = self.run_console(
            "SELECT credential_owner_id, actor_id, action, occurred_at "
            "FROM access_logs ORDER BY occurred_at;"
        )

        self.assertEqual(status, 0)
        self.assertIn("Le journal met côte à côte le compte et l’acteur", output)
        self.assertNotIn("Mickael", output)
        self.assertNotIn("Anthony", output)

    def test_final_witness_reaction_focuses_on_statement_and_timing(self):
        status, output = self.run_console(
            "SELECT body, evidence_tag FROM messages "
            "WHERE evidence_tag = 'TEMOIN-02';"
        )

        self.assertEqual(status, 0)
        self.assertIn("J’entends des souvenirs, des hésitations", output)

    def test_decoy_message_is_not_narrated_as_a_witness_statement(self):
        status, output = self.run_console(
            "SELECT body, evidence_tag FROM messages "
            "WHERE evidence_tag = 'DECOY';"
        )

        self.assertEqual(status, 0)
        self.assertIn("Ce message est arrivé après les faits", output)
        self.assertNotIn("témoignage", output)

    def test_last_case_queries_get_contextual_jack_reactions_on_real_seed(self):
        game_database = Path(self.temp_dir.name) / "real-game.sqlite3"
        root = Path(__file__).resolve().parents[1]
        with sqlite3.connect(game_database) as connection:
            connection.executescript((root / "database/schema.sql").read_text())
            connection.executescript((root / "database/seed.sql").read_text())
            self.assertEqual(
                connection.execute(
                    "SELECT channel_id, COUNT(*) FROM access_logs "
                    "GROUP BY channel_id HAVING COUNT(*) >= 2 "
                    "ORDER BY COUNT(*) DESC, channel_id;"
                ).fetchall(),
                [(7, 4), (1, 2), (2, 2), (3, 2), (4, 2)],
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM messages WHERE evidence_tag LIKE 'TEMOIN-%';"
                ).fetchone()[0],
                10,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT sent_at FROM messages WHERE evidence_tag = 'DECOY';"
                ).fetchone()[0],
                "2026-10-14 08:58:00",
            )
            self.assertEqual(
                connection.execute(
                    "SELECT occurred_at FROM events WHERE event_type = 'theft' AND channel_id = 7;"
                ).fetchone()[0],
                "2026-10-14 08:52:00",
            )

        status, output = self.run_console(
            "SELECT channel_id, channel_name, status FROM channels WHERE status != 'active';",
            "SELECT channel_id, COUNT(*) AS trace_count FROM access_logs "
            "GROUP BY channel_id HAVING COUNT(*) >= 2 "
            "ORDER BY trace_count DESC, channel_id;",
            "SELECT member_id, channel_id, privilege, granted_at FROM access_grants "
            "WHERE privilege = 'manage' AND channel_id = 7;",
            "SELECT m.display_name, g.privilege, g.channel_id, g.granted_at "
            "FROM access_grants AS g JOIN members AS m ON m.member_id = g.member_id "
            "WHERE g.privilege = 'manage' AND g.channel_id = 7;",
            "SELECT message_id, channel_id, member_id, sent_at, body, evidence_tag "
            "FROM messages WHERE evidence_tag LIKE 'TEMOIN-%' ORDER BY sent_at;",
            "SELECT m.display_name, msg.sent_at, msg.body, msg.evidence_tag "
            "FROM messages AS msg JOIN members AS m ON m.member_id = msg.member_id "
            "WHERE msg.evidence_tag LIKE 'TEMOIN-%' ORDER BY msg.sent_at;",
            "SELECT credential_owner_id, actor_id, action, occurred_at, device, details "
            "FROM access_logs WHERE channel_id = 7 ORDER BY occurred_at;",
            "SELECT a.action, a.occurred_at, m.display_name AS actor "
            "FROM access_logs AS a JOIN members AS m ON m.member_id = a.actor_id "
            "WHERE a.channel_id = 7 AND a.action IN ('export', 'archive') "
            "ORDER BY a.occurred_at;",
            "SELECT member_id, sent_at, body, evidence_tag FROM messages "
            "WHERE evidence_tag = 'DECOY';",
            "SELECT event_type, occurred_at, details FROM events "
            "WHERE channel_id = 7 ORDER BY occurred_at;",
            "SELECT m.display_name AS credential_owner FROM access_logs AS a "
            "JOIN members AS m ON m.member_id = a.credential_owner_id "
            "WHERE a.channel_id = 7 AND a.action = 'export';",
            "SELECT m.display_name AS actor FROM access_logs AS a "
            "JOIN members AS m ON m.member_id = a.actor_id "
            "WHERE a.channel_id = 7 AND a.action = 'export';",
            database=game_database,
        )

        self.assertEqual(status, 0)
        jack_lines = [line for line in output.splitlines() if line.startswith("[Jack Query]")]
        reactions = [line.split("] ", 1)[1] for line in jack_lines[1:]]
        expected_reactions = [
            "Kevin m’avait prévenu pour le Campement 7.",
            "Plusieurs salons franchissent votre seuil.",
            "Un droit de gestion a été accordé avant l’incident.",
            "Le droit a maintenant un nom.",
            "J’entends des souvenirs, des hésitations",
            "Les voix ont maintenant un nom, mais pas un visage.",
            "Voilà les gestes consignés autour du Campement 7",
            "J’ai le nom associé à l’action.",
            "Ce message est arrivé après les faits.",
            "Ces repères fixent la chronologie du Campement 7.",
            "Le compte dont les droits ont servi apparaît dans le registre.",
            "J’ai le nom associé à l’action.",
        ]
        self.assertEqual(len(reactions), len(expected_reactions))
        for index, expected in enumerate(expected_reactions):
            with self.subTest(query_number=index + 1):
                self.assertIn(expected, reactions[index])
        self.assertFalse(any("Mickael" in line or "Anthony" in line for line in jack_lines))

    def test_results_use_the_case_file_layout_without_losing_long_evidence(self):
        long_evidence = "témoignage confidentiel " * 12
        with sqlite3.connect(self.database) as connection:
            connection.execute("INSERT INTO messages (body) VALUES (?)", (long_evidence,))

        status, output = self.run_console("SELECT body FROM messages WHERE id = 3;")

        self.assertEqual(status, 0)
        self.assertIn("LES ARCHIVES DU CAMPEMENT 7", output)
        self.assertIn("EXTRAIT DES ARCHIVES", output)
        self.assertIn(long_evidence, output)

    def test_colors_are_used_in_a_terminal(self):
        status, output = self.run_console("SELECT label FROM alpha;", terminal=True)

        self.assertEqual(status, 0)
        self.assertIn("\033[96;1m", output)
        self.assertIn("\033[95;1m", output)
        self.assertIn("\033[0m", output)

    def test_colors_are_disabled_when_output_is_redirected(self):
        status, output = self.run_console("SELECT label FROM alpha;")

        self.assertEqual(status, 0)
        self.assertNotIn("\033[", output)

    def test_no_color_environment_variable_disables_terminal_colors(self):
        status, output = self.run_console(
            "SELECT label FROM alpha;", terminal=True, no_color=True
        )

        self.assertEqual(status, 0)
        self.assertNotIn("\033[", output)

    def test_colored_readline_prompt_marks_ansi_sequences_as_nonprinting(self):
        status, _output = self.run_console(".exit", terminal=True)

        self.assertEqual(status, 0)
        prompt = self.prompts[0]
        if "\033[" in prompt:
            self.assertTrue(prompt.startswith("\001"))
            self.assertTrue(prompt.endswith("\002"))
            self.assertEqual(prompt.count("\001"), prompt.count("\002"))
            self.assertLess(prompt.index("\002"), prompt.index("sql>"))
            self.assertGreater(prompt.index("\001", prompt.index("sql>")), prompt.index("sql>"))

    def test_incomplete_query_can_be_cancelled_and_console_continues(self):
        status, output = self.run_console(
            "SELECT label FROM alpha", ".cancel", "SELECT label FROM alpha;"
        )

        self.assertEqual(status, 0)
        self.assertIn("Requête abandonnée", output)
        self.assertIn("archive-readable", output)
        self.assertEqual(output.count("archive-readable"), 1)
        self.assertTrue(any(".cancel annule" in prompt for prompt in self.prompts))

    def test_commands_other_than_cancel_cannot_interrupt_pending_sql(self):
        status, output = self.run_console(
            "SELECT label FROM alpha", ".tables", ".cancel", "SELECT label FROM alpha;"
        )

        self.assertEqual(status, 0)
        self.assertIn("Terminez-la ou utilisez .cancel", output)
        self.assertNotIn("access_grants  access_logs", output)
        self.assertIn("archive-readable", output)


if __name__ == "__main__":
    unittest.main()

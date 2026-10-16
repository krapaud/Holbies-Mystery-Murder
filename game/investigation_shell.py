"""Console SQL en lecture seule avec les réactions de Jack Query."""

import os
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import Optional

try:
    import readline
except ImportError:  # pragma: no cover - readline is not available on every platform
    readline = None


TABLE_REACTIONS = {
    "channels": "« Une piste vient de remonter du registre des salons. Je la garde au dossier. »",
    "messages": "« Les messages viennent de parler. Ces mots devront tenir face aux heures. »",
    "events": "« Une trace apparaît dans le journal des événements. Elle prendra tout son sens dans la chronologie. »",
    "access_grants": "« Le registre vient de livrer un indice sur les autorisations. Reste à comprendre ce qu’on en a fait. »",
    "access_logs": "« Le journal vient de livrer une trace. L’heure et les identifiants pourraient compter. »",
    "members": "« Un indice remonte du registre des membres. Chaque nom devra être recoupé avant de conclure. »",
}
GENERIC_REACTION = "« Une pièce de plus au dossier. Je ne sais pas encore ce qu’elle vaut, mais je la garde. »"
MULTI_ARCHIVE_REACTION = "« Vous venez de faire parler deux registres à la fois. Certains détails s’éclairent, mais il reste des zones d’ombre. »"
EMPTY_REACTIONS = {
    "channels": "« Rien ne remonte avec ces critères. Le salon a peut-être échappé au filtre ; je ne conclurais pas qu’il n’existe pas. »",
    "messages": "« Aucun message ne remonte avec cette recherche. Les témoins ne se sont pas tus pour autant ; le filtre est peut-être trop étroit. »",
    "events": "« Je n’obtiens aucune trace pour ces critères. La chronologie n’est pas forcément vide ; il faut vérifier la recherche. »",
    "access_grants": "« Aucun droit ne ressort ici. Cela ne prouve pas qu’il n’y en a pas ; vérifions les critères de recherche. »",
    "access_logs": "« Le journal ne renvoie aucune ligne. Je ne peux pas en déduire qu’il n’y a pas eu d’accès : peut-être cherchons-nous au mauvais endroit. »",
    "members": "« Aucun nom ne remonte avec ces critères. La liste n’est pas muette, notre recherche l’est peut-être trop. »",
}
PAIRED_ARCHIVE_REACTIONS = {
    frozenset(("access_grants", "members")): "« Le droit a maintenant un nom. Je sais qui détenait la clé, pas encore qui s’en est servi. »",
    frozenset(("access_logs", "members")): "« L’identifiant a retrouvé un nom. Le journal nous donne une action et une heure, mais pas encore toute l’histoire. »",
    frozenset(("messages", "members")): "« Cette voix a un nom, maintenant. Reste à savoir ce qu’elle a vraiment vu, et ce que les heures confirment. »",
}
APP_NAME = "LES ARCHIVES DU CAMPEMENT 7"
APP_SUBTITLE = "Console d’enquête | Accès en lecture seule"
FROM_CLAUSE_END = {
    "WHERE", "GROUP", "HAVING", "ORDER", "LIMIT", "WINDOW", "UNION",
    "EXCEPT", "INTERSECT", "RETURNING", "QUALIFY",
}
ANSI_RESET = "\033[0m"
ANSI_COLORS = {
    "cyan": "96",
    "green": "92",
    "magenta": "95",
    "red": "91",
    "muted": "90",
    "bold": "1",
}


def _sql_tokens(sql: str) -> list[tuple[str, int]]:
    """Tokenise les mots-clés utiles sans confondre chaînes, commentaires et identifiants cités."""
    tokens = []
    index = 0
    depth = 0
    length = len(sql)
    while index < length:
        char = sql[index]
        if char.isspace():
            index += 1
            continue
        if sql.startswith("--", index):
            end = sql.find("\n", index)
            index = length if end == -1 else end + 1
            continue
        if sql.startswith("/*", index):
            end = sql.find("*/", index + 2)
            index = length if end == -1 else end + 2
            continue
        if char in "'\"`[":
            closing = "]" if char == "[" else char
            index += 1
            while index < length:
                if sql[index] == closing:
                    if closing != "]" and index + 1 < length and sql[index + 1] == closing:
                        index += 2
                        continue
                    index += 1
                    break
                index += 1
            tokens.append(("<quoted>", depth))
            continue
        if char == "(":
            tokens.append((char, depth))
            depth += 1
            index += 1
            continue
        if char == ")":
            depth = max(0, depth - 1)
            tokens.append((char, depth))
            index += 1
            continue
        if char in ",;":
            tokens.append((char, depth))
            index += 1
            continue
        if char.isalpha() or char == "_":
            end = index + 1
            while end < length and (sql[end].isalnum() or sql[end] in "_$"):
                end += 1
            tokens.append((sql[index:end].upper(), depth))
            index = end
            continue
        index += 1
    return tokens


def _join_count(sql: str) -> int:
    """Compte les jointures explicites et les sources séparées par virgules dans les FROM."""
    tokens = _sql_tokens(sql)
    count = 0
    count += sum(1 for token, _depth in tokens if token == "JOIN")
    for position, (token, depth) in enumerate(tokens):
        if token != "FROM":
            continue
        for source, source_depth in tokens[position + 1:]:
            if source_depth < depth:
                break
            if source_depth > depth:
                continue
            if source == ";" or source in FROM_CLAUSE_END:
                break
            if source == ",":
                count += 1
        # JOIN tokens in nested FROM clauses are counted by their own FROM scan.
    return count


def _read_only_authorizer(read_tables: set[str]):
    allowed = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION,
        sqlite3.SQLITE_RECURSIVE,
    }

    def authorize(action: int, arg1: str, _arg2: str, _database: str, _source: str) -> int:
        if action == sqlite3.SQLITE_READ and arg1:
            read_tables.add(arg1.lower())
        return sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY

    return authorize


def _narration(
    read_tables: set[str],
    rows: list[tuple],
    columns: list[str],
    sql: str = "",
) -> str:
    if not rows:
        for table, reaction in EMPTY_REACTIONS.items():
            if table in read_tables:
                return reaction
        return "« Je ne trouve rien de concluant dans cette recherche. L’archive ne parle pas encore. »"
    normalized_sql = " ".join(sql.lower().split())
    records = [dict(zip(columns, row)) for row in rows]
    values = {str(value).lower() for row in rows for value in row if value is not None}
    if "channels" in read_tables and any(
        row.get("status") == "hidden" and row.get("channel_name") for row in records
    ):
        return "« Kevin m’avait prévenu pour le Campement 7. Au moins, nous savons où regarder ; les archives devraient garder une trace de son identité. »"
    if "access_logs" in read_tables and "having" in normalized_sql and "count(" in normalized_sql:
        return "« Plusieurs salons franchissent votre seuil. Celui qui se détache attire mon attention, mais un relevé d’accès ne raconte pas ce qui s’est passé. Il nous faudra les heures et les actes. »"
    if "access_grants" in read_tables and "manage" in values:
        if "members" in read_tables:
            return "« Le droit a maintenant un nom. Je sais qui détenait la clé, pas encore qui s’en est servi. »"
        return "« Un droit de gestion a été accordé avant l’incident. Cela nous dit qui pouvait agir, pas qui l’a fait. Je garderais cette distinction en tête. »"
    if "events" in read_tables and "channel_id = 7" in normalized_sql and any(
        row.get("event_type") == "theft" for row in records
    ):
        return "« Ces repères fixent la chronologie du Campement 7. Les journaux disent quelles actions ont été enregistrées ; ces événements racontent ce qui se passait autour. »"
    if "messages" in read_tables and "evidence_tag" in columns:
        tags = {
            str(row.get("evidence_tag")).lower()
            for row in records
            if row.get("evidence_tag") is not None
        }
        if tags == {"temoin-10"}:
            return "« Cette déclaration arrive après les actions. Elle rapporte ce qui a été vérifié ensuite, pas ce qui s’est passé au moment du vol. »"
        if tags == {"decoy"}:
            return "« Ce message est arrivé après les faits. Je ne sais pas encore s’il éclaire l’affaire ou s’il cherche à l’embrouiller ; faisons-le parler avec les heures. »"
        if tags and all(tag.startswith("temoin-") for tag in tags):
            if "members" in read_tables:
                return "« Les voix ont maintenant un nom, mais pas un visage. Une silhouette n’est pas une personne reconnue ; les heures et les lieux restent à confronter. »"
            return "« J’entends des souvenirs, des hésitations, même des conversations sans rapport avec le vol. Une silhouette n’est pas un visage, un badge n’est pas une personne. »"
    if "access_logs" in read_tables:
        if "credential_owner" in columns:
            return "« Le compte dont les droits ont servi apparaît dans le registre. Il me manque encore la personne qui a déclenché l’export. »"
        if "actor" in columns and "members" in read_tables:
            return "« J’ai le nom associé à l’action. Un nom seul ne suffit pas ; les droits, les heures et les déclarations doivent tenir ensemble. »"
        if "credential_owner_id" in columns and "actor_id" in columns:
            if any(
                row.get("action") in {"export", "archive"}
                and row.get("credential_owner_id") != row.get("actor_id")
                for row in records
            ):
                return "« Voilà les gestes consignés autour du Campement 7 : les heures, les actions et les identifiants. Cette fois, les journaux parlent d’actes, pas de souvenirs. »"
            return "« Le journal met côte à côte le compte et l’acteur. Sans isoler la scène qui nous occupe, je ne sais pas encore quelle trace retenir. »"
    for pair, reaction in PAIRED_ARCHIVE_REACTIONS.items():
        if pair.issubset(read_tables):
            return reaction
    if len(read_tables) > 1:
        return MULTI_ARCHIVE_REACTION
    matching_reactions = [
        reaction
        for table, reaction in TABLE_REACTIONS.items()
        if table in read_tables
    ]
    if len(matching_reactions) > 1:
        return MULTI_ARCHIVE_REACTION
    if matching_reactions:
        return matching_reactions[0]
    return GENERIC_REACTION


def _terminal_width() -> int:
    """Retourne une largeur raisonnable, y compris dans un terminal étroit."""
    return max(20, min(shutil.get_terminal_size(fallback=(80, 24)).columns, 100))


def _colors_enabled() -> bool:
    """N'émet de couleur que dans un terminal, sauf demande explicite NO_COLOR."""
    return (
        "NO_COLOR" not in os.environ
        and os.environ.get("TERM") != "dumb"
        and sys.stdout.isatty()
    )


def _style(text: str, *styles: str) -> str:
    if not _colors_enabled():
        return text
    codes = ";".join(ANSI_COLORS[style] for style in styles)
    return f"\033[{codes}m{text}{ANSI_RESET}"


def _input_prompt(text: str, *styles: str) -> str:
    """Colorise le prompt sans fausser le curseur GNU Readline."""
    if readline is None or not _colors_enabled():
        return text
    codes = ";".join(ANSI_COLORS[style] for style in styles)
    color_start = f"\033[{codes}m"
    # Readline compte autrement les caractères invisibles et redessine alors
    # mal la ligne lors de l’édition, de l’historique ou d’une saisie multiligne.
    return f"\001{color_start}\002{text}\001{ANSI_RESET}\002"


def _print_jack(message: str) -> None:
    print(f"{_style('[Jack Query]', 'magenta', 'bold')} {message}")


def _print_rule(character: str = "-", color: str = "muted") -> None:
    print(_style(_rule(character), color))


def _rule(character: str = "-") -> str:
    return character * _terminal_width()


def _print_banner() -> None:
    width = _terminal_width()
    print()
    _print_rule("=", "cyan")
    print(_style(APP_NAME.center(width), "cyan", "bold"))
    print(_style(APP_SUBTITLE.center(width), "muted"))
    _print_rule("=", "cyan")
    _print_jack("« Le terminal est à vous. Terminez chaque requête par ;, ou appelez-moi avec .help. »")
    print()


def _format_rows(cursor: sqlite3.Cursor, rows: list[tuple]) -> None:
    names = [item[0] for item in cursor.description or ()]
    if not names:
        print()
        _print_rule()
        print(_style("  ARCHIVE MISE À JOUR", "green", "bold"))
        _print_rule()
        return
    rendered = [["NULL" if value is None else str(value) for value in row] for row in rows]
    widths = [max([len(names[i])] + [len(row[i]) for row in rendered]) for i in range(len(names))]
    available_width = _terminal_width() - 4
    print()
    _print_rule()
    print(_style("  EXTRAIT DES ARCHIVES", "cyan", "bold"))
    _print_rule()
    if sum(widths) + 3 * (len(widths) - 1) > available_width:
        for row_number, row in enumerate(rendered, start=1):
            print(f"  Dossier {row_number}")
            for name, value in zip(names, row):
                print(f"    {name}: {value}")
    else:
        print(_style("  " + " | ".join(name.ljust(widths[i]) for i, name in enumerate(names)), "cyan", "bold"))
        print(_style("-+-".join("-" * width for width in widths), "muted"))
        for row in rendered:
            print("  " + " | ".join(value.ljust(widths[i]) for i, value in enumerate(row)))
    _print_rule()
    print(_style(f"  {len(rows)} résultat(s) dans cette archive", "green"))


def _show_tables(connection: sqlite3.Connection) -> None:
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    print("  ".join(row[0] for row in rows))
    _print_jack("« Les archives sont ouvertes. Je vous accompagne, mais c’est à vous de recoller les morceaux. »")


def _show_schema(connection: sqlite3.Connection, table: Optional[str] = None) -> None:
    names = [row[0] for row in connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )]
    if table:
        if table not in names:
            print("Table inconnue. Utilisez .tables pour consulter les archives disponibles.")
            return
        names = [table]
    for name in names:
        safe_name = name.replace('"', '""')
        row = connection.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = ?", (name,)
        ).fetchone()
        if row and row[0]:
            print(row[0] + ";")
        for index in connection.execute(f'PRAGMA index_list("{safe_name}")'):
            index_name = index[1].replace('"', '""')
            result = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'index' AND name = ?", (index[1],)
            ).fetchone()
            if result and result[0]:
                print(result[0] + ";")
    _print_jack("« Vous voyez comment les dossiers s’emboîtent. Le schéma montre les liens, pas encore ce qu’ils prouvent. »")


def _handle_command(connection: sqlite3.Connection, command: str) -> bool:
    parts = command.strip().split(maxsplit=1)
    name = parts[0].lower()
    argument = parts[1].strip() if len(parts) > 1 else None
    if name in {".exit", ".quit"}:
        return False
    if name in {".help", ".?"}:
        print("Commandes : .tables, .schema [table], .help, .exit.")
        print("Pendant une saisie multiligne, .cancel annule la requête. Terminez chaque requête SQL par un point-virgule.")
        _print_jack("« Une seule jointure à la fois, enquêteurs. Sinon, les pistes se brouillent. »")
    elif name == ".tables":
        _show_tables(connection)
    elif name == ".schema":
        _show_schema(connection, argument)
    elif name == ".cancel":
        print("Aucune requête multiligne à annuler.")
    else:
        print("Commande inconnue. Tapez .help pour consulter les commandes disponibles.")
    return True


def run_sql_console(database: Path) -> int:
    """Ouvre une console de requêtes uniquement en lecture seule."""
    database_uri = f"file:{database.resolve()}?mode=ro"
    connection = sqlite3.connect(database_uri, uri=True)
    pending = ""
    _print_banner()
    try:
        while True:
            try:
                prompt = (
                    _input_prompt("sql> ", "cyan", "bold")
                    if not pending
                    else _input_prompt("SQL… [; exécute | .cancel annule] > ", "cyan", "bold")
                )
                line = input(prompt)
            except EOFError:
                print()
                break
            if not pending and not line.strip():
                continue
            if pending and line.strip().lower() == ".cancel":
                pending = ""
                _print_jack("« Requête abandonnée. Les archives restent intactes ; vous pouvez repartir sur une nouvelle piste. »")
                continue
            if pending and line.strip().startswith("."):
                _print_jack("« Une requête attend encore son point-virgule. Terminez-la ou utilisez .cancel avant d’appeler une autre commande. »")
                continue
            if not pending and line.strip().startswith("."):
                if not _handle_command(connection, line):
                    break
                continue
            pending += line + "\n"
            if not sqlite3.complete_statement(pending):
                continue
            sql = pending.strip()
            pending = ""
            if _join_count(sql) > 1:
                print()
                _print_rule(color="red")
                _print_jack("« Une seconde jointure et je perds le fil. Séparez ces pistes, une seule jointure par requête. »")
                _print_rule(color="red")
                continue
            try:
                read_tables = set()
                connection.set_authorizer(_read_only_authorizer(read_tables))
                cursor = connection.execute(sql)
                rows = cursor.fetchall() if cursor.description else []
                _format_rows(cursor, rows)
                columns = [column[0].lower() for column in cursor.description or ()]
                _print_jack(_narration(read_tables, rows, columns, sql))
            except sqlite3.Error as error:
                print()
                _print_rule(color="red")
                print(_style(f"  Archive illisible : {error}", "red"))
                _print_jack("« Cette page du registre résiste... Vérifiez le nom de la table, les colonnes et la forme de la requête. »")
                _print_rule(color="red")
            finally:
                connection.set_authorizer(None)
    finally:
        connection.close()
    return 0

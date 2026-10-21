"""Console SQL en lecture seule avec les réactions de Jack Query."""

import os
import sqlite3
import sys
from pathlib import Path
from typing import Optional


TABLE_REACTIONS = {
    "channels": "Un lieu est identifié. Gardez son état et son identifiant sous les yeux.",
    "messages": "Une déclaration donne un point de vue. Confrontez-la aux heures et aux autres archives.",
    "events": "Les événements fixent des faits dans le temps. Comparez-les aux récits.",
    "access_grants": "Un droit indique ce qui était possible, pas qui a réellement agi.",
    "access_logs": "Une trace technique décrit une action. Vérifiez séparément l’identité associée à l’action.",
    "members": "Un nom relie une trace à un compte, mais un nom seul ne prouve rien.",
}
GENERIC_REACTION = "Notez ce résultat, puis confrontez-le à une archive indépendante avant de conclure."
MULTI_ARCHIVE_REACTION = "Plusieurs archives se recoupent. Distinguez ce qu’elles confirment de ce qu’elles ne montrent pas."
YELLOW = "\033[33m"
RESET = "\033[0m"
FROM_CLAUSE_END = {
    "WHERE", "GROUP", "HAVING", "ORDER", "LIMIT", "WINDOW", "UNION",
    "EXCEPT", "INTERSECT", "RETURNING", "QUALIFY",
}


def _print_narration(message: str, prefix: str = "[Jack Query]") -> None:
    """Affiche la narration en jaune dans un terminal, sans polluer les sorties redirigées."""
    line = f"{prefix} {message}"
    forced = os.environ.get("FORCE_COLOR") in {"1", "2", "3"}
    is_terminal = getattr(sys.stdout, "isatty", lambda: False)()
    supports_color = forced or is_terminal
    if os.environ.get("NO_COLOR"):
        supports_color = False
    print(f"{YELLOW}{line}{RESET}" if supports_color else line)


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


def _narration(read_tables: set[str], row_count: int) -> str:
    if row_count == 0:
        return "Aucune ligne ne répond à ce filtre. Élargissez ou vérifiez votre recherche."
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


def _format_rows(cursor: sqlite3.Cursor, rows: list[tuple]) -> None:
    names = [item[0] for item in cursor.description or ()]
    if not names:
        print("Requête exécutée.")
        return
    rendered = [["NULL" if value is None else str(value) for value in row] for row in rows]
    widths = [max([len(names[i])] + [len(row[i]) for row in rendered]) for i in range(len(names))]
    print(" | ".join(name.ljust(widths[i]) for i, name in enumerate(names)))
    print("-+-".join("-" * width for width in widths))
    for row in rendered:
        print(" | ".join(value.ljust(widths[i]) for i, value in enumerate(row)))
    print(f"({len(rows)} ligne(s))")


def _show_tables(connection: sqlite3.Connection) -> None:
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    print("  ".join(row[0] for row in rows))
    _print_narration("Les archives sont ouvertes. Choisissez un dossier et suivez ses liens.")


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
    _print_narration("Le schéma indique comment les archives se répondent, pas ce qu’elles prouvent.")


def _handle_command(connection: sqlite3.Connection, command: str) -> bool:
    parts = command.strip().split(maxsplit=1)
    name = parts[0].lower()
    argument = parts[1].strip() if len(parts) > 1 else None
    if name in {".exit", ".quit"}:
        return False
    if name in {".help", ".?"}:
        print("Commandes : .tables, .schema [table], .help, .exit. Terminez chaque requête SQL par un point-virgule.")
        _print_narration("Une requête à la fois, et une seule jointure au maximum, quelle que soit sa syntaxe.")
    elif name == ".tables":
        _show_tables(connection)
    elif name == ".schema":
        _show_schema(connection, argument)
    else:
        print("Commande inconnue. Tapez .help pour consulter les commandes disponibles.")
    return True


def run_sql_console(database: Path) -> int:
    """Ouvre une console de requêtes uniquement en lecture seule."""
    database_uri = f"file:{database.resolve()}?mode=ro"
    connection = sqlite3.connect(database_uri, uri=True)
    pending = ""
    print("Console d’enquête prête. Terminez chaque requête par ;, ou tapez .help. Une jointure maximum par requête.")
    try:
        while True:
            try:
                line = input("sql> " if not pending else "... ")
            except EOFError:
                print()
                break
            if not pending and not line.strip():
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
                _print_narration(
                    "cette archive demande une seule jointure au maximum. Séparez votre recherche en plusieurs requêtes.",
                    prefix="Jack Query :",
                )
                continue
            try:
                read_tables = set()
                connection.set_authorizer(_read_only_authorizer(read_tables))
                cursor = connection.execute(sql)
                rows = cursor.fetchall() if cursor.description else []
                _format_rows(cursor, rows)
                _print_narration(_narration(read_tables, len(rows) if cursor.description else 1))
            except sqlite3.Error as error:
                print(f"Archive illisible : {error}")
                _print_narration("Vérifiez le nom de la table, les colonnes et la forme de votre requête.")
            finally:
                connection.set_authorizer(None)
    finally:
        connection.close()
    return 0

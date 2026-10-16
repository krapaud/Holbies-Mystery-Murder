"""Start the Salon Fantôme investigation."""

import sqlite3
import sys
from pathlib import Path

from game.investigation_shell import run_sql_console
from game.validate_answer import validate

ROOT = Path(__file__).parent
DATABASE = ROOT / "database" / "game.db"
STUDENT_DATABASE = ROOT / ".student-data" / "game.db"


def build_database(database: Path = STUDENT_DATABASE) -> None:
    database.parent.mkdir(parents=True, exist_ok=True)
    database.unlink(missing_ok=True)
    connection = sqlite3.connect(database)
    try:
        connection.executescript((ROOT / "database" / "schema.sql").read_text())
        connection.executescript((ROOT / "database" / "seed.sql").read_text())
    finally:
        connection.close()


def main() -> int:
    arguments = sys.argv[1:]
    if not arguments:
        build_database()
        print("Opération Salon Fantôme")
        print("Kevin vous appelle : le 🏕️ Campement 7 a été supprimé.")
        print("Vous connaissez la scène. Vous devez maintenant trouver le compte compromis et le voleur.")
        print("Quand votre preuve est complète, quittez la console et relancez avec --answer 'COMPTE|VOLEUR'.")
        return run_sql_console(STUDENT_DATABASE)
    if arguments[0] != "--answer":
        print("Utilisez uniquement l'option --answer pour envoyer votre preuve.")
        return 1
    if len(arguments) != 2:
        print("Indiquez une preuve après --answer.")
        return 1
    return validate(arguments[1])


if __name__ == "__main__":
    raise SystemExit(main())

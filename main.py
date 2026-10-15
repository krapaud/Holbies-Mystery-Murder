"""Start the Salon Fantôme investigation."""

import sqlite3
from pathlib import Path

from game.validate_flag import validate

ROOT = Path(__file__).parent
DATABASE = ROOT / "database" / "game.db"


def build_database() -> None:
    DATABASE.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE)
    try:
        connection.executescript((ROOT / "database" / "schema.sql").read_text())
        connection.executescript((ROOT / "database" / "seed.sql").read_text())
    finally:
        connection.close()


def main() -> int:
    build_database()
    print("Dossier 001 - Disparition du salon vocal")
    print("Jack Query vous attend. Explorez la base avec : sqlite3 database/game.db")
    print("Quand vous avez reconstitué le flag, relancez ce programme avec --flag FLAG.")
    import sys
    if "--flag" in sys.argv:
        index = sys.argv.index("--flag")
        if index + 1 >= len(sys.argv):
            print("Indique un flag après --flag.")
            return 1
        return validate(sys.argv[index + 1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

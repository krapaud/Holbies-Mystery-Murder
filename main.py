"""Start the Salon Fantôme investigation."""

import sqlite3
import sys
from pathlib import Path

from game.validate_answer import validate

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
    print("Opération Salon Fantôme")
    print("Kevin vous appelle : le salon Orbite a été volé puis masqué.")
    print("Vous devez retrouver le salon, le compte privilégié utilisé et le voleur.")
    print("Explorez la base avec : sqlite3 database/game.db")
    print("Quand votre preuve est complète, relancez avec --answer 'SALON|COMPTE|VOLEUR'.")
    if "--answer" not in sys.argv:
        return 0
    index = sys.argv.index("--answer")
    if index + 1 >= len(sys.argv):
        print("Indiquez une preuve après --answer.")
        return 1
    return validate(sys.argv[index + 1])


if __name__ == "__main__":
    raise SystemExit(main())

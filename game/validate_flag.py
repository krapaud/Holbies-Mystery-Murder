"""Validate the structured final answer without exposing it."""

import hashlib

ANSWER_DIGEST = "d29aa5a12c4046bc86ba9562c7d416d43db9d108d7c9057e408107968786f672"


def validate(candidate: str) -> int:
    normalized = candidate.strip().upper()
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    if digest == ANSWER_DIGEST:
        print("Félicitations, vous avez identifié le salon, le compte utilisé et le voleur.")
        print("Kevin vous attend : le dossier est résolu.")
        return 0
    print("La preuve est incomplète. Vérifiez le salon, le compte privilégié et l'auteur du vol.")
    return 1


if __name__ == "__main__":
    import sys
    raise SystemExit(validate(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Preuve finale : ")))

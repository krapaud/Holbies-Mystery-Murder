"""Validate the structured final answer without exposing it."""

import hashlib

ANSWER_DIGEST = "5ae303e35b25cc3b4376255e50d4332e2e5fd250c382e3b3e6039ba0362cdf5f"


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

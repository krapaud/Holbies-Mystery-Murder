"""Validate the structured culprit proof without exposing it."""

import hashlib

ANSWER_DIGEST = "b3ffedd5bb99d61f2a0dabf1bff96e84f9384add08cec1854e4f5e36763c212a"


def validate(candidate: str) -> int:
    normalized = candidate.strip().upper()
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    if digest == ANSWER_DIGEST:
        print("Félicitations, vous avez identifié le compte compromis et le voleur.")
        print("Kevin vous attend : l'enquête est résolue.")
        return 0
    print("La preuve est incomplète. Vérifiez le compte privilégié et l'auteur du vol.")
    return 1


if __name__ == "__main__":
    import sys
    raise SystemExit(validate(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Preuve finale : ")))

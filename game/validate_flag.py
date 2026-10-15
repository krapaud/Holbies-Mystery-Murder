"""Validate the final answer without exposing it."""

import hashlib

FLAG_DIGEST = "b10a31ebbd8a5a65e83783612b7dbbec1d133c050a792e53e6723cf792a6376f"


def validate(candidate: str) -> int:
    digest = hashlib.sha256(candidate.strip().encode("utf-8")).hexdigest()
    if digest == FLAG_DIGEST:
        print("Félicitations, le mot de passe est correct ! Contacte Kevin, le maître des salons.")
        return 0
    print("Ce mot de passe ne clôture pas l'enquête. Vérifie tes fragments et réessaie.")
    return 1


if __name__ == "__main__":
    import sys
    raise SystemExit(validate(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Flag : ")))

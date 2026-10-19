#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
EVIDENCE="$ROOT/evidence"

for file in \
  "$EVIDENCE/incident/incident-note.txt" \
  "$EVIDENCE/identity/members.txt" \
  "$EVIDENCE/identity/credentials.txt" \
  "$EVIDENCE/identity/sessions.log" \
  "$EVIDENCE/logs/access.log" \
  "$EVIDENCE/logs/terminal-history.log" \
  "$EVIDENCE/git/branch-log.txt" \
  "$EVIDENCE/permissions/current.txt" \
  "$EVIDENCE/team/notes.txt"; do
  test -s "$file"
done

grep -Fq 'missing_file=release/release-candidate.tar.gz' "$EVIDENCE/incident/incident-note.txt"
grep -Fq 's-44|m-01|poste-04' "$EVIDENCE/identity/sessions.log"
grep -Fq 'cred-17|m-02' "$EVIDENCE/identity/credentials.txt"
grep -Fq 's-44|cred-17|remove|release/release-candidate.tar.gz|success' "$EVIDENCE/logs/access.log"
grep -Fq 'poste-04 rm' "$EVIDENCE/logs/terminal-history.log"
grep -Fq 'session=s-44' "$EVIDENCE/git/branch-log.txt"

echo "Shell Mystery Murder corpus: OK"

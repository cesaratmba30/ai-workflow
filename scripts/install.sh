#!/usr/bin/env bash
# Install ai-workflow skills into an agent's skills directory.
# Usage: scripts/install.sh [claude|codex|both] [--project] [--copy]
#   claude  -> ~/.claude/skills   (or .claude/skills with --project)
#   codex   -> ~/.codex/skills    (or .codex/skills with --project)
#   Default is symlink; --copy copies instead (use for machines that sync/clone).
set -euo pipefail

TARGETS="${1:-both}"; shift || true
MODE="link"; SCOPE="user"
for a in "$@"; do
  case "$a" in
    --copy) MODE="copy" ;;
    --project) SCOPE="project" ;;
    *) echo "unknown arg: $a" >&2; exit 1 ;;
  esac
done

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

install_into() {
  local dest="$1"
  mkdir -p "$dest"
  for d in "$REPO_DIR"/skills/*/; do
    name="$(basename "$d")"
    rm -rf "${dest:?}/$name"
    if [ "$MODE" = "copy" ]; then cp -R "$d" "$dest/$name"; else ln -s "$d" "$dest/$name"; fi
  done
  echo "Installed $(ls "$REPO_DIR/skills" | wc -l | tr -d ' ') skills -> $dest ($MODE)"
}

base_claude="$HOME/.claude/skills"; base_codex="$HOME/.codex/skills"
if [ "$SCOPE" = "project" ]; then base_claude=".claude/skills"; base_codex=".codex/skills"; fi

case "$TARGETS" in
  claude) install_into "$base_claude" ;;
  codex)  install_into "$base_codex" ;;
  both)   install_into "$base_claude"; install_into "$base_codex" ;;
  *) echo "usage: install.sh [claude|codex|both] [--project] [--copy]" >&2; exit 1 ;;
esac

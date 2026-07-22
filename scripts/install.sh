#!/usr/bin/env bash
# Install ai-workflow skills into an agent's skills directory. Non-destructive:
# an existing destination is backed up (never deleted) before being replaced,
# and you're asked to confirm unless --yes is passed.
#
# Usage: scripts/install.sh [claude|codex|both] [options]
#   claude  -> ~/.claude/skills   (or .claude/skills with --project)
#   codex   -> ~/.codex/skills    (or .codex/skills with --project)
#
# Options:
#   --project      install into the current project instead of the user's home
#   --copy         copy instead of symlink (default: symlink)
#   --yes, -y      don't prompt before replacing an existing skill
#   --dry-run      print what would happen, change nothing
#   --backup-dir=D put backups under D (default: <repo>/.install-backups/<timestamp>)
set -euo pipefail

TARGETS="${1:-both}"; shift || true
MODE="link"; SCOPE="user"; ASSUME_YES=0; DRY_RUN=0; BACKUP_DIR=""
for a in "$@"; do
  case "$a" in
    --copy) MODE="copy" ;;
    --project) SCOPE="project" ;;
    --yes|-y) ASSUME_YES=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --backup-dir=*) BACKUP_DIR="${a#--backup-dir=}" ;;
    -h|--help)
      sed -n '2,17p' "$0"; exit 0 ;;
    *) echo "unknown arg: $a" >&2; exit 1 ;;
  esac
done

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="${BACKUP_DIR:-$REPO_DIR/.install-backups/$TIMESTAMP}"

confirm() {
  # $1 = prompt message. Returns 0 (proceed) or 1 (skip).
  if [ "$ASSUME_YES" = 1 ]; then
    return 0
  fi
  if [ ! -t 0 ]; then
    echo "  SKIP: $1 (non-interactive; re-run with --yes to replace)" >&2
    return 1
  fi
  read -r -p "  $1 [y/N] " reply
  case "$reply" in
    y|Y|yes|YES) return 0 ;;
    *) return 1 ;;
  esac
}

already_correct() {
  # $1 = dest, $2 = source. True if dest is already a symlink to source
  # (link mode) or an up-to-date copy (copy mode, compared with diff -rq).
  local dest="$1" src="$2"
  if [ "$MODE" = "link" ]; then
    if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
      return 0
    fi
    return 1
  fi
  if [ -d "$dest" ] && diff -rq "$src" "$dest" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

install_into() {
  local dest="$1"
  mkdir -p "$dest"
  local installed=0 skipped=0 backed_up=0
  for d in "$REPO_DIR"/skills/*/; do
    d="${d%/}"
    name="$(basename "$d")"
    target="$dest/$name"

    if [ -e "$target" ] || [ -L "$target" ]; then
      if already_correct "$target" "$d"; then
        continue
      fi
      if [ "$MODE" = "copy" ] && [ -d "$target" ] && [ ! -L "$target" ]; then
        echo "  $name: destination differs from source:"
        diff -rq "$d" "$target" 2>&1 | sed 's/^/    /' | head -10 || true
      fi
      if ! confirm "$name already exists at $target — back it up and replace it?"; then
        skipped=$((skipped + 1))
        continue
      fi
      if [ "$DRY_RUN" = 1 ]; then
        echo "  [dry-run] would back up $target -> $BACKUP_DIR/$name"
      else
        mkdir -p "$BACKUP_DIR"
        mv "$target" "$BACKUP_DIR/$name"
        backed_up=$((backed_up + 1))
      fi
    fi

    if [ "$DRY_RUN" = 1 ]; then
      echo "  [dry-run] would $MODE $d -> $target"
    else
      if [ "$MODE" = "copy" ]; then cp -R "$d" "$target"; else ln -s "$d" "$target"; fi
    fi
    installed=$((installed + 1))
  done
  if [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] Would install $installed skill(s) -> $dest ($MODE)"
  else
    echo "Installed $installed skill(s) -> $dest ($MODE)"
  fi
  if [ "$skipped" -gt 0 ]; then
    echo "  Skipped $skipped existing skill(s) (declined or non-interactive)."
  fi
  if [ "$backed_up" -gt 0 ]; then
    echo "  Backed up $backed_up replaced skill(s) -> $BACKUP_DIR"
  fi
}

base_claude="$HOME/.claude/skills"; base_codex="$HOME/.codex/skills"
if [ "$SCOPE" = "project" ]; then base_claude=".claude/skills"; base_codex=".codex/skills"; fi

case "$TARGETS" in
  claude) install_into "$base_claude" ;;
  codex)  install_into "$base_codex" ;;
  both)   install_into "$base_claude"; install_into "$base_codex" ;;
  *) echo "usage: install.sh [claude|codex|both] [--project] [--copy] [--yes] [--dry-run]" >&2; exit 1 ;;
esac

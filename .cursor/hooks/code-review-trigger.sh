#!/bin/bash
# stop hook: after the agent finishes a turn, if reviewable code changed,
# tell the agent to delegate to the `code-reviewer` subagent before ending.
#
# A state file records the signature of the last-reviewed change-set so the
# follow-up only fires when the change-set actually changed. This lets the
# review->fix->review cycle converge (and stop) on its own; `loop_limit` in
# hooks.json is just a backstop.
set -euo pipefail

cat >/dev/null  # drain stdin (hook event JSON); not needed here

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [[ -z "$repo_root" ]]; then
  echo '{}'
  exit 0
fi
cd "$repo_root"

# Reviewable changes: source/test/infra files, excluding Cursor plumbing.
changed=$(
  git status --porcelain 2>/dev/null \
    | cut -c4- \
    | grep -E '(\.(py|sql|tf|tfvars|toml)$)|(^(src|tests|infrastructure)/)' \
    | grep -vE '^\.cursor/' \
    || true
)

if [[ -z "$changed" ]]; then
  echo '{}'
  exit 0
fi

# Signature of the current change-set (filenames + tracked diff content).
sig=$( { git status --porcelain; git diff HEAD 2>/dev/null; } \
  | shasum -a 256 | awk '{print $1}')

state_file=".cursor/hooks/.code-review-state"
last=""
[[ -f "$state_file" ]] && last=$(cat "$state_file")

# Already reviewed this exact change-set; don't loop.
if [[ "$sig" == "$last" ]]; then
  echo '{}'
  exit 0
fi
echo "$sig" >"$state_file"

file_list=$(echo "$changed" | sed 's/^/- /')

msg="Code changed this turn. Before ending your turn, delegate to the \`code-reviewer\` subagent (Task tool) to review these changes for business-logic/data-integrity, security, performance, and coding-standard issues.

Changed files:
${file_list}

Give the reviewer the diff to inspect (\`git diff HEAD\` for tracked edits, plus the contents of any new untracked files). After it reports: fix every Critical/High finding, briefly note Medium/Low ones, then finish. If it reports no issues, say so."

jq -n --arg m "$msg" '{followup_message: $m}'
exit 0

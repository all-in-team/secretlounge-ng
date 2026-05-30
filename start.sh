#!/bin/bash
set -e

mkdir -p data

cat > config.yaml << EOF
bot_token: "${BOT_TOKEN}"
database: [sqlite, "data/secretlounge.sqlite"]
allow_contacts: false
allow_documents: true
allow_remove_command: false
message_reaction_upvote: true
enable_signing: false
EOF

python3 apply_patch.py

exec python -m secretlounge_ng

#!/bin/bash
set -e

cat > config.yaml << EOF
bot_token: "${BOT_TOKEN}"
database: [sqlite, "secretlounge.sqlite"]
allow_contacts: false
allow_documents: true
allow_remove_command: false
message_reaction_upvote: true
enable_signing: false
EOF

exec python -m secretlounge_ng

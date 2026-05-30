#!/usr/bin/env python3
"""Apply pending approval patch to core.py at startup."""
import sys

CORE_PATH = "secretlounge_ng/core.py"

with open(CORE_PATH, "r") as f:
    content = f.read()

if "PENDING_PATCH_APPLIED" in content:
    print("Pending patch already applied")
    sys.exit(0)

helper = '''
# === PENDING_PATCH_APPLIED ===
import os as _os
_ADMIN_CHAT_ID = int(_os.environ.get("ADMIN_ID", "0"))

def _notify_admin_of_pending(c_user):
    try:
        from . import telegram as _tg
        if not _ADMIN_CHAT_ID or _tg.bot is None:
            return
        name = c_user.realname or "(no name)"
        username = "@" + c_user.username if c_user.username else None
        identifier = username if username else str(c_user.id)
        msg_lines = [
            "🔔 <b>New join request</b>",
            f"Username: {username or '(no username)'}",
            f"Name: {name}",
            f"ID: <code>{c_user.id}</code>",
            "",
            f"To approve, send: <code>/promote {identifier} user</code>",
        ]
        _tg.bot.send_message(_ADMIN_CHAT_ID, "\\n".join(msg_lines), parse_mode="HTML")
    except Exception:
        import logging
        logging.exception("Failed to send pending notification")
# === END PENDING_PATCH ===

'''

marker = "# module variables"
if marker n

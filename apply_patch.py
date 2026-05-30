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
if marker not in content:
    print(f"ERROR: marker '{marker}' not found")
    sys.exit(1)
content = content.replace(marker, helper + marker, 1)

old_block = '''	# create new user
	user = User()
	user.defaults()
	user.id = c_user.id
	updateUserFromEvent(user, c_user)
	if not any(db.iterateUserIds()):
		user.rank = RANKS.admin

	logging.info("%s joined chat", user)
	db.addUser(user)
	ret = [rp.Reply(rp.types.CHAT_JOIN)]

	motd = db.getSystemConfig().motd
	if motd:
		ret.append(rp.Reply(rp.types.CUSTOM, text=motd))

	return ret'''

new_block = '''	# create new user
	user = User()
	user.defaults()
	user.id = c_user.id
	updateUserFromEvent(user, c_user)

	is_first = not any(db.iterateUserIds())
	if is_first:
		user.rank = RANKS.admin
		logging.info("%s joined chat as first user (admin)", user)
		db.addUser(user)
		ret = [rp.Reply(rp.types.CHAT_JOIN)]
		motd = db.getSystemConfig().motd
		if motd:
			ret.append(rp.Reply(rp.types.CUSTOM, text=motd))
		return ret

	user.rank = RANKS.banned
	user.blacklistReason = "PENDING_APPROVAL"
	logging.info("%s joined as PENDING (awaiting approval)", user)
	db.addUser(user)
	_notify_admin_of_pending(c_user)
	return [rp.Reply(rp.types.CUSTOM, text="\u23f3 Your join request has been sent to the admin. You will be notified once approved.")]'''

if old_block not in content:
    print("ERROR: old_block not found in core.py")
    sys.exit(1)

content = content.replace(old_block, new_block)

with open(CORE_PATH, "w") as f:
    f.write(content)

print("Pending patch applied successfully")

from telethon import Button, events

from Evelyn import tbot
from Evelyn.events import Cbot

from . import can_ban_users, cb_can_ban_users, db, get_user, is_admin

approve_d = db.approve_d


@Cbot(pattern="^/approve ?(.*)")
async def appr(event):
    if (
        event.text.startswith(".approved")
        or event.text.startswith("/approved")
        or event.text.startswith("!approved")
        or event.text.startswith("?approved")
        or event.text.startswith("?approval")
        or event.text.startswith(".approval")
        or event.text.startswith("/approval")
        or event.text.startswith("!approved")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if not await can_ban_users(event, event.sender_id):
            return
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if await is_admin(event.chat_id, user.id):
            return await event.reply(
                "User is already admin - locks, blocklists, and antiflood already don't apply to them."
            )
        a_str = "<a href='tg://user?id={}'>{}</a> has been approved in {}! They will now be ignored by automated admin actions like locks, blocklists, and antiflood."
        await event.respond(
            a_str.format(user.id, user.first_name, event.chat.title),
            reply_to=event.reply_to_msg_id or event.id,
            parse_mode="html",
        )
        if not approve_d.find_one({"user_id": user.id, "chat_id": event.chat_id}):
            approve_d.insert_one(
                {"user_id": user.id, "chat_id": event.chat_id, "name": user.first_name}
            )
    else:
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        cb_data = str(user.id) + "|" + "approve" + "|" + str(user.first_name[:15])
        a_text = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        a_button = Button.inline("Click to prove admin", data="anap_{}".format(cb_data))
        await event.reply(a_text, buttons=a_button)


@Cbot(pattern="^/disapprove ?(.*)")
async def dissapprove(event):
    if (
        event.text.startswith(".disapproveall")
        or event.text.startswith("!disapproveall")
        or event.text.startswith("?disapproveall")
        or event.text.startswith("/disapproveall")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if not await can_ban_users(event, event.sender_id):
            return
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if await is_admin(event.chat_id, user.id):
            return await event.reply("This user is an admin, they can't be unapproved.")
        if approved.find_one({"user_id": user.id, "chat_id": event.chat_id}):
            await event.reply(
                f"{user.first_name} is no longer approved in {event.chat.title}."
            )
            return approve_d.delete_one({"user_id": user.id})
        await event.reply(f"{user.first_name} isn't approved yet!")
    else:
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        cb_data = str(user.id) + "|" + "disapprove" + "|" + str(user.first_name[:15])
        a_text = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        a_button = Button.inline("Click to prove admin", data="anap_{}".format(cb_data))
        await event.reply(a_text, buttons=a_button)


@Cbot(pattern="^/approved")
async def approved(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if not await can_ban_users(event, event.sender_id):
            return
    app_rove_d = approve_d.find({"chat_id": event.chat_id})
    if not app_rove_d:
        await event.reply(f"No users are approved in {event.chat.title}")
    else:
        out_str = "The following users are approved:"
        for app_r in app_rove_d:
            out_str += "\n- `{}`: {}".format(app_r["user_id"], app_r["name"])
        await event.reply(out_str)


# Anonymous Admins
# ----------------
@tbot.on(events.CallbackQuery(pattern=r"anap(\_(.*))"))
async def _(event):
    input = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    user, mode, name = input.split("|")
    user = int(user.strip())
    mode = mode.strip()
    name = name.strip()
    if not await cb_can_ban_users(event, event.sender_id):
        return
    if mode == "disapprove":
        if await is_admin(event.chat_id, user):
            return await event.edit("This user is an admin, they can't be unapproved.")
        if approved.find_one({"user_id": user, "chat_id": event.chat_id}):
            await event.edit(f"{name} is no longer approved in {event.chat.title}.")
            return approve_d.delete_one({"user_id": user})
        await event.edit(f"{name} isn't approved yet!")
    elif mode == "approve":
        if await is_admin(event.chat_id, user):
            return await event.edit(
                "User is already admin - locks, blocklists, and antiflood already don't apply to them."
            )
        a_str = "<a href='tg://user?id={}'>{}</a> has been approved in {}! They will now be ignored by automated admin actions like locks, blocklists, and antiflood."
        await event.edit(
            a_str.format(user, name, event.chat.title),
            parse_mode="html",
        )
        if not approve_d.find_one({"user_id": user, "chat_id": event.chat_id}):
            approve_d.insert_one(
                {"user_id": user, "chat_id": event.chat_id, "name": user.first_name}
            )

from telethon import Button, events
from telethon.errors import ChatAdminRequiredError
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

import Jessica.modules.sql.fsub_sql as sql
from Jessica import BOT_ID, CMD_HELP, OWNER_ID, tbot
from Jessica.events import Cbot

from . import DEVS, is_admin


async def participant_check(channel, user_id):
    try:
        await tbot(GetParticipantRequest(channel, int(user_id)))
        return True
    except UserNotParticipantError:
        return False
    except:
        return False


@Cbot(pattern="^/(fsub|Fsub|forcesubscribe|Forcesub|forcesub|Forcesubscribe) ?(.*)")
async def fsub(event):
    if event.is_private:
        return
    if event.is_group:
        perm = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not perm.is_admin:
            return await event.reply("You need to be an admin to do this.")
        if not perm.is_creator:
            return await event.reply(
                "❗ <b>Group Creator Required</b> \n<i>You have to be the group creator to do that.</i>",
                parse_mode="html",
            )
    try:
        channel = event.text.split(None, 1)[1]
    except IndexError:
        channel = None
    if not channel:
        chat_db = sql.fs_settings(event.chat_id)
        if not chat_db:
            await event.reply(
                "<b>❌ Force Subscribe is disabled in this chat.</b>", parse_mode="HTML"
            )
        else:
            await event.reply(
                f"Forcesubscribe is currently <b>enabled</b>. Users are forced to join <b>@{chat_db.channel}</b> to speak here.",
                parse_mode="html",
            )
    elif channel in ["on", "yes", "y"]:
        await event.reply("❗Please specify the channel username.")
    elif channel in ["off", "no", "n"]:
        await event.reply("**❌ Force Subscribe is Disabled Successfully.**")
        sql.disapprove(event.chat_id)
    else:
        try:
            channel_entity = await tbot.get_entity(channel)
        except:
            return await event.reply(
                "❗<b>Invalid channel Username provided.</b>", parse_mode="html"
            )
        channel = channel_entity.username
        try:
            channel_entity.broadcast
            if not channel_entity.broadcast:
                return await event.reply("That's not a valid channel.")
        except:
            return await event.reply("That's not a valid channel.")
        if not await participant_check(channel, BOT_ID):
            return await event.reply(
                f"❗**Not an Admin in the Channel**\nI am not an admin in the [channel](https://t.me/{channel}). Add me as a admin in order to enable ForceSubscribe.",
                link_preview=False,
            )
        sql.add_channel(event.chat_id, str(channel))
        await event.reply(f"✅ **Force Subscribe is Enabled** to @{channel}.")


@tbot.on(events.NewMessage())
async def fsub_n(e):
    if not sql.fs_settings(e.chat_id):
        return
    if e.is_private:
        return
    if e.chat.admin_rights:
        if not e.chat.admin_rights.ban_users:
            return
    else:
        return
    if not e.from_id:
        return
    if (
        await is_admin(e.chat_id, e.sender_id)
        or e.sender_id in DEVS
        or e.sender_id == OWNER_ID
    ):
        return
    channel = (sql.fs_settings(e.chat_id)).channel
    try:
        check = await participant_check(channel, e.sender_id)
    except ChatAdminRequiredError:
        return
    if not check:
        buttons = [Button.url("Join Channel", f"t.me/{channel}")], [
            Button.inline("Unmute Me", data="fs_{}".format(str(e.sender_id)))
        ]
        txt = f'<b><a href="tg://user?id={e.sender_id}">{e.sender.first_name}</a></b>, you have <b>not subscribed</b> to our <b><a href="t.me/{channel}">Channel</a></b> yet❗.Please <b><a href="t.me/{channel}">Join</a></b> and <b>press the button below</b> to unmute yourself.'
        await e.reply(txt, buttons=buttons, parse_mode="html", link_preview=False)
        await tbot.edit_permissions(e.chat_id, e.sender_id, send_messages=False)


@tbot.on(events.CallbackQuery(pattern=r"fs(\_(.*))"))
async def unmute_fsub(event):
    user_id = int(((event.pattern_match.group(1)).decode()).split("_", 1)[1])
    if not event.sender_id == user_id:
        return await event.answer("This is not meant for you.", alert=True)
    channel = (sql.fs_settings(e.chat_id)).channel
    check = False
    try:
        check = await participant_check(channel, user_id)
    except ChatAdminRequiredError:
        return
    if not check:
        return await event.answer(
            "You have to join the channel first, to get unmuted!", alert=True
        )
    try:
        await tbot.edit_permissions(event.chat_id, user_id, send_messages=True)
    except ChatAdminRequiredError:
        pass
    await event.delete()


__name__ = "forcesubscribe"
__help__ = """
Here is the help for the FSub module:

Commands (`chat creator only`):

 • /forcesub <channel username>: It will force user to join channel otherwise user will remain muted till admins unmute.
    Example:
      /fjoin @NidhiUpdates » If user not joined channel than Nidhi mutes him till he joins channel and click unmute button.
 • /forcesub: Sends current settings of the chat.
 • /forcesub on/off: To turn off force join channel.

Forcesub now supports multiple channels, simply now bot will force users to Join multiple channels if enabled like /fsub `@NekoChan_GbanLogs @Nekochan_Updates`
To Force user to join single channel use like this /fjoin @GlobalLogs

Works for Public channels only.

/fsub or /forcesubscribe another alias of /forcesub.

**Note:** You need to make Bot admin in channel and group before turning on this module.
"""

CMD_HELP.update({__name__: [__name__, __help__]})

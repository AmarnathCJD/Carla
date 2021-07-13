import os

from telethon import Button, events
from telethon.errors.rpcerrorlist import (
    ChatNotModifiedError,
    ParticipantsTooFewError,
    UserAdminInvalidError,
)
from telethon.tl.functions.channels import (
    EditPhotoRequest,
    EditTitleRequest,
    SetStickersRequest,
)
from telethon.tl.functions.messages import EditChatAboutRequest, ExportChatInviteRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaDocument,
    MessageMediaPhoto,
    UserStatusLastMonth,
)

from Jessica import OWNER_ID, tbot
from Jessica.events import Cbot

from . import (
    ELITES,
    can_change_info,
    can_promote_users,
    cb_can_promote_users,
    check_owner,
    get_user,
    is_admin,
    is_owner,
)


@Cbot(pattern="^/promote ?(.*)")
async def _(event):
    if event.is_private:
        return  # connection
    title = None
    if event.from_id:
        if event.sender_id == OWNER_ID or event.sender_id in ELITES:
            pass
        elif await can_promote_users(event, event.sender_id):
            pass
        else:
            return
        try:
            user, title = await get_user(event)
        except:
            pass
        if not user:
            return
        if not title:
            title = "Λ∂мιи"
        if await check_owner(event, user.id):
            return await event.reply(
                "I would love to promote the chat creator, but... well, they already have all the power."
            )
        try:
            await tbot.edit_admin(
                event.chat_id,
                user.id,
                manage_call=False,
                add_admins=False,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title=title,
            )
            name = user.first_name
            if name:
                name = (name.replace("<", "&lt;")).replace(">", "&gt!")
            await event.reply(
                f"Successfully promoted <a href='tg://user?id={user.id}'>{name}</a>!",
                parse_mode="html",
            )
        except UserAdminInvalidError:
            return await event.reply(
                "This user has already been promoted by someone other than me; I can't change their permissions!"
            )
        except:
            await event.reply("Seems like I don't have enough rights to do that.")
    else:
        await anonymous(event, "promote")


@Cbot(pattern="^/superpromote ?(.*)")
async def _(event):
    if event.is_private:
        return  # connection
    title = None
    if event.from_id:
        if event.sender_id == OWNER_ID or event.sender_id in ELITES:
            pass
        elif await can_promote_users(event, event.sender_id):
            pass
        else:
            return
        try:
            user, title = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if not title:
            title = "𝙎υρєя Λ∂мιи"
        if await check_owner(event, user.id):
            return await event.reply(
                "I would love to promote the chat creator, but... well, they already have all the power."
            )
        try:
            await tbot.edit_admin(
                event.chat_id,
                user.id,
                manage_call=True,
                add_admins=True,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title=title,
            )
            name = user.first_name
            if name:
                name = (name.replace("<", "&lt;")).replace(">", "&gt!")
            await event.reply(
                f"Successfully promoted <a href='tg://user?id={user.id}'>{name}</a>!",
                parse_mode="html",
            )
        except UserAdminInvalidError:
            return await event.reply(
                "This user has already been promoted by someone other than me; I can't change their permissions!."
            )
        except:
            await event.reply("Seems like I don't have enough rights to do that.")
    else:
        await anonymous(event, "superpromote")


@Cbot(pattern="^/demote ?(.*)")
async def _(event):
    if event.is_private:
        return  # connection
    if event.from_id:
        if event.sender_id == OWNER_ID or event.sender_id in ELITES:
            pass
        elif await can_promote_users(event, event.sender_id):
            pass
        else:
            return
        try:
            user, title = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if await check_owner(event, user.id):
            return await event.reply(
                "I don't really feel like staging a mutiny today, I think the chat owner deserves to stay an admin."
            )
        elif user.bot:
            return await event.reply(
                "Due to telegram limitations, I can't demote bots. Please demote them manually!"
            )
        if not await is_admin(event.chat_id, user.id):
            return await event.reply("This user isn't an admin anyway!")
        try:
            await tbot.edit_admin(
                event.chat_id,
                user.id,
                is_admin=False,
                manage_call=False,
                add_admins=False,
                pin_messages=False,
                delete_messages=False,
                ban_users=False,
                change_info=False,
                invite_users=False,
            )
            name = user.first_name
            if name:
                name = (name.replace("<", "&lt;")).replace(">", "&gt!")
            await event.reply(
                f"Demoted <a href='tg://user?id={user.id}'>{name}</a>!",
                parse_mode="html",
            )
        except UserAdminInvalidError:
            return await event.reply(
                "This user was promoted by someone other than me; I can't change their permissions! Demote them manually."
            )
        except:
            await event.reply("Seems like I don't have enough rights to do that.")
    else:
        await anonymous(event, "demote")


async def anonymous(event, mode):
    try:
        user, title = await get_user(event)
    except:
        pass
    if not user:
        return
    if user.bot and mode == "demote":
        return await event.reply(
            "Due to telegram limitations, I can't demote bots. Please demote them manually!"
        )
    cb_data = f"{user.id}!{mode}"
    buttons = Button.inline("Click to prove Admin", data="sup_{}".format(cb_data))
    await event.reply(
        "It looks like you're anonymous. Tap this button to confirm your identity.",
        buttons=buttons,
    )


@tbot.on(events.CallbackQuery(pattern=r"sup(\_(.*))"))
async def _(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    input = data.split("_", 1)[1]
    user_id, mode = input.split("!", 1)
    user_id = user_id.strip()
    mode = mode.strip()
    if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
        k = await cb_can_promote_users(event, event.sender_id)
        if not k:
            return
    if mode == "promote":
        try:
            await tbot.edit_admin(
                event.chat_id,
                int(user_id),
                manage_call=False,
                add_admins=False,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title="Admin",
            )
            text = f"Promoted **User** in **{event.chat.title}**."
        except:
            text = "Seems like I don't have enough rights to do that."
    elif mode == "superpromote":
        try:
            await tbot.edit_admin(
                event.chat_id,
                int(user_id),
                manage_call=True,
                add_admins=True,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title="Admin",
            )
            text = f"Promoted **User** in **{event.chat.title}** with full Rights."
        except:
            text = "Seems like I don't have enough rights to do that."
    elif mode == "demote":
        try:
            await tbot.edit_admin(
                event.chat_id,
                int(user_id),
                is_admin=False,
                manage_call=False,
                add_admins=False,
                pin_messages=False,
                delete_messages=False,
                ban_users=False,
                change_info=False,
                invite_users=False,
            )
            text = "Demoted!."
        except:
            text = "Seems like I don't have enough rights to do that."
    await event.edit(text)


@Cbot(pattern="^/invitelink")
async def link(event):
    if event.is_private:
        return  # connection
    if event.from_id:
        if not await is_admin(event.chat_id, event.sender_id):
            return await event.reply("You need to be an admin to do this ")
        perm = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not perm.invite_users:
            return await event.reply(
                "You are missing the following rights to use this command: CanInviteUsers."
            )
        link = await tbot(ExportChatInviteRequest(event.chat_id))
        await event.reply(f"`{link.link}`", link_preview=False)
    else:
        link = await tbot(ExportChatInviteRequest(event.chat_id))
        await event.reply(f"`{link.link}`", link_preview=False)


@Cbot(pattern="^/adminlist")
async def admeene(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.chat.admin_rights.ban_users:
        return
    mentions = f"Admins in **{event.chat.title}:**"
    async for user in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        if not user.bot:
            if not user.deleted:
                if user.username:
                    link = "- @{}".format(user.username)
                    mentions += f"\n{link}"
    mentions += "\n\nNote: __These values are up-to-date__"
    await event.reply(mentions)


@Cbot(pattern="^/kickthefools$")
async def kekthem(event):
    if event.is_private:
        return await event.reply("This command is made for Groups, not my PM.")
    if not await is_owner(event, event.sender_id):
        return
    if not event.chat.admin_rights.ban_users:
        return await event.reply("Unable to perform, not enough rights.")
    total = 0
    zec = await event.reply("Working....")
    async for c in tbot.iter_participants(event.chat_id):
        if isinstance(c.status, UserStatusLastMonth):
            await tbot.kick_participant(event.chat_id, c.id)
            total += 1
    if total == 0:
        return await zec.edit("Congo, No inactive users to kick.")
    await zec.edit(f"Sucessfully kicked {total} Inactive users.")


@Cbot(pattern="^/bots$")
async def bot(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.is_group:
        if not await is_admin(event.chat_id, event.sender_id):
            return await event.reply("Only admins can execute this command!")
    final = f"Bots in __{event.chat.title}__:"
    async for user in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsBots
    ):
        final += f"\n- @{user.username}"
    await event.reply(final)


@Cbot(pattern="^/rpromote ?(.*)")
async def kek(event):
    if not event.sender_id == OWNER_ID:
        return
    user = None
    try:
        user, chat = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    user_id = user.id
    try:
        chat = await tbot.get_entity(int(chat))
    except ValueError:
        chat = await tbot.get_entity(chat)
    except:
        return await event.reply("Unable to find the chat/channel!")
    chat_id = chat.id
    try:
        await tbot.edit_admin(
            chat_id,
            int(user_id),
            manage_call=True,
            add_admins=True,
            pin_messages=True,
            delete_messages=True,
            ban_users=True,
            change_info=True,
            invite_users=True,
            title="Admin",
        )
        await event.reply(f"Promoted **{user.first_name}** in **{chat.title}**")
    except:
        await event.reply("Seems like I don't have enough rights to do that.")


@Cbot(pattern="^/setgpic")
async def x_pic(e):
    if not e.is_channel:
        return await e.reply("This command is made to be used in groups!")
    if not await can_change_info(e, e.sender_id):
        return
    if not e.reply_to:
        return await e.reply("Reply to some photo or file to set new chat pic!")
    reply = await e.get_reply_message()
    if e.chat.admin_rights:
        if not e.chat.admin_rights.change_info:
            return await e.reply("Error! Not enough rights to change chat photo")
    else:
        return
    if not reply.media:
        return await e.reply("That's not a valid image for group pic!")
    elif isinstance(reply.media, MessageMediaPhoto):
        photo = reply.media.photo
    elif (
        isinstance(reply.media, MessageMediaDocument)
        and reply.media.document.mime_type.split("/", 1)[0] == "image"
    ):
        photo = reply.media.document
        photo_x = await tbot.download_media(photo, "photo.jpg")
        photo = await tbot.upload_file(photo_x)
        os.remove(photo_x)
    else:
        return await e.reply("That's not a valid image for group pic!")
    try:
        await tbot(EditPhotoRequest(e.chat_id, photo))
    except Exception as x:
        return await e.reply(str(x))
    await e.reply("✨ Successfully set new chatpic!")


@Cbot(pattern="^/setgtitle ?(.*)")
async def x_title(e):
    if not e.is_channel:
        return await e.reply("This command is made to be used in groups!")
    if not await can_change_info(e, e.sender_id):
        return
    if not e.pattern_match.group(1):
        return await e.reply("Enter some text to set new title in your chat!")
    if e.chat.admin_rights:
        if not e.chat.admin_rights.change_info:
            return await e.reply("Error! Not enough rights to change chat title")
    else:
        return
    text = e.pattern_match.group(1)
    try:
        await tbot(EditTitleRequest(e.chat_id, text))
        await e.reply(f"✨ Successfully set **{text}** as new chat title!")
    except ChatNotModifiedError:
        await e.reply(f"✨ Successfully set **{text}** as new chat title!")
    except Exception as x:
        await e.reply(str(x))


@Cbot(pattern="^/setgsticker")
async def x_sticker_set(e):
    if not e.is_channel:
        return await e.reply("This command is made to be used in groups!")
    if not await can_change_info(e, e.sender_id):
        return
    if not e.reply_to:
        return await e.reply("Reply to some sticker to set new chat sticker pack!")
    reply = await e.get_reply_message()
    if not reply.media:
        return await e.reply(
            "You need to reply to some sticker to set chat sticker set!"
        )
    if not isinstance(reply.media, MessageMediaDocument):
        return await e.reply(
            "You need to reply to some sticker to set chat sticker set!"
        )
    x_meme = reply.media.document.mime_type
    if not str(x_meme) == "image/webp":
        return await e.reply(
            "You need to reply to some sticker to set chat sticker set!"
        )
    sticker_set_id = sticker_set_access_hash = None
    try:
        for x in range(len(reply.media.document.attributes)):
            _x = reply.media.document.attributes[x]
            if isinstance(_x, DocumentAttributeSticker):
                sticker_set_id = _x.stickerset.id
                sticker_set_access_hash = _x.stickerset.access_hash
    except Exception as x:
        return await e.reply(
            "You need to reply to some sticker to set chat sticker set!" + str(x)
        )
    if not sticker_set_id:
        return await e.reply("Failed to find the sticker set for the sticker!")
    try:
        await tbot(
            SetStickersRequest(
                e.chat_id,
                InputStickerSetID(
                    id=sticker_set_id, access_hash=sticker_set_access_hash
                ),
            )
        )
        await e.reply(f"✨ Successfully set new group stickers in {e.chat.title}!")
    except ChatNotModifiedError:
        await e.reply(f"✨ Successfully set new group stickers in {e.chat.title}!")
    except ParticipantsTooFewError:
        await e.reply("Failed to set stickerset, Not enough participants.")
    except Exception as x:
        await e.reply(str(x))


@Cbot(pattern="^/(setgdesc|setgdescription) ?(.*)")
async def x_description(e):
    if not e.is_channel:
        return await e.reply("This command is made to be used in groups!")
    if not await can_change_info(e, e.sender_id):
        return
    if not e.reply_to:
        try:
            about = e.text.split(None, 1)[1]
        except IndexError:
            about = None
        if not about:
            return await e.reply("Setting empty description won't do anything!")
    elif e.reply_to:
        reply = await e.get_reply_message()
        if not reply.text:
            return await e.reply("Setting empty description won't do anything!")
        about = reply.text
    try:
        await tbot(EditChatAboutRequest(e.chat_id, about))
        await e.reply(f"✨ Successfully updated chat description in {e.chat.title}!")
    except ChatNotModifiedError:
        await e.reply(f"✨ Successfully updated chat description in {e.chat.title}!")
    except Exception as x:
        await e.reply(str(x))


__name__ = "admin"
__help__ = """
test
"""

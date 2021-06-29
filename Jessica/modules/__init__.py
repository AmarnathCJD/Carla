import asyncio
import math
import re
import shlex
import time
from random import choice, randint
from typing import Tuple

from multicolorcaptcha import CaptchaGenerator
from PIL import Image, ImageDraw, ImageFont
from pymongo import MongoClient
from telethon import Button, events, types
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

from Jessica import BOT_ID, MONGO_DB_URI, OWNER_ID, tbot
from Jessica.modules.sql.chats_sql import add_chat, is_chat

SUDO_USERS = []
ELITES = []
DEVS = []

ELITES.append(OWNER_ID)

# DB
client = MongoClient(MONGO_DB_URI)
db = client["Rylee"]

# Add chat to DB
@tbot.on(events.ChatAction())
async def handler(event):
    if event.user_added:
        if event.user_id == int(BOT_ID):
            if not is_chat(event.chat_id):
                add_chat(event.chat_id)
            await event.respond(
                f"""Thanks for adding me to {event.chat.title}

Promote me as administrator in your group otherwise I will not function properly""",
                buttons=[
                    [Button.url("Support Chat", "https://t.me/NekoChan_Support")],
                    [Button.url("Updates Channel", "https://t.me/NekoChan_Updates")],
                ],
            )


async def can_promote_users(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.reply("You have to be an admin to do this!")
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        if not p.participant.admin_rights.add_admins:
            await event.reply(
                "You are missing the following rights to use this command: CanPromoteMembers."
            )
            return False
        return True


async def cb_can_promote_users(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.answer("You have to be an admin to do this!", alert=True)
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        if not p.participant.admin_rights.add_admins:
            await event.edit(
                "You are missing the following rights to use this command: CanPromoteMembers."
            )
            return False
        return True


async def cb_can_ban_users(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.answer("You have to be an admin to do this!", alert=True)
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        if not p.participant.admin_rights.ban_users:
            await event.edit(
                "You are missing the following rights to use this command: CanRestrictUsers."
            )
            return False
        return True


async def can_change_info(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.reply("You have to be an admin to do this!")
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        if not p.participant.admin_rights.change_info:
            await event.reply(
                "You are missing the following rights to use this command: CanChangeInfo."
            )
            return False
        return True


async def cb_can_change_info(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.reply("You have to be an admin to do this!")
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        if not p.participant.admin_rights.change_info:
            await event.reply(
                "You are missing the following rights to use this command: CanChangeInfo."
            )
            return False
        return True


async def can_pin_messages(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.reply("You have to be an admin to do this!")
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        if not p.participant.admin_rights.pin_messages:
            await event.reply(
                "You are missing the following rights to use this command: CanPinMessages."
            )
            return False
        return True


async def can_ban_users(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.reply("You have to be an admin to do this!")
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        if not p.participant.admin_rights.ban_users:
            await event.reply(
                "You are missing the following rights to use this command: CanRestrictUsers."
            )
            return False
        return True


async def is_owner(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.reply("You have to be an admin to do this!")
        return False
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        await event.reply(
            f"You need to be the chat owner of {event.chat.title} to do this."
        )
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True


async def cb_is_owner(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.answer("You have to be an admin to do this!", alert=True)
        return False
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        await event.edit(
            f"You need to be the chat owner of {event.chat.title} to do this."
        )
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True


async def check_owner(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    else:
        return False


async def can_del_msg(event, user_id):
    try:
        p = await tbot(GetParticipantRequest(event.chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipant):
        await event.reply("You have to be an admin to do this!")
        return False
    elif isinstance(p.participant, types.ChannelParticipantCreator):
        return True
    elif isinstance(p.participant, types.ChannelParticipantAdmin):
        if not p.participant.admin_rights.delete_messages:
            await event.reply(
                "You are missing the following rights to use this command: CanDeleteMessages."
            )
            return False
        return True


async def is_admin(chat_id, user_id):
    try:
        p = await tbot(GetParticipantRequest(chat_id, user_id))
    except UserNotParticipantError:
        return False
    if isinstance(p.participant, types.ChannelParticipantAdmin) or isinstance(
        p.participant, types.ChannelParticipantCreator
    ):
        return True
    else:
        return False


async def get_user(event):
    args = event.pattern_match.group(1).split(" ", 1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await tbot.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        extra = None
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.reply(
                "I don't know who you're talking about, you're going to need to specify a user...!"
            )
            return
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError):
            await event.reply(
                "Looks like I don't have control over that user, or the ID isn't a valid one. If you reply to one of their messages, I'll be able to interact with them."
            )
            return

    return user_obj, extra


"""
if not event.message.entities is not None:
            ent = event.message.entities[0]
            if isinstance(ent, types.MessageEntityMentionName):
                user = ent.user_id
                try:
                    user_obj = await tbot.get_entity(user)
                except (TypeError, ValueError):
                    await event.reply(
                        "Looks like I don't have control over that user, or the ID isn't a valid one. If you reply to one of their messages, I'll be able to interact with them."
                    )
                    return
                return user_obj, extra
"""


async def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await message.reply("Invalid time amount specified.")
            return ""
        if unit == "m":
            bantime = int(time_num) * 60
        elif unit == "h":
            bantime = int(time_num) * 60 * 60
        elif unit == "d":
            bantime = int(time_num) * 24 * 60 * 60
        else:
            return
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return False


def g_time(time):
    time = int(time)
    if time >= 86400:
        time = time / (60 * 60 * 24)
        text = f"{int(time)} days"
        if not time - int(time) == 0:
            kuk = (time - int(time)) * 24
            text += f" {int(kuk)} hours"
    elif time >= 3600 < 86400:
        time = time / (60 * 60)
        text = f"{int(time)} hours"
        if not time - int(time) == 0:
            kuk = (time - int(time)) * 60
            text += f" {int(kuk)} minutes"
    elif time >= 60 < 3600:
        time = time / 60
        text = f"{int(time)} minutes"
        if not time - int(time) == 0:
            kuk = (time - int(time)) * 60
            text += f" {int(kuk)} seconds"
    return text


BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\((btnurl|buttonalert):(?:/{0,2})(.+?)(:same)?\))"
)


def button_parser(text):
    if "buttonalert" in text:
        text = text.replace("\n", "\\n").replace("\t", "\\t")
    buttons = []
    note_data = ""
    prev = 0
    for match in BTN_URL_REGEX.finditer(text):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            note_data += text[prev : match.start(1)]
            prev = match.end(1)
            if bool(match.group(5)) and buttons:
                buttons[-1].append(
                    Button.url(match.group(2), match.group(4).replace(" ", ""))
                )
            else:
                buttons.append(
                    [Button.url(match.group(2), match.group(4).replace(" ", ""))]
                )

        # if odd, escaped -> move along
        else:
            note_data += text[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += text[prev:]
    if str(buttons) == "[]":
        buttons = None
    try:
        return note_data, buttons
    except:
        return note_data


BUTTONS = {}


def get_reply_msg_btns_text(message):
    text = ""
    for column in message.reply_markup.rows:
        btn_num = 0
        for btn in column.buttons:
            btn_num += 1
            btn.text
            if btn.url:
                btn.url
                text += f"\n[{btn.text}](btnurl:{btn.url}*!repl!*)"
                if btn_num > 1:
                    text = text.replace("*!repl!*", ":same")
                else:
                    text = text.replace("*!repl!*", "")
    return text


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


async def format_fill(event, text):
    first_name = last_name = ""
    if event.sender.first_name:
        first_name = ((event.sender.first_name).replace("<", "&lt;")).replace(
            ">", "&gt;"
        )
    if event.sender.last_name:
        last_name = ((event.sender.last_name).replace("<", "&lt;")).replace(">", "&gt;")
    if last_name:
        full_name = first_name + last_name
    else:
        full_name = first_name
    user_id = event.sender_id
    title = event.chat.title
    chat_id = event.chat_id
    chat_username = event.chat.username
    username = event.sender.username
    mention = f'<a href="tg://user?id={user_id}">{full_name}</a>'
    try:
        text = text.format(
            first=first_name,
            last=last_name,
            fullname=full_name,
            id=user_id,
            chattitle=title,
            chat_id=chat_id,
            chat_username=chat_username,
            username=username,
            mention=mention,
        )
    except KeyError:
        return text
    return text


# -----CAPTCHA-----
number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
alphabet_lowercase = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
alphabet_uppercase = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]


def gen_captcha_text(max_limit=4):
    captcha_string_list = []
    base_char = alphabet_lowercase + alphabet_uppercase + number_list
    for i in range(max_limit):
        char = choice(base_char)
        captcha_string_list.append(char)
    captcha_string = ""
    for item in captcha_string_list:
        captcha_string += str(item)
    return captcha_string


def gen_captcha(mode="text"):
    generator = CaptchaGenerator(13)
    if mode == "text":
        captcha_total = generator.gen_captcha_image(2, "hex", choice([True, False]))
        captcha = captcha_total[
            "image"
        ]
        captcha.save("captcha.png")
        return "captcha.png", captcha_total["characters"]
    elif mode == "math":
        captcha_total = generator.gen_math_captcha_image(2, False, True, False)
        (captcha_total["image"]).save("captcha.png")
        return "captcha.png", captcha_total["equation_result"]

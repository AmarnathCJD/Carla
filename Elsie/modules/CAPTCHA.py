from asyncio import sleep
from random import shuffle

from telethon import Button, events

import Elsie.modules.sql.captcha_sql as sql
from Elsie.events import Cbot

from . import (
    button_parser,
    can_change_info,
    extract_time,
    g_time,
    gen_math_question,
    math_captcha_pic,
    rand_no,
)

onn = """
Users will be asked to complete a CAPTCHA before being allowed to speak in the chat.

To change this setting, try this command again followed by one of yes/no/on/off
"""
offf = """
Users will NOT be muted when joining the chat.

To change this setting, try this command again followed by one of yes/no/on/off
"""
ca_on = """
I am currently kicking users that haven't completed the CAPTCHA after {}.

To change this setting, try this command again followed by one of yes/no/on/off
"""
ca_off = """
Users that don't complete their CAPTCHA are allowed to stay in the chat, muted, and can complete the CAPTCHA whenever.

To change this setting, try this command again followed by one of yes/no/on/off
"""
smdd = """
Users will stay muted until they use the CAPTCHA.

To change the CAPTCHA mute time, try this command again with a time value.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
sudd = """
If users haven't unmuted themselves after {}, they will be unmuted automatically.

To change the CAPTCHA mute time, try this command again with a time value.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
ca_ot = """
Users that don't complete their CAPTCHA are allowed to stay in the chat, muted, and can complete the CAPTCHA whenever.

To change the CAPTCHA kick time, try this command again with a time value.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
ca_time = """
I am currently kicking users that haven't completed the CAPTCHA after {}.

To change the CAPTCHA kick time, try this command again with a time value.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
caut = """
That isn't a valid time - '{}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
bu_h = """
The current CAPTCHA mode is: button
Button CAPTCHAs simply require a user to press a button in their welcome message to confirm they're human.

Available CAPTCHA modes are: button/math/text
"""
tx_h = """
The current CAPTCHA mode is: text
Text CAPTCHAs require the user to answer a CAPTCHA containing letters and numbers.

Available CAPTCHA modes are: button/math/text
"""
mt_h = """
The current CAPTCHA mode is: math
Math CAPTCHAs require the user to solve a basic maths question. Please note that this may discriminate against users with little maths knowledge.

Available CAPTCHA modes are: button/math/text
"""


pos = ["on", "y", "yes"]
neg = ["off", "n", "no"]


@Cbot(pattern="^/captcha ?(.*)")
async def _(event):
    if (
        event.text.startswith("!captchakick")
        or event.text.startswith("/captchakick")
        or event.text.startswith("?captchakick")
        or event.text.startswith("!captchakicktime")
        or event.text.startswith("/captchakicktime")
        or event.text.startswith("?captchakicktime")
        or event.text.startswith("!captchatime")
        or event.text.startswith("?captchatime")
        or event.text.startswith("/captchatime")
        or event.text.startswith("/captchamode")
        or event.text.startswith("?captchamode")
        or event.text.startswith("!captchamode")
        or event.text == "!captchamode"
        or event.text == "?captchamode"
        or event.text == "/captchamode"
    ):
        return
    if event.is_private:
        return  # connect
    if not await can_change_info(event, event.sender_id):
        return
    settings = sql.get_mode(event.chat_id)
    args = event.pattern_match.group(1)
    if not args:
        if settings == True:
            await event.reply(onn)
        elif settings == False:
            await event.reply(offf)
    elif args in pos:
        await event.reply(
            "CAPTCHAs have been enabled. I will now mute people when they join."
        )
        sql.set_mode(event.chat_id, True)
    elif args in neg:
        await event.reply("CAPTCHAs have been disabled. Users can join normally.")
        sql.set_mode(event.chat_id, False)
    else:
        await event.reply(
            "That isn't a boolean - expected one of y/yes/on or n/no/off; got: {}".format(
                args
            )
        )


@Cbot(pattern="^/captchakick ?(.*)")
async def _(event):
    if (
        event.text.startswith("!captchakicktime")
        or event.text.startswith("?captchakicktime")
        or event.text.startswith("/captchakicktime")
    ):
        return
    if event.is_private:
        return  # connect
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(1)
    settings = sql.get_time(event.chat_id)
    if not args:
        if settings == False or settings == 0:
            await event.reply(ca_off)
        else:
            synctime = g_time(settings)
            await event.reply(ca_on.format(synctime))
    elif args in pos:
        if settings:
            synctime = g_time(settings)
        else:
            synctime = "5 Minutes"
            settings = 300
        await event.reply(
            f"I will now kick people that haven't solved the CAPTCHA after {synctime}."
        )
        sql.set_time(event.chat_id, settings)
    elif args in neg:
        await event.reply(
            "I will no longer kick people that haven't solved the CAPTCHA."
        )
        sql.set_time(event.chat_id, 0)
    else:
        await event.reply(
            "That isn't a boolean - expected one of y/yes/on or n/no/off; got: {args}"
        )


@Cbot(pattern="^/captchakicktime ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(1)
    settings = sql.get_time(event.chat_id)
    if not args:
        if settings == False or settings == 0:
            await event.reply(ca_ot)
        else:
            synctime = g_time(settings)
            await event.reply(ca_time.format(synctime))
    elif args:
        if len(args) == 1:
            return await event.reply(caut.format(args))
        time = await extract_time(event, args)
        if not time:
            return
        if time < 300 or time > 86400:
            return await event.reply(
                "The welcome kick time can only be between 5 minutes, and 1 day. Please choose another time."
            )
        await event.reply(f"Welcome kick time has been set to {args}.")
        sql.set_time(event.chat_id, time)


@Cbot(pattern="^/captchatime ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(1)
    settings = sql.get_unmute_time(event.chat_id)
    if not args:
        if settings == 0 or settings == False:
            await event.reply(smdd)
        else:
            value = g_time(settings)
            await event.reply(sudd.format(value))
    elif args:
        if len(args) == 1:
            return await event.reply(caut.format(args))
        time = await extract_time(event, args)
        if not time:
            return
        await event.reply(
            f"I will now mute people for {g_time(time)} when they join - or until they solve the CAPTCHA in the welcome message."
        )
        sql.set_unmute_time(event.chat_id, time)


@Cbot(pattern="^/captchamode ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(1)
    settings = sql.get_style(event.chat_id)
    if not args:
        if settings == False or settings == "button":
            await event.reply(bu_h)
        elif settings == "text":
            await event.reply(tx_h)
        elif settings == "math":
            await event.reply(mt_h)
    else:
        if not args in ["button", "math", "text"]:
            await event.reply(
                f"'{args}' is not a recognised CAPTCHA mode! Try one of: button/math/text"
            )
        else:
            text = f"CAPTCHA set to **{args}**\n"
            if args == "button":
                text += "\nButton CAPTCHAs simply require a user to press a button in their welcome message to confirm they're human."
            elif args == "math":
                text += "\nMath CAPTCHAs require the user to solve a basic maths question. Please note that this may discriminate against users with little maths knowledge."
            elif args == "text":
                text += "\nText CAPTCHAs require the user to answer a CAPTCHA containing letters and numbers."
            await event.reply(text)
            sql.set_style(event.chat_id, args)


async def captcha_to_welcome(event, text, file):
    style = sql.get_style(event.chat_id)
    await tbot.edit_permissions(event.chat_id, event.user_id, send_messages=False)
    chat_info = event.chat_id
    if event.chat.username:
      chat_info = event.chat.username
    if style in ["math", "text"]:
        text = (
            text
            + f" [Click here to prove human](btnurl://t.me/MissElsie_Bot?start=captcha_{chat_info}&{style})"
        )
        welcome_text, buttons = button_parser(text)
    else:
        welcome_text, buttons = button_parser(text)
        buttons.append(
            [
                Button.inline(
                    "Click to prove human",
                    data="humanv_{}&{}".format(event.chat_id, event.user_id),
                )
            ]
        )
    await event.reply(welcome_text, file=file, buttons=buttons, parse_mode="html")


@tbot.on(events.CallbackQuery(pattern=r"humanv(\_(.*))"))
async def dcfd_fed(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    user_id = int(data.split("_", 1)[1])
    if not event.sender_id == user_id:
        return await event.answet("You are the not the user to be verified.")
    try:
        await tbot.edit_permissions(event.chat_id, event.sender_id, send_messages=True)
    except:
        pass
    await event.answer("Verified.")


@Cbot(pattern="^/start captcha_(.*)&(.*)")
async def kek(event):
    chat_info = event.pattern_match.group(1)
    style = event.pattern_match.group(2)
    if style == "math":
        await math_captcha(event, chat_info, event.sender_id)
    elif style == "text":
        await text_captcha(event, chat_info, event.sender_id)

box = 3

async def math_captcha(event, chat_info, user_id):
    question, answer = gen_math_question()
    no1, no2, no3, no4, no5, no6, no7, no8 = rand_no()
    pic = math_captcha_pic(question)
    buttons = []
    A = [
        Button.inline("{}".format(no1), data="ca_{}".format(no1)),
        Button.inline("{}".format(no2), data="ca_{}".format(no2)),
        Button.inline("{}".format(no3), data="ca_{}".format(no3)),
    ]
    B = [
        Button.inline("{}".format(no4), data="ca_{}".format(no4)),
        Button.inline("{}".format(answer), data="cca_{}".format(chat_info)),
        Button.inline("{}".format(no5), data="ca_{}".format(no5)),
    ]
    C = [
        Button.inline("{}".format(no6), data="ca_{}".format(no6)),
        Button.inline("{}".format(no7), data="ca_{}".format(no7)),
        Button.inline("{}".format(no8), data="ca_{}".format(no8)),
    ]
    shuffle(A)
    shuffle(B)
    shuffle(C)
    buttons.append(A)
    buttons.append(B)
    buttons.append(C)
    shuffle(buttons)
    await sleep(0.1)
    global box
    box = 3
    await event.respond(
        f"Click the correct answer to get verified.\nYou have {box} chances left.",
        buttons=buttons,
        file=pic,
    )

@tbot.on(events.CallbackQuery(pattern="cca(\_(.*))"))"))
async def kek(event):
  tata = event.pattern_match.group(1)
  data = tata.decode()
  chat_info = data.split("_", 1)[1]
  buttons = Button.url("Return to chat", f"t.me/{chat_info}")
  if str(chat_info).isdigit():
    chat_info = int(chat_info)
    buttons = None
  await event.edit("Congratulations, you've passed the CAPTCHA. You've been unmuted in the chat.", buttons=buttons)
  try:
   await tbot.edit_permissions(chat_info, event.sender_id, send_messages=True)
  except:
   pass

# fix error
# soon will fix
# soon
# fix final message not going

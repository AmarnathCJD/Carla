import Jessica.modules.sql.chatbot_sql as sql
from Jessica import tbot
from Jessica.events import Cbot

BOT_ID = 1766741237
from requests import get
from telethon import events

from . import can_change_info

url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"


@Cbot(pattern="^/chatbot ?(.*)")
async def cb(event):
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    args = event.pattern_match.group(1)
    if not args:
        mode = sql.chatbot_mode(event.chat_id)
        if mode:
            await event.reply("AI chatbot is currently **enabled** for this chat.")
        else:
            await event.reply("AI chatbot is currently **disabled** for this chat.")
    elif args in ["on", "y", "yes"]:
        await event.reply("**Enabled** AI chatbot for this chat.")
        sql.set_chatbot_mode(event.chat_id, True)
    elif args in ["off", "n", "no"]:
        await event.reply("**Disabled** AI chatbotfor this chat.")
        sql.set_chatbot_mode(event.chat_id, False)
    else:
        await event.reply("Your input was not recognised as one of: yes/no/y/n/on/off")


@tbot.on(events.NewMessage(pattern=None))
async def cb_tr(event):
    if not sql.chatbot_mode(event.chat_id):
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        if not msg.sender_id == BOT_ID:
            return
    elif "Jessica" in event.text:
        pass
    elif "Jessica" in event.text:
        pass
    elif "Evie" in event.text:
        pass
    else:
        return
    if (
        event.text.startswith(".")
        or event.text.startswith("!")
        or event.text.startswith("/")
        or event.text.startswith("?")
    ):
        return
    result = event.text
    for x in ["Evie", "Jessica", "Jessica"]:
        result = result.replace(x, "Aco")
    querystring = {
        "bid": "178",
        "key": "sX5A2PcYZbsN5EY6",
        "uid": "mashape",
        "msg": result,
    }
    headers = {
        "x-rapidapi-key": "cf9e67ea99mshecc7e1ddb8e93d1p1b9e04jsn3f1bb9103c3f",
        "x-rapidapi-host": "acobot-brainshop-ai-v1.p.rapidapi.com",
    }
    response = get(url, headers=headers, params=querystring)
    ans = response.json()["cnt"]
    ans = ans.replace("Acobot Team", "RoseLoverX")
    ans = ans.replace("Aco", "Jessica")
    await event.reply(ans)
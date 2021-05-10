from Carla import tbot, OWNER_ID
from . import can_change_info, ELITES
import re
from Carla.events import Cbot
import Carla.modules.sql.welcome_sql as sql
import Carla.modules.sql.captcha_sql as cas
from telethon import events, Button

wlc_st = """
I am currently welcoming users: `{}`
I am currently deleting old welcomes: `{}`
I am currently deleting service messages: `True`
CAPTCHAs are `{}`.
"""
pos = ['yes', 'y', 'on']
neg = ['n', 'no', 'off']

@Cbot(pattern="^/welcome ?(.*)")
async def _(event):
 if event.is_private:
   return
 if not await can_change_info(event, event.sender_id):
   return
 args = event.pattern_match.group(1)
 if not args:
  bstr = 'False'
  welc = str(sql.is_chat(event.chat_id))
  cws = sql.get_current_welcome_settings(event.chat_id)
  if cws:
   if cws.should_clean_welcome is True:
    bstr = 'True'
  mode = str(cas.get_mode(event.chat_id))
  await event.reply(wlc_st.format(welc, bstr, mode))
 elif args in pos:
  await event.reply("I'll be welcoming all new members from now on!")
  sql.add_c(event.chat_id)
 elif args in neg:
  await event.reply("I'll stay quiet when new members join.")
  sql.rmc(event.chat_id)
 else:
  await event.reply("Your input was not recognised as one of: yes/no/on/off")

@tbot.on(events.ChatAction())
async def _(event):
 if not event.user_joined:
  return
 if not sql.is_chat(event.chat_id):
  return
 if cas.get_mode(event.chat_id) == True:
  return
 cws = sql.get_current_welcome_settings(event.chat_id)
 if not cws:
  return await event.reply(f"Hey {event.user.first_name}, Welcome to {event.chat.title}! How are you?")
 user_id = event.user_id
 chattitle = event.chat.title
 first_name = event.user.first_name
 last_name = event.user.last_name
 username = event.user.username
 fullname = first_name
 if last_name:
  fullname = first_name + " " + last_name
 chat_id = event.chat_id
 mention = "[{first_name}](tg://user?id={user_id})"
 current_saved_welcome_message = None
 current_saved_welcome_message = cws.custom_welcome_message
 if "|" in current_saved_welcome_message:
  current_saved_welcome_message, button = current_saved_welcome_message.split("|")
  current_saved_welcome_message = current_saved_welcome_message.strip()
  button = button.strip()
  if "•" in button:
   mbutton = button.split("•")
   lbutton = []     
   for i in mbutton:
     params = re.findall(r"\'(.*?)\'", i) or re.findall(r"\"(.*?)\"", i)
     lbutton.append(params)
     butto = []
     for c in lbutton:
        smd = [Button.url(*c)]
        butto.append(smd)
  else:
    params = re.findall(r"\'(.*?)\'", button) or re.findall(r"\"(.*?)\"", button)
    butto = [Button.url(*params)]
 gulambi = current_saved_welcome_message.format(
                                mention=mention,
                                chattitle=chattitle,
                                first=first_name,
                                last=last_name,
                                fullname=fullname,
                                userid=user_id,
                                username=username,
                            )
 try:
   reply_msg = await event.reply(gulambi, parse_mode='html', buttons=bnt, file=cws.media_file_id)
 except:
   reply_msg = await event.reply(gulambi, parse_mode='html', buttons=None, file=cws.media_file_id)

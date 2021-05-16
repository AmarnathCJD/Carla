from Carla import tbot
from Carla.events import Cbot
from . import can_del_msg, db
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon import events, Button
import asyncio


purgex = db.purge
def get_id(id):
    return purgex.find_one({"id": id})

@Cbot(pattern="^/purge ?(.*)")
async def pugre(event):
 if event.text.startswith("!purgefrom") or event.text.startswith("/purgefrom") or event.text.startswith("?purgefrom") or event.text.startswith("!purgeto") or event.text.startswith("?purgeto") or event.text.startswith("/purgeto"):
    return
 lt = event.pattern_match.group(1)
 if lt:
   if not lt.isdigit():
      lt = None
 if lt:
   limit = lt
 else:
   limit = 1000
 if event.is_group:
   if not await can_del_msg(event, event.sender_id):
       return
 if not event.reply_to_msg_id:
  return await event.reply("Reply to a message to show me where to purge from.")
 reply_msg = await event.get_reply_message()
 messages = []
 message_id = reply_msg.id
 delete_to = event.message.id
 messages.append(event.reply_to_msg_id)
 for msg_id in range(message_id, delete_to + 1):
   messages.append(msg_id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")
 x = await event.respond("Purge complete!")
 await asyncio.sleep(4)
 await x.delete()

@Cbot(pattern="^/purgefrom$")
async def lil(event):
 if event.is_group:
   if not await can_del_msg(event, event.sender_id):
       return
 if not event.reply_to_msg_id:
  return await event.reply("Reply to a message to mark for purge.")
 reply_msg = await event.get_reply_message()
 msg_id = reply_msg.id
 chats = purgex.find({})
 for c in chats:
  if event.chat_id == c["id"]:
    to_check = get_id(id=event.chat_id)
    purgex.update_one(
           {
              "_id": to_check["_id"],
              "id": to_check["id"],
              "msg_id": to_check["msg_id"],
            },
             {"$set": {"msg_id": msg_id}},
            )
    return await event.respond("Message marked for deletion. Reply to another message with /purgeto to delete all messages in between.", reply_to=msg_id)
 purgex.insert_one(
        {"id": event.chat_id, "msg_id": msg_id}
    )
 await event.respond("Message marked for deletion. Reply to another message with /purgeto to delete all messages in between.", reply_to=msg_id)

@Cbot(pattern="^/purgeto$")
async def lilz(event):
 if event.is_group:
   if not await can_del_msg(event, event.sender_id):
       return
 if not event.reply_to_msg_id:
  return await event.reply("Reply to a message to purge till.")
 reply_msg = await event.get_reply_message()
 to_id = reply_msg.id
 msg_id = None
 chats = purgex.find({})
 for c in chats:
  if event.chat_id == c["id"]:
    msg_id = c["msg_id"]
 if msg_id == None:
   return await event.reply("You can only use this command after having used the /purgefrom command.")
 messages = []
 limit = 1000
 delete_to = event.reply_to_msg_id
 messages.append(event.reply_to_msg_id)
 for id in range(msg_id, delete_to + 1):
   messages.append(id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")
 chats = purgex.find({})
 for c in chats:
   if event.chat_id == c["id"]:
     purgex.delete_one({"id": event.chat_id})

@Cbot(pattern="^/spurge ?(.*)")
async def b(event):
 lt = event.pattern_match.group(1)
 if lt:
   if not lt.isdigit():
      lt = None
 if lt:
   limit = lt
 else:
   limit = 1000
 if event.is_group:
   if not await can_del_msg(event, event.sender_id):
       return
 if not event.reply_to_msg_id:
  return await event.reply("Reply to a message to show me where to purge from.")
 reply_msg = await event.get_reply_message()
 messages = []
 message_id = reply_msg.id
 delete_to = event.message.id
 messages.append(event.reply_to_msg_id)
 for msg_id in range(message_id, delete_to + 1):
   messages.append(msg_id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")

@Cbot(pattern="^/delall$")
async def kek(event):
 print(6)

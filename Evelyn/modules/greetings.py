import Evelyn.modules.mongodb.welcome_db as db
from . import can_change_info
from telethon import types

def get_fileids(r_msg):
  if isinstance(r_msg.media, types.MessageMediaDocument):
     file_id = r_msg.media.document.id
     access_hash = r_msg.media.document.access_hash
     file_reference = r_msg.media.document.file_reference
     type = "doc"
  elif isinstance(r_msg.media, types.MessageMediaPhoto):
     file_id = r_msg.file.id
     access_hash = None
     file_reference = None
     type = "photo"
  else:
     return None, None, None, None
  return file_id, access_hash, file_reference, type

@Cbot(pattern="^/setwelcome ?(.*)")
async def set_welxome(event):
 if event.is_private:
   return await event.reply("nope")
 if not event.from_id:
   return await a_welcome(event, "setwelcome")
 if event.is_group:
   if not await can_change_info(event, event.sender_id):
       return
 if not event.reply_to and not event.pattern_match.group(1):
       return await event.reply("You need to give the welcome message some content!")
 elif event.reply_to:
   r_msg = await event.get_reply_message()
   id, hash, ref, type = get_fileids(r_msg)
   if r_msg.text:
     r_text = r_msg.text
   else:
     r_text = None
   if r_msg.reply_markup:
     r_text = r_text + get_reply_msg_btns_text(r_msg)
 elif event.pattern_match.group(1):
  id = hash = ref = type = None
  r_text = event.text.split(None, 1)[1]
 await event.reply("The new welcome message has been saved!")
 db.set_welcome(event.chat_id, r_text, id, hash, ref, type, True)

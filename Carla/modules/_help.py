from Carla import tbot
from Carla.events import Cbot
from Carla import CMD_LIST
from telethon import Button

string = "Contact me in PM for help!"

f_button = [Button.inline("Fed Admin Commands", data="f_ad"), Button.inline("Fed Owner Commands", data="f_ow")], [Button.inline("User Commands", data="f_us")], [Button.inline("Back", data="go_back")]
c_button = Button.inline("Back", data="go_back")
bl_button = [Button.inline('Blocklist Command Examples', data='bl_cmd')], [Button.inline("Back", data="go_back")]
welcome = """
**Greetings**

Give your members a warm welcome with the greetings module! Or a sad goodbye... Depends!

**Admin commands:**
- /welcome <yes/no/on/off>: Enable/disable welcomes messages.
- /goodbye <yes/no/on/off>: Enable/disable goodbye messages.
- /setwelcome <text>: Set a new welcome message. Supports markdown, buttons, and fillings.
- /resetwelcome: Reset the welcome message.
- /setgoodbye <text>: Set a new goodbye message. Supports markdown, buttons, and fillings.
- /resetgoodbye: Reset the goodbye message.
- /cleanservice <yes/no/on/off>: Delete all service messages. Those are the annoying 'x joined the group' notifications you see when people join.
- /cleanwelcome <yes/no/on/off>: Delete old welcome messages. When a new person joins, or after 5 minutes, the previous message will get deleted.

**Examples:**
- Get the welcome message without any formatting
-> /welcome noformat
"""
wlc_btn = [Button.inline("CAPTCHA", data='captcha'), Button.inline('Formatting', data='formatting')], [Button.inline('Back', data="go_back")]
antiflood = """
**Antiflood**

You know how sometimes, people join, send 100 messages, and ruin your chat? With antiflood, that happens no more!

Antiflood allows you to take action on users that send more than x messages in a row. Actions are: ban/kick/mute/tban/tmute

Admin commands:
- /flood: Get the current antiflood settings
- /setflood <number/off/no>: Set the number of messages after which to take action on a user. Set to '0', 'off', or 'no' to disable.
- /setfloodmode <action type>: Choose which action to take on a user who has been flooding. Options: ban/kick/mute/tban/tmute
"""
blocklist = """
**Blocklists**

Want to stop people asking stupid questions? or ban anyone saying censored words? Blocklists is the module for you!

From blocking rude words, filenames/extensions, to specific emoji, everything is possible.

Admin commands:
- /addblocklist <blocklist trigger> <reason>: Add a blocklist trigger. You can blocklist an entire sentence by putting it in "quotes".
- /rmblocklist <blocklist trigger>: Remove a blocklist trigger.
- /unblocklistall: Remove all blocklist triggers - chat creator only.
- /blocklist: List all blocklisted items.
- /blocklistmode <blocklist mode>: Set the desired action to take when someone says a blocklisted item. Available: nothing/ban/mute/kick/warn/tban/tmute.
- /blocklistdelete <yes/no/on/off>: Set whether blocklisted messages should be deleted. Default: (on)
- /setblocklistreason <reason>: Set the default blocklist reason to warn people with.
- /resetblocklistreason: Reset the default blocklist reason to default - nothing.

Top tip:
Blocklists allow you to use some modifiers to match "unknown" characters. For example, you can use the ? character to match a single occurrence of any non-whitespace character.
You could also use the * modifier, which matches any number of any character. If you want to blocklist urls, this will allow you to match the full thing. It matches every character except spaces. This is cool if you want to block, for example, url shorteners.
"""
locks = """
**Locks**

Do stickers annoy you? or want to avoid people sharing links? or pictures? You're in the right place!

The locks module allows you to lock away some common items in the telegram world; the bot will automatically delete them!

**Admin commands:**
- /lock <item(s)>: Lock one or more items. Now, only admins can use this type!
- /unlock <item(s)>: Unlock one or more items. Everyone can use this type again!
- /locks: List currently locked items.
- /lockwarns <yes/no/on/off>: Enabled or disable whether a user should be warned when using a locked item.
- /locktypes: Show the list of all lockable items.
- /allowlist <url/id/@channelname(s)>: Allowlist a URL, group ID, channel @, or bot @ to stop them being deleted by URL, forward, invitelink, and inline locks. Separate with a space to add multiple items at once. If no arguments are given, returns the current allowlist.
- /rmallowlist <url/id/@channelname(s)>: Remove an item from the allowlist - url, invitelink, and forward locking will now take effect on messages containing it again. Separate with a space to remove multiple items.
- /rmallowlistall: Remove all allowisted items.

**Examples:**
- Lock stickers with:
-> /lock sticker
- You can lock/unlock multiple items by chaining them:
-> /lock sticker photo gif video
- To allow forwards from a specific channel, eg @CarlaSupport, you can allowlist it. You can also use the ID, or invitelink:
-> /allowlist @CarlaSupport
"""
fedz = """
**Federations**

Ah, group management. It's all fun and games, until you start getting spammers in, and you need to ban them. Then you need to start banning more, and more, and it gets painful.
But then you have multiple groups, and you don't want these spammers in any of your groups - how can you deal? Do you have to ban them manually, in all your groups?

No more! With federations, you can make a ban in one chat overlap to all your other chats.
You can even appoint federation admins, so that your trustworthiest admins can ban across all the chats that you want to protect.
"""
admin = """
**Admin**

Make it easy to promote and demote users with the admin module!

**Admin commands:**
- /promote <reply/username/mention/userid>: Promote a user.
- /demote <reply/username/mention/userid>: Demote a user.
- /adminlist: List the admins in the current chat
- /anonadmin <yes/no/on/off>: Allow anonymous admins to use all commands without checking their permissions. Not recommended.
"""
purge = """
**Purges**

Need to delete lots of messages? That's what purges are for!

**Admin commands:**
- /purge: Delete all messages from the replied to message, to the current message.
- /purge <X>: Delete the following X messages after the replied to message.
- /spurge: Same as purge, but doesnt send the final confirmation message.
- /del: Deletes the replied to message.
- /purgefrom: Reply to a message to mark the message as where to purge from - this should be used followed by a /purgeto.
- /purgeto: Delete all messages between the replied to message, and the message marked by the latest /purgefrom.

**Examples:**
- Delete all messages from the replied to message, until now.
-> /purge
- Mark the first message to purge from (as a reply).
-> /purgefrom
- Mark the message to purge to (as a reply). All messages between the previously marked /purgefrom and the newly marked /purgeto will be deleted.
-> /purgeto
"""
pin = """
**Pin**

All the pin related commands can be found here; keep your chat up to date on the latest news with a simple pinned message!

**User commands:**
- /pinned: Get the current pinned message.

**Admin commands:**
- /pin: Pin the message you replied to. Add 'loud' or 'notify' to send a notification to group members.
- /permapin <text>: Pin a custom message through the bot. This message can contain markdown, buttons, and all the other cool features.
- /unpin: Unpin the current pinned message. If used as a reply, unpins the replied to message.
- /unpinall: Unpins all pinned messages.
- /antichannelpin <yes/no/on/off>: Don't let telegram auto-pin linked channels. If no arguments are given, shows current setting.
- /cleanlinked <yes/no/on/off>: Delete messages sent by the linked channel.
"""

approve = """
**Approval**

Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blacklists, and antiflood not applying to them.

That's what approvals are for - approve of trustworthy users to allow them to send 

**Admin commands:**
- /approval: Check a user's approval status in this chat.

**Admin commands:**
- /approve: Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
- /unapprove: Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
- /approved: List all approved users.
- /unapproveall: Unapprove ALL users in a chat. This cannot be undone.
"""

@Cbot(pattern="^/help ?(.*)")
async def help(event):
 if not event.is_private:
  if event.pattern_match.group(1):
    module = event.pattern_match.group(1)
  else:
    module = "all"
  buttons = Button.url("Click me for help", "t.me/MissCarla_bot?start=help_{}".format(module))
  await event.reply(string, buttons=buttons)

@Cbot(pattern="^/start help_(.*)")
async def hh(event):
 plugin_name = (event.pattern_match.group(1)).lower()
 if plugin_name == 'welcome' or plugin_name == 'greetings':
   await event.reply(welcome, buttons=wlc_btn)
 elif plugin_name == 'antiflood' or plugin_name == 'antispam':
   await event.reply(antiflood, buttons=c_button)
 elif plugin_name == 'blocklist' or plugin_name == 'blacklist' or plugin_name == 'blocklists' or plugin_name == 'blacklists':
   await event.reply(blocklist, buttons=bl_button)
 elif plugin_name == 'lock' or plugin_name == 'locks':
   await event.reply(locks, buttons=c_button)
 elif plugin_name in ['fed', 'feds', 'federation', 'federations']:
   await event.reply(fedz, buttons=f_button)
 elif plugin_name in ['admin', 'admins']:
   await event.reply(admin, buttons=c_button)
 elif plugin_name in ['purge', 'purges', 'del', 'delete']:
   await event.reply(purge, buttons=c_button)
 elif plugin_name in ['pin', 'pins']:
   await event.reply(pin, buttons=c_button)
 elif plugin_name in ['approve', 'approval']:
   await event.reply(approve, buttons=c_button)

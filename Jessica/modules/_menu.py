from telethon import Button, events

from .. import CMD_HELP, tbot
from ..events import Cbot, Cinline

plugins = [
    "Admin",
    "AFK",
    "Approval",
    "AI-Chatbot",
    "Filters",
    "Greetings",
    "Locks",
    "Stickers",
    "Rules",
    "Song",
    "Reports",
    "Quotly",
    "Purges",
    "Pin",
    "Misc",
    "Inline",
    "    Force-Sub   ",
    "Federations",
    "Extras",
    "Bans",
    "Blocklist",
    "Antiflood",
    "CAPTCHA",
    "Warnings",
]

dps = [
    "https://telegra.ph/file/c6e1b8dffef90de602f52.jpg",
    "https://telegra.ph/file/75bf845ca6c731e7f0dc3.jpg",
]
help_caption = """
Hey! My name is NekoChan. I am a group management bot, here to help you get around and keep the order in your groups!
I have lots of handy features, such as flood control, a warning system, a note keeping system, and even predetermined replies on certain keywords.

**Helpful commands:**
- `/start`: Starts me! You've probably already used this.
- `/help`: Sends this message; I'll tell you more about myself!

If you have any bugs or questions on how to use me, have a look at @NekoChan_Updates.
 All commands can be used with the following: `/!?`
"""
advanced_caption = """
Hey **{}**, My name is Neko.

I'm here to help you to manage your groups.
I have lots of handy features such as:
‣ Warning system
‣ Artificial intelligence
‣ Flood control system
‣ Note keeping system
‣ Filters keeping system
‣ Approvals and much more.

So what are you waiting for?
Add me in your groups and give me full rights to make me function well.
"""
about = """
**Aʙᴏᴜᴛ Mᴇ**

Mʏ Nᴀᴍᴇ Is Nᴇᴋᴏ Cʜᴀɴ , A Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ Bᴏᴛ Wʜᴏ Cᴀɴ Tᴀᴋᴇ Cᴀʀᴇ Oғ Yᴏᴜʀ Gʀᴏᴜᴘs Wɪᴛʜ Aᴜᴛᴏᴍᴀᴛᴇᴅ Rᴇɢᴜʟᴀʀ Aᴅᴍɪɴ Aᴄᴛɪᴏɴs! 

**Mʏ Sᴏғᴛᴡᴀʀᴇ Vᴇʀsɪᴏɴ:** 1.0.5

**Mʏ Dᴇᴠᴇʟᴏᴘᴇʀs:**
• `@RoseLoverX`
• `@Itz_RexModz`

**Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ:** [Cʟɪᴄᴋ Hᴇʀᴇ](t.me/nekochan_updates)
**Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ:** [Cʟɪᴄᴋ Hᴇʀᴇ](t.me/nekochan_support)

__Aɴᴅ Fɪɴᴀʟʟʏ Sᴘᴇᴄɪᴀʟ Tʜᴀɴᴋs Oғ Gʀᴀᴛɪᴛᴜᴅᴇ Tᴏ Aʟʟ Mʏ Usᴇʀs Wʜᴏ Rᴇʟɪᴇᴅ Oɴ Mᴇ Fᴏʀ Mᴀɴᴀɢɪɴɢ Tʜᴇɪʀ Gʀᴏᴜᴘs , I Hᴏᴘᴇ Yᴏᴜ Wɪʟʟ Aʟᴡᴀʏs Lɪᴋᴇ Mᴇ ; Mʏ Dᴇᴠᴇʟᴏᴘᴇʀs Aʀᴇ Cᴏɴsᴛᴀɴᴛʟʏ Wᴏʀᴋɪɴɢ Tᴏ Iᴍᴘʀᴏᴠᴇ Mᴇ!__
"""
tc = """
**Tᴇʀᴍs Aɴᴅ Cᴏɴᴅɪᴛɪᴏɴs:**

- Oɴʟʏ Yᴏᴜʀ Usᴇʀ_Iᴅ Is Sᴛᴏʀᴇᴅ Fᴏʀ A Cᴏɴᴠᴇɴɪᴇɴᴛ Cᴏᴍᴍᴜɴɪᴄᴀᴛɪᴏɴ!
- Nᴏ Gʀᴏᴜᴘ Iᴅ Oʀ Iᴛs Mᴇssᴀɢᴇs Aʀᴇ Sᴛᴏʀᴇᴅ , Wᴇ Rᴇsᴘᴇᴄᴛ Eᴠᴇʀʏᴏɴᴇ's Pʀɪᴠᴀᴄʏ.
- Mᴇssᴀɢᴇs Bᴇᴛᴡᴇᴇɴ Bᴏᴛ Aɴᴅ Yᴏᴜ Is Oɴʟʏ IɴFʀᴏɴᴛ Oғ Yᴏᴜʀ Eʏᴇs Aɴᴅ Tʜᴇʀᴇ Is Nᴏ BᴀᴄᴋUsᴇ Oғ Iᴛ.
- Wᴀᴛᴄʜ Yᴏᴜʀ Gʀᴏᴜᴘ , Iғ Sᴏᴍᴇᴏɴᴇ Is Sᴘᴀᴍᴍɪɴɢ Yᴏᴜʀ Gʀᴏᴜᴘ , Yᴏᴜ Cᴀɴ Usᴇ Tʜᴇ Rᴇᴘᴏʀᴛ Fᴇᴀᴛᴜʀᴇ Oғ Yᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Cʟɪᴇɴᴛ.
- Dᴏ Nᴏᴛ Sᴘᴀᴍ Cᴏᴍᴍᴀɴᴅs , Bᴜᴛᴛᴏɴs , Oʀ Aɴʏᴛʜɪɴɢ Iɴ Bᴏᴛ Pᴍ

𝙉𝙊𝙏𝙀: Tᴇʀᴍs Aɴᴅ Cᴏɴᴅɪᴛɪᴏɴs Mɪɢʜᴛ Cʜᴀɴɢᴇ Aɴʏᴛɪᴍᴇ.

**Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ:** [Cʟɪᴄᴋ Hᴇʀᴇ](t.me/nekochan_updates)
**Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ:** [Cʟɪᴄᴋ Hᴇʀᴇ](t.me/nekochan_support)
"""
start_buttons = [
    [Button.url("Add to your Group ➕", "https://t.me/MissNeko_Bot?startgroup=true")],
    [
        Button.inline("Advanced ⭐", data="soon"),
        Button.url("Gban Logs 🌐", "t.me/NekoChan_Logs"),
    ],
    [Button.inline("Help and commands ❓", data="help_menu")],
]


@tbot.on(events.NewMessage(pattern=f"(?i)^[?+!/]start(@MissNeko_Bot)$"))
async def start(event):
    if event.is_group or event.is_channel:
        await event.reply("Hi there, I'm online ^_^")
    elif event.is_private:
        buttons = start_buttons
        await event.respond(
            advanced_caption.format(event.sender.first_name),
            buttons=buttons,
        )


@Cbot(pattern="^/help ?(.*)")
async def help(event):
    if event.is_group:
        buttons = [
            [Button.url("❔ Help", "https://t.me/MissNeko_Bot?start=_help")],
        ]
        await event.reply(
            "Contact me in PM to get the list of possible commands.",
            buttons=buttons,
        )
    elif event.is_private:
        buttons = paginate_help()
        await event.reply(help_caption, buttons=buttons)


@Cbot(pattern="^/start _help")
async def st_help(e):
    buttons = paginate_help()
    await e.respond(help_caption, buttons=buttons)


@Cinline(pattern=r"help_menu")
async def help_menu(event):
    buttons = paginate_help()
    await event.edit(help_caption, buttons=buttons)


@Cinline(pattern=r"us_plugin_(.*)")
async def us_0(event):
    pl_name = (event.pattern_match.group(1)).decode()
    try:
        pl_help = CMD_HELP[pl_name][1]
    except KeyError:
        pl_help = "The help menu for this module will be provided soon!"
    await event.edit(
        pl_help,
        buttons=[
            Button.inline("Home", data="soon"),
            Button.inline("Back", data="help_menu"),
        ],
    )


def paginate_help():
    helpable_plugins = sorted(plugins)
    modules = [
        Button.inline(x, data=f"us_plugin_{x.lower()}") for x in helpable_plugins
    ]
    pairs = list(
        zip(
            modules[::3],
            modules[1::3],
            modules[2::3],
        )
    )
    modulo_page = 0 % 1
    pairs = pairs[modulo_page * 8 : 8 * (modulo_page + 1)] + [
        (Button.inline("Back", data="soon"),)
    ]
    return pairs


@Cinline(pattern="soon")
async def soon(event):
    buttons = [
        [Button.url("Configuration Tutorial", "https://t.me/NekoChan_Updates/13")],
        [
            Button.inline("About Me", data="me_detail"),
            Button.inline("Commands", data="help_menu"),
        ],
        [Button.inline("Terms and Conditions", data="t&c")],
    ]
    await event.edit(
        advanced_caption.format(event.sender.first_name),
        buttons=buttons,
    )


@Cinline(pattern="me_detail")
async def me(e):
    buttons = Button.inline("Back", data="soon")
    await e.edit(about, buttons=buttons, link_preview=False)


@Cinline(pattern="t&c")
async def t_c(e):
    buttons = Button.inline("Back", data="soon")
    await e.edit(tc, buttons=buttons, link_preview=False)

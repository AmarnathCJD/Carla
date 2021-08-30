import math
import os
import random

import emoji
from PIL import Image
from telethon import Button
from telethon.errors.rpcerrorlist import (
    PackShortNameOccupiedError,
    StickerEmojiInvalidError,
    StickerPngNopngError,
)
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.stickers import (
    AddStickerToSetRequest,
    CreateStickerSetRequest,
    RemoveStickerFromSetRequest,
)
from telethon.tl.types import (
    DocumentAttributeSticker,
    InputDocument,
    InputStickerSetEmpty,
    InputStickerSetID,
    InputStickerSetItem,
    MaskCoords,
    MessageMediaPhoto,
)

from .. import OWNER_ID, tbot
from ..events import Cbot
from . import db

sticker_sets = db.sticker_packs
pkang = db.pack_kang


def get_emoji(v):
    p = "".join(c for c in v if c in emoji.UNICODE_EMOJI["en"])
    if len(p) != 0:
        return p[0]
    return None


@Cbot(pattern="^/kang ?(.*)")
async def kang(event):
    if not event.reply_to:
        return await event.reply("Please reply to a sticker, or image to kang it!")
    msg = await event.get_reply_message()
    if not msg.sticker and not isinstance(msg.media, MessageMediaPhoto):
        return await event.reply("Yeah, I can't kang that.")
    try:
        emoji = event.text.split(None, 1)[1]
        emoji = get_emoji(emoji) or ""
    except IndexError:
        try:
            emoji = msg.media.document.attributes[1].alt
        except:
            emoji = "😂"
    if emoji == "":
        emoji = random.choice(["😍", "😂", "🙅‍♀️"])
    if msg.sticker:
        mime_type = msg.media.document.mime_type
        if "application/x-tgsticker" in mime_type:
            return
        sticker_id_id = msg.media.document.id
        access_hash_id = msg.media.document.access_hash
        file_reference = msg.media.document.file_reference
    elif msg.media.photo:
        file = await tbot.download_media(msg)
        resize_image(file)
        sended = await tbot.send_message("RoseLoverX", file="sticker.webp")
        sticker_id_id = sended.media.document.id
        access_hash_id = sended.media.document.access_hash
        file_reference = sended.media.document.file_reference
        os.remove("sticker.webp")
        await sended.delete()
    short_name = f"ev{event.sender_id}_by_MissNeko_Bot"
    user_id = OWNER_ID
    if event.sender.first_name:
        title = f"{event.sender.first_name}'s Kang pack"
    else:
        title = f"{event.sender_id}'s Kang pack"
    if str((sticker_sets.find({"id": event.sender_id})).distinct("sticker_id")) == "[]":
        try:
            result = await tbot(
                CreateStickerSetRequest(
                    user_id=user_id,
                    title=title,
                    short_name=short_name,
                    stickers=[
                        InputStickerSetItem(
                            document=InputDocument(
                                id=sticker_id_id,
                                access_hash=access_hash_id,
                                file_reference=file_reference,
                            ),
                            emoji=emoji,
                            mask_coords=MaskCoords(n=42, x=7.13, y=7.13, zoom=7.13),
                        )
                    ],
                    masks=False,
                    animated=False,
                )
            )
        except StickerPngNopngError:
            return
        except StickerEmojiInvalidError:
            return await event.reply(
                f"Invalid emoji provided, '{event.pattern_match.group(1)}' is not an emoji."
            )
        except Exception as e:
            return await event.reply(str(e))
        txt = f"Sticker successfully added to <a href='http://t.me/addstickers/{short_name}'>pack</a>\nEmoji is: {emoji}"
        await event.reply(txt, parse_mode="html", link_preview=False)
        return sticker_sets.insert_one(
            {
                "id": event.sender_id,
                "sticker_id": result.set.id,
                "access_hash": result.set.access_hash,
            }
        )
    user_st = sticker_sets.find({"id": event.sender_id})
    sticker_id = user_st.distinct("sticker_id")[0]
    access_hash = user_st.distinct("access_hash")[0]
    try:
        result = await tbot(
            AddStickerToSetRequest(
                stickerset=InputStickerSetID(id=sticker_id, access_hash=access_hash),
                sticker=InputStickerSetItem(
                    document=InputDocument(
                        id=sticker_id_id,
                        access_hash=access_hash_id,
                        file_reference=file_reference,
                    ),
                    emoji=emoji,
                ),
            )
        )
    except StickerPngNopngError:
        return
    except StickerEmojiInvalidError:
        return await event.reply(
            f"Invalid emoji provided, '{event.pattern_match.group(1)}' is not an emoji."
        )
    except Exception as e:
        return await event.respond(str(e))
    txt = f"Sticker successfully added to <a href='http://t.me/addstickers/{result.set.short_name}'>pack</a>\nEmoji is: {emoji}"
    await event.reply(txt, parse_mode="html", link_preview=False)


@Cbot(pattern="^/(rmkang|unkang)$")
async def uk(event):
    if not event.reply_to_msg_id:
        return
    msg = await event.get_reply_message()
    if not msg.sticker:
        return await event.reply("Yeah, that's not a sticker!")
    sticker_id = msg.media.document.id
    access_hash = msg.media.document.access_hash
    file_reference = msg.media.document.file_reference
    try:
        result = await tbot(
            RemoveStickerFromSetRequest(
                sticker=InputDocument(
                    id=sticker_id,
                    access_hash=access_hash,
                    file_reference=file_reference,
                ),
            )
        )
        await event.reply(
            f"Sticker sucessfully removed from <a href='http://t.me/addstickers/{result.set.short_name}'>pack</a>",
            parse_mode="HTML",
        )
    except:
        await event.reply(
            "The provided sticker set is invalid or sticker pack not made by me!"
        )


def resize_image(image):
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    os.remove(image)
    im.save("sticker.webp")


@Cbot(pattern="^/mypac(k|ks) ?(.*)")
async def my_pack(e):
    if str((sticker_sets.find({"id": e.sender_id})).distinct("sticker_id")) == "[]":
        return await e.reply("You have not yet created any sticker packs!")
    user_st = sticker_sets.find({"id": e.sender_id})
    sticker_id = user_st.distinct("sticker_id")[0]
    access_hash = user_st.distinct("access_hash")[0]
    x = await tbot(
        GetStickerSetRequest(
            stickerset=InputStickerSetID(id=sticker_id, access_hash=access_hash)
        )
    )
    short_name = x.set.short_name
    await e.reply(
        f'Here is your kang <a href="http://t.me/addstickers/{short_name}">pack</a>.',
        parse_mode="html",
        link_preview=False,
    )


@Cbot(pattern="^/(pkang|packkang) ?(.*)")
async def pck_kang__(e):
    if not e.reply_to:
        return await e.reply("Reply to a sticker.")
    r = await e.get_reply_message()
    if not r.sticker:
        return await e.reply("That's not a sticker file.")
    if len(e.text.split(" ", 1)) == 2:
        pname = e.text.split(" ", 1)[1]
        emoji = get_emoji(pname)
        if emoji:
            pname = pname.replace(emoji)
    else:
        pname = f"{e.sender.first_name}'s PKang pack"
        emoji = None
    id = access_hash = None
    for x in r.sticker.attributes:
        if isinstance(x, DocumentAttributeSticker):
            if not isinstance(x.stickerset, InputStickerSetEmpty):
                id = x.stickerset.id
                access_hash = x.stickerset.access_hash
    if not (id or access_hash):
        return await e.reply("That sticker is not part of any pack to kang!")
    _stickers = await tbot(
        GetStickerSetRequest(
            stickerset=InputStickerSetID(id=id, access_hash=access_hash)
        )
    )
    stk = []
    if emoji:
        for x in _stickers.documents:
            stk.append(
                InputStickerSetItem(
                    document=InputDocument(
                        id=x.id,
                        access_hash=x.access_hash,
                        file_reference=x.file_reference,
                    ),
                    emoji=emoji,
                )
            )
    else:
        for x in _stickers.documents:
            stk.append(
                InputStickerSetItem(
                    document=InputDocument(
                        id=x.id,
                        access_hash=x.access_hash,
                        file_reference=x.file_reference,
                    ),
                    emoji=(x.attributes[1]).alt,
                )
            )
    pack = 1
    xp = pkang.find_one({"user_id": e.sender_id})
    if xp:
        pack = xp.get("pack") + 1
    pkang.update_one({"user_id": e.sender_id}, {"$set": {"pack": pack}}, upsert=True)
    pm = random.choice(["a", "b", "c", "d", "e", "f", "g"])
    try:
        p = await tbot(
            CreateStickerSetRequest(
                user_id=e.sender_id,
                title=pname,
                short_name=f"{pm}{e.sender_id}_{pack}_by_MissNeko_Bot",
                stickers=stk,
            )
        )
    except PackShortNameOccupiedError:
        pack += 1
        p = await tbot(
            CreateStickerSetRequest(
                user_id=e.sender_id,
                title=pname,
                short_name=f"{pm}{e.sender_id}_{pack}_by_MissNeko_Bot",
                stickers=stk,
            )
        )
    except Exception as ex:
        return await e.reply(str(ex))
    await e.reply(
        f"Sticker Set successfully Kanged to <b><a href='http://t.me/addstickers/{p.set.short_name}'>Pack</a></b>.",
        buttons=Button.url(
            "View Pack", url=f"http://t.me/addstickers/{p.set.short_name}"
        ),
        parse_mode="html",
    )


async def animated_sticker_kang(event, msg):
    print("ani kang")


# soon work on animated sticker

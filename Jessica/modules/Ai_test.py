from Jessica import ubot
from Jessica.events import Cbot


@Cbot(pattern="^/c ?(.*)")
async def cb(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    async with ubot.conversation("@KukiAI_bot") as chat:
        await chat.send_message(str(q))
        res = await chat.get_response()
        if res.text:
            await e.reply(res.text)
        elif res.media:
            re_re = await ubot.send_message(file=res.media)
            await e.reply(file=re_re.media)

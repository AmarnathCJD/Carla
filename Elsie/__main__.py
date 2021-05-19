from sys import exit
import Elsie.events # pylint:disable=E0602
from Elsie import TOKEN, tbot

try:
    tbot.start(bot_token=TOKEN)
except Exception:
    print("Token Invalid.")
    exit(1)


async def start_log():
    await tbot.send_message(-1001273171524, "**Bot Started!**")


tbot.loop.run_until_complete(start_log())
tbot.run_until_disconnected()

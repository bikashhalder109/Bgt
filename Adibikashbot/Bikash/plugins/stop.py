from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from Bikash import app
from Bikash.core.call import Bikashh
from Bikash.utils.database import set_loop
from Bikash.utils.decorators import AdminRightsCheck
from Bikash.utils.events.filters import command
from Bikash.utils.inline.play import close_keyboard

# Commands
STOP_COMMAND = get_command("STOP_COMMAND")


@app.on_message(
    command(STOP_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    await Bikashh.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_9"].format(message.from_user.first_name),
        reply_markup=close_keyboard,
    )

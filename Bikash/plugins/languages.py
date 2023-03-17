from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from config import BANNED_USERS
from strings import get_command, get_string
from Bikash import app
from Bikash.utils.database import get_lang, set_lang
from Bikash.utils.decorators import (ActualAdminCB, language,
                                         languageCB)

# Languages Available


def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.row(
        InlineKeyboardButton(
            text="🇦🇺 𝐄𝐧𝐠𝐥𝐢𝐬𝐡 🇦🇺",
            callback_data=f"languages:en",
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"], callback_data=f"close"
        ),
    )
    return keyboard


LANGUAGE_COMMAND = get_command("LANGUAGE_COMMAND")


@app.on_message(
    filters.command(LANGUAGE_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=keyboard
    )


@app.on_callback_query(
    filters.regex(r"languages:(.*?)") & ~BANNED_USERS
)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(langauge):
        return await CallbackQuery.answer(
            "𝐘𝐨𝐮'𝐫𝐞 𝐀𝐥𝐫𝐞𝐝𝐲 𝐔𝐬𝐢𝐧𝐠 𝐒𝐚𝐦𝐞 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞 𝐅𝐨𝐫 𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭.", show_alert=True
        )
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(
            "𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐂𝐡𝐚𝐧𝐠𝐞 𝐘𝐨𝐮𝐫 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞.", show_alert=True
        )
    except:
        return await CallbackQuery.answer(
            "𝐅𝐚𝐢𝐥𝐞𝐝 𝐓𝐨 𝐂𝐡𝐚𝐧𝐠𝐞 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞",
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=keyboard
    )

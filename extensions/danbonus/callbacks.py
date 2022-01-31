from aiogram.types import CallbackQuery, ParseMode
from aiogram.utils.markdown import hlink

from bot import main
from extensions.danbonus import markup

codes = {
    "8665788965": "shorturl.at/agjE1",
    "0451": "shorturl.at/huT01"
}


@main.dp.callback_query_handler(lambda cb: cb.data.startswith("keypad_erase"))
async def keypad_number_callback(cb: CallbackQuery):
    if cb.message.text == "-":
        return

    await cb.message.edit_text(text="-", reply_markup=markup.get_markup())


@main.dp.callback_query_handler(lambda cb: cb.data.startswith("keypad_submit"))
async def keypad_number_callback(cb: CallbackQuery):
    code = cb.message.text

    if code in codes:
        await cb.message.answer(f"Ты указал верный код! Он ведет к ссылке:\n{hlink('Ссылка', codes[code])}",
                                parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        await cb.message.answer("Неверный код!")

    await cb.message.delete()


@main.dp.callback_query_handler(lambda cb: cb.data.startswith("keypad_num_"))
async def keypad_number_callback(cb: CallbackQuery):
    await main.bot.answer_callback_query(cb.id)

    number = cb.data.split("_")[2][0]

    if not number.isdigit():
        return

    original_text = cb.message.text

    if original_text == "-" or len(original_text) == 10:
        original_text = ""

    original_text += number

    await cb.message.edit_text(text=original_text, reply_markup=markup.get_markup())

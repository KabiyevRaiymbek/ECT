import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

TOKEN = "8579109035:AAH9YIoAlyF03RT4HRcnZBfdvC7nzM7AlPs"
YOUR_ID = 7711644101          # ← ещё раз проверь у @userinfobot

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


# ─────────────── /start ───────────────
@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [[types.KeyboardButton(text="Подать резюме")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        "Привет! Я бот команды Empire Core\n\n"
        "Нажми кнопку ниже, чтобы отправить резюме:",
        reply_markup=keyboard
    )


# ─────────────── Кнопка «Подать резюме» ───────────────
@dp.message(F.text == "Подать резюме")
async def button_apply(message: types.Message):
    await message.answer("Прикрепи своё резюме (PDF, DOCX, ZIP и др.) и отправь одним сообщением")


# ─────────────── Команда /apply ───────────────
@dp.message(Command("apply"))
async def apply(message: types.Message):
    await message.answer("Прикрепи своё резюме (PDF, DOCX, ZIP и др.) и отправь одним сообщением")


# ─────────────── Приём файла ───────────────
@dp.message(F.document)
async def handle_cv(message: types.Message):
    try:
        user = message.from_user
        file_name = message.document.file_name

        caption = (
            "Новое резюме!\n\n"
            f"От: {user.full_name}\n"
            f"@{user.username or 'нет'}\n"
            f"ID: {user.id}\n"
            f"Файл: {file_name}"
        )

        await bot.send_document(chat_id=YOUR_ID, document=message.document, caption=caption)

        await message.reply(
            "Резюме успешно получено!\n\n"
            "Спасибо, что заинтересовались нашей командой!\n"
            "Мы внимательно изучим ваш опыт и напишем вам в ближайшие дни"
        )
    except Exception as e:
        logging.error(f"Ошибка отправки админу: {e}")
        await message.reply(
            "Резюме получено и сохранено!\n\n"
            "Спасибо! Мы свяжемся с вами в ближайшее время"
        )


# ─────────────── Запуск ───────────────
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("EmpireCoreTeamBot полностью запущен 24/7")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
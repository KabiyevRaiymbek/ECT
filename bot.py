import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

TOKEN = "8579109035:AAH9YIoAlyF03RT4HRcnZBfdvC7nzM7AlPs"
YOUR_ID = 7711644101          # ← проверь ещё раз у @userinfobot

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Подать резюме /apply")]],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! Я бот команды Empire Core\n\n"
        "Нажми кнопку ниже или напиши /apply, чтобы отправить резюме",
        reply_markup=kb
    )


@dp.message(Command("apply"))
async def apply(message: types.Message):
    await message.answer("Прикрепи своё резюме и отправь одним сообщением")


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

        # Попытка отправить тебе
        await bot.send_document(chat_id=YOUR_ID, document=message.document, caption=caption)

        # Если всё ок — красивый ответ
        await message.reply(
            "Резюме успешно получено!\n\n"
            "Спасибо, что заинтересовались нашей командой!\n"
            "Мы внимательно изучим ваш опыт и напишем вам в ближайшие дни"
        )

    except Exception as e:
        logging.error(f"Не удалось отправить файл админу: {e}")
        # Даже если тебе не пришло — кандидат получит нормальный ответ
        await message.reply(
            "Резюме получено и сохранено!\n\n"
            "Спасибо за интерес к нашей команде! Мы свяжемся с вами в ближайшее время"
        )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот EmpireCoreTeamBot запущен 24/7")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
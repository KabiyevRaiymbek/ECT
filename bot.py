import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

TOKEN = "8579109035:AAH9YIoAlyF03RT4HRcnZBfdvC7nzM7AlPs"
YOUR_ID = 7711644101

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
print("Бот EmpireCoreTeamBot запущен и работает!")


@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Подать резюме /apply")]],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! Я бот команды Empire Core Team\n\n"
        "Нажми кнопку ниже или напиши /apply, чтобы отправить резюме",
        reply_markup=keyboard
    )


@dp.message(Command("apply"))
async def apply(message: types.Message):
    await message.answer("Прикрепи своё резюме и отправь одним сообщением")


# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# САМЫЙ ВАЖНЫЙ БЛОК — с try/except и явным ответом
@dp.message(F.document)
async def handle_cv(message: types.Message):
    try:
        user = message.from_user
        file_name = message.document.file_name

        caption = (
            "Новое резюме в Empire Core!\n\n"
            f"От: {user.full_name}\n"
            f"@{user.username or 'нет'}\n"
            f"ID: {user.id}\n"
            f"Файл: " + file_name
        )

        # Отправляем тебе
        await bot.send_document(7711644101, message.document, caption=caption)

        # Отвечаем кандидату — теперь точно дойдёт
        await message.reply(
            "Резюме успешно получено!\n\n"
            "Спасибо, что заинтересовались нашей командой!\n"
            "Мы внимательно изучим ваш опыт и напишем вам в ближайшие дни"
        )

    except Exception as e:
        logging.error(f"Ошибка при обработке файла: {e}")
        await message.reply("Произошла ошибка при отправке. Попробуйте позже.")


async def main():
    webhook = await bot.get_webhook_info()
    if webhook.url:
        await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook удалён")

    print("Бот EmpireCoreTeamBot запущен и работает 24/7!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
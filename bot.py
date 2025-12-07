import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# ─────── ТВОИ ДАННЫЕ (уже вставлены) ───────
TOKEN = "8579109035:AAH9YIoAlyF03RT4HRcnZBfdvC7nzM7AlPs"
YOUR_ID = 7711644101          # сюда приходят все резюме
# ───────────────────────────────────────────────

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
print("Бот EmpireCoreTeamBot запущен и работает!")


@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Подать резюме /apply"))
    await message.answer(
        "Привет! Я бот команды Empire Core\n\n"
        "Нажми кнопку ниже или напиши /apply, чтобы отправить резюме",
        reply_markup=keyboard
    )


@dp.message(Command("apply"))
async def apply(message: types.Message):
    await message.answer(
        "Прикрепи своё резюме (PDF, DOCX, ZIP и любые другие файлы) "
        "и отправь одним сообщением ↓"
    )


@dp.message(F.document)
async def handle_cv(message: types.Message):
    user = message.from_user
    file_name = message.document.file_name

    caption = (
        "Новое резюме!\n\n"
        f"От: {user.full_name}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}\n"
        f"Файл: {file_name}"
    )

    await bot.send_document(chat_id=YOUR_ID, document=message.document, caption=caption)
    await message.answer("Резюме получено! Скоро свяжемся")


async def main():
    # Автоматически убираем старый webhook, если он был
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url:
        await bot.delete_webhook(drop_pending_updates=True)
        print("Старый webhook удалён")

    print("Бот EmpireCoreTeamBot запущен и работает 24/7!")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
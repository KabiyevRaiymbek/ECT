import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8579109035:AAH9YIoAlyF03RT4HRcnZBfdvC7nzM7AlPs"
YOUR_ID = 771164           # ← твой ID (проверь через @userinfobot)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO)


# Состояния FSM
class ApplyForm(StatesGroup):
    waiting_for_text_cv = State()


# Текст инструкции
INSTRUCTION_TEXT = (
    "Спасибо за интерес к нашей команде! 🚀\n\n"
    "Мы не принимаем резюме в виде файлов (docx, pdf и т.д.).\n"
    "Пожалуйста, ответьте текстом в одном сообщении на следующие вопросы:\n\n"
    "1. Как вы нашли нас?\n"
    "2. Какой опыт работы в серой сфере?\n"
    "3. Какой опыт работы с криптой?\n"
    "4. Сколько лет в этой сфере?\n"
    "5. Какие навыки у вас есть?\n"
    "6. Какой у вас опыт в трафике? (источники, объёмы, профит и т.д.)\n"
    "7. На каких языках можете говорить?\n"
    "8. Сколько времени готовы уделять работе в день?\n"
    "9. Если у вас есть доказательства опыта (скрины статистики, кейсы, источники трафика и т.д.) — прикрепите изображения к этому же сообщению.\n\n"
    "Отправьте всё одним сообщением — мы рассмотрим и свяжемся с вами в ближайшее время! 😊"
)


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Подать резюме /apply")]],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! Я бот команды Empire Core Team 👋\n\n"
        "Мы ищем сильных специалистов в арбитраже трафика.\n"
        "Нажми кнопку ниже или напиши /apply, чтобы подать заявку.",
        reply_markup=kb
    )


@dp.message(F.text.lower() == "подать резюме /apply" or Command("apply"))
async def apply_command(message: types.Message, state):
    await state.set_state(ApplyForm.waiting_for_text_cv)
    await message.answer(
        INSTRUCTION_TEXT,
        reply_markup=types.ReplyKeyboardRemove()  # убираем кнопку, чтобы не мешала
    )


@dp.message(ApplyForm.waiting_for_text_cv)
async def handle_text_cv(message: types.Message, state):
    user = message.from_user
    text = message.text or "Без текста (только фото?)"

    # Формируем сообщение для тебя (админа)
    admin_message = (
        "🔔 Новая заявка в Empire Core!\n\n"
        f"От: {user.full_name}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}\n\n"
        f"Текст заявки:\n{text}"
    )

    # Если есть фото — пересылаем их тоже
    if message.photo:
        await bot.send_message(chat_id=YOUR_ID, text=admin_message)
        for photo in message.photo:
            await bot.send_photo(chat_id=YOUR_ID, photo=photo.file_id, caption="Скрин/доказательство от кандидата")
    else:
        await bot.send_message(chat_id=YOUR_ID, text=admin_message)

    # Ответ кандидату
    await message.answer(
        "✅ Заявка успешно получена!\n\n"
        "Спасибо за подробный ответ! Мы внимательно изучим ваш опыт и свяжемся с вами в ближайшие дни."
    )

    # Сбрасываем состояние
    await state.clear()


# Если прислали документ — напоминаем, что нужен текст
@dp.message(F.document)
async def handle_document(message: types.Message):
    await message.answer(
        "🚫 Мы не принимаем резюме в виде файлов.\n\n"
        "Пожалуйста, используйте кнопку ниже или команду /apply и отправьте информацию текстом по предложенному шаблону."
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот EmpireCoreTeamBot запущен 24/7")
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())

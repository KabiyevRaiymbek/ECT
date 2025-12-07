    import asyncio
    import logging
    from aiogram import Bot, Dispatcher, types, F
    from aiogram.filters import Command
    
    TOKEN = "8579109035:AAH9YIoAlyF03RT4HRcnZBfdvC7nzM7AlPs"
    YOUR_ID = 7711644101          # ← если @userinfobot показал другой — поменяй
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    logging.basicConfig(level=logging.INFO)
    
    
    @dp.message(Command("start"))
    async def start(message: types.Message):
        # Одна чистая кнопка «Подать резюме»
        kb = [[types.KeyboardButton(text="Подать резюме")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Привет! Я бот команды Empire Core\n\n"
            "Нажми кнопку ниже, чтобы отправить резюме:",
            reply_markup=keyboard
        )
    
    
    # Ловим нажатие кнопки
    @dp.message(F.text == "Подать резюме")
    async def from_button(message: types.Message):
        await message.answer("Прикрепи своё резюме (PDF, DOCX, ZIP и др.) и отправь одним сообщением")
    
    
    # Ловим прямую команду (на всякий случай)
    @dp.message(Command("apply"))
    async def apply(message: types.Message):
        await message.answer("Прикрепи своё резюме (PDF, DOCX, ZIP и др.) и отправь одним сообщением")
    
    
    # Приём файла
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
    
            await bot.send_document(YOUR_ID, message.document, caption=caption)
    
            await message.reply(
                "Резюме успешно получено!\n\n"
                "Спасибо, что заинтересовались нашей командой!\n"
                "Мы внимательно изучим ваш опыт и напишем вам в ближайшие дни"
            )
    
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            await message.reply(
                "Резюме получено!\n\nСпасибо, мы скоро свяжемся с вами"
            )
    
    
    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        print("Бот запущен 24/7")
        await dp.start_polling(bot)
    
    
    if __name__ == "__main__":
        asyncio.run(main())
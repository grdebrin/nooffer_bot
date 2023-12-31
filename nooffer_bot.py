import telegram
from telegram.ext import Updater, CommandHandler
import random
from datetime import datetime, time
import pytz

# Укажите ваш токен бота Telegram
TOKEN = 'YOUR_TOKEN'

# Путь к файлу с текстом
TEXT_FILE_PATH = 'text.txt'

# Создаем экземпляр бота
bot = telegram.Bot(token=TOKEN)

# Словарь для хранения chat_id пользователей
user_chat_ids = {}

# Получаем случайную фразу из файла
def get_random_phrase():
    with open(TEXT_FILE_PATH, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n\n')
        return random.choice(lines)

# Обработчик команды /start
def start(update, context):
    chat_id = update.effective_chat.id
    user_chat_ids[chat_id] = True  # Сохраняем chat_id пользователя в словаре
    context.bot.send_message(chat_id=chat_id, text=f"Привет, {update.effective_user.first_name}! Я бот, который каждый день в 09:00 (GMT+3) буду отправлять тебе слова поддержки, пока ты ищешь работу!")

# Функция для отправки фразы каждый день в 09:00 по московскому времени
def send_daily_phrase(context):
    phrase = get_random_phrase()
    for chat_id in user_chat_ids.keys():
        bot.send_message(chat_id=chat_id, text=phrase)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Устанавливаем время для выполнения задачи каждый день в 09:00 по московскому времени
    job_queue = updater.job_queue
    moscow_tz = pytz.timezone('Europe/Moscow')
    job_queue.run_daily(send_daily_phrase, time(hour=9, minute=0, tzinfo=moscow_tz))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
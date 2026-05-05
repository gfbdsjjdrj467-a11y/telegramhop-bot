import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ID премиум эмодзи
PREMIUM_EMOJI_ID = "5440431182602842059"

# Словарь для отслеживания статистики
user_stats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Инициализируем статистику для пользователя
    if user_id not in user_stats:
        user_stats[user_id] = {'count': 0, 'joined_at': datetime.now()}
    
    # Создаем кнопки
    keyboard = [
        [KeyboardButton("📨 Отправить эмодзи")],
        [KeyboardButton("📊 Статистика"), KeyboardButton("❓ Справка")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"{PREMIUM_EMOJI_ID}\n\n"
        f"Привет, {user_name}! 👋\n\n"
        f"Я бот для отправки премиум эмодзи! 🎉\n\n"
        f"ID эмодзи: `{PREMIUM_EMOJI_ID}`\n\n"
        f"Используй кнопки ниже или просто напиши сообщение!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = f"""
{PREMIUM_EMOJI_ID}

🤖 *Справка по боту*

*Доступные команды:*
/start - Начать работу
/help - Эта справка
/emoji - Отправить эмодзи
/stats - Посмотреть статистику
/clear - Очистить статистику

*Что умеет бот:*
✅ Отправлять премиум эмодзи
✅ Считать количество отправок
✅ Показывать статистику

*Как использовать:*
1. Нажми кнопку "📨 Отправить эмодзи"
2. Или напиши любое сообщение
3. Бот отправит премиум эмодзи!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def emoji_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправить премиум эмодзи"""
    user_id = update.effective_user.id
    
    if user_id not in user_stats:
        user_stats[user_id] = {'count': 0, 'joined_at': datetime.now()}
    
    user_stats[user_id]['count'] += 1
    
    await update.message.reply_text(
        f"{PREMIUM_EMOJI_ID}\n\n"
        f"Вот ваш премиум эмодзи! 🎁\n\n"
        f"{PREMIUM_EMOJI_ID}\n\n"
        f"📊 Уже отправлено вам: {user_stats[user_id]['count']}"
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать статистику"""
    user_id = update.effective_user.id
    
    if user_id not in user_stats:
        await update.message.reply_text(
            f"{PREMIUM_EMOJI_ID}\n\n"
            f"У вас еще нет статистики. Напишите сообщение или нажмите кнопку!"
        )
        return
    
    stats = user_stats[user_id]
    joined_at = stats['joined_at'].strftime("%d.%m.%Y %H:%M")
    
    stats_text = f"""
{PREMIUM_EMOJI_ID}

📊 *Ваша статистика*

👤 ID пользователя: `{user_id}`
📨 Эмодзи отправлено: *{stats['count']}*
📅 Присоединился: {joined_at}
"""
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def clear_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очистить статистику"""
    user_id = update.effective_user.id
    
    if user_id in user_stats:
        del user_stats[user_id]
        await update.message.reply_text(
            f"{PREMIUM_EMOJI_ID}\n\n"
            f"✅ Статистика очищена!"
        )
    else:
        await update.message.reply_text(
            f"{PREMIUM_EMOJI_ID}\n\n"
            f"У вас нет статистики для очистки."
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех сообщений"""
    user_id = update.effective_user.id
    text = update.message.text
    
    # Инициализируем статистику если её нет
    if user_id not in user_stats:
        user_stats[user_id] = {'count': 0, 'joined_at': datetime.now()}
    
    # Проверяем команды с кнопок
    if text == "📨 Отправить эмодзи":
        user_stats[user_id]['count'] += 1
        await update.message.reply_text(
            f"{PREMIUM_EMOJI_ID}\n\n"
            f"Премиум эмодзи для вас! ✨\n\n"
            f"{PREMIUM_EMOJI_ID}\n\n"
            f"Всего: {user_stats[user_id]['count']}"
        )
    elif text == "📊 Статистика":
        stats = user_stats[user_id]
        joined_at = stats['joined_at'].strftime("%d.%m.%Y %H:%M")
        stats_text = f"{PREMIUM_EMOJI_ID}\n\n📊 *Ваша статистика*\n\n📨 Эмодзи: *{stats['count']}*\n📅 С: {joined_at}"
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    elif text == "❓ Справка":
        help_text = f"{PREMIUM_EMOJI_ID}\n\n*Бот отправляет премиум эмодзи!*\n\nПросто напишите сообщение, и я отправлю эмодзи! 🎁"
        await update.message.reply_text(help_text, parse_mode='Markdown')
    else:
        # Для любого другого сообщения отправляем эмодзи
        user_stats[user_id]['count'] += 1
        await update.message.reply_text(
            f"{PREMIUM_EMOJI_ID}\n\n"
            f"Ваше премиум эмодзи 🌟\n\n"
            f"{PREMIUM_EMOJI_ID}"
        )

def main():
    """Запуск бота"""
    TOKEN = "8679806194:AAH35zUFUYhnHWnL210bRwrcTsD_p3ZZM9A"
    
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("emoji", emoji_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("clear", clear_stats))

    # Обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен! (Ctrl+C для остановки)")
    print("TOKEN: 8679806194:AAH35zUFUYhnHWnL210bRwrcTsD_p3ZZM9A")
    print("Эмодзи ID: 5440431182602842059")
    application.run_polling()

if __name__ == '__main__':
    main()
    

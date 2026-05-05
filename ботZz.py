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
PREMIUM_EMOJI = f'<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">⭐</tg-emoji>'

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
        f"{PREMIUM_EMOJI}\n\n"
        f"Привет, {user_name}! 👋\n\n"
        f"Я бот для отправки премиум эмодзи! 🎉",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = f"""
{PREMIUM_EMOJI}

<b>🤖 Справка по боту</b>

<b>Доступные команды:</b>
/start - Начать работу
/help - Эта справка
/emoji - Отправить эмодзи
/stats - Посмотреть статистику
/clear - Очистить статистику

<b>Что умеет бот:</b>
✅ Отправлять премиум эмодзи
✅ Считать количество отправок
✅ Показывать статистику

<b>Как использовать:</b>
1. Нажми кнопку "📨 Отправить эмодзи"
2. Или напиши любое сообщение
3. Бот отправит премиум эмодзи!
"""
    await update.message.reply_text(help_text, parse_mode='HTML')

async def emoji_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправить премиум эмодзи"""
    user_id = update.effective_user.id
    
    if user_id not in user_stats:
        user_stats[user_id] = {'count': 0, 'joined_at': datetime.now()}
    
    user_stats[user_id]['count'] += 1
    
    await update.message.reply_text(
        f"{PREMIUM_EMOJI}\n\n"
        f"Вот ваш премиум эмодзи! 🎁\n\n"
        f"📊 Уже отправлено вам: {user_stats[user_id]['count']}",
        parse_mode='HTML'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать статистику"""
    user_id = update.effective_user.id
    
    if user_id not in user_stats:
        await update.message.reply_text(
            f"{PREMIUM_EMOJI}\n\n"
            f"У вас еще нет статистики. Напишите сообщение или нажмите кнопку!",
            parse_mode='HTML'
        )
        return
    
    stats = user_stats[user_id]
    joined_at = stats['joined_at'].strftime("%d.%m.%Y %H:%M")
    
    stats_text = f"""
{PREMIUM_EMOJI}

<b>📊 Ваша статистика</b>

👤 ID пользователя: <code>{user_id}</code>
📨 Эмодзи отправлено: <b>{stats['count']}</b>
📅 Присоединился: {joined_at}
"""
    await update.message.reply_text(stats_text, parse_mode='HTML')

async def clear_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очистить статистику"""
    user_id = update.effective_user.id
    
    if user_id in user_stats:
        del user_stats[user_id]
        await update.message.reply_text(
            f"{PREMIUM_EMOJI}\n\n"
            f"✅ Статистика очищена!",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            f"{PREMIUM_EMOJI}\n\n"
            f"У вас нет статистики для очистки.",
            parse_mode='HTML'
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
            f"{PREMIUM_EMOJI}\n\n"
            f"Премиум эмодзи для вас! ✨\n\n"
            f"Всего: {user_stats[user_id]['count']}",
            parse_mode='HTML'
        )
    elif text == "📊 Статистика":
        stats = user_stats[user_id]
        joined_at = stats['joined_at'].strftime("%d.%m.%Y %H:%M")
        stats_text = f"{PREMIUM_EMOJI}\n\n<b>📊 Ваша статистика</b>\n\n📨 Эмодзи: <b>{stats['count']}</b>\n📅 С: {joined_at}"
        await update.message.reply_text(stats_text, parse_mode='HTML')
    elif text == "❓ Справка":
        help_text = f"{PREMIUM_EMOJI}\n\n<b>Бот отправляет премиум эмодзи!</b>\n\nПросто напишите сообщение, и я отправлю эмодзи! 🎁"
        await update.message.reply_text(help_text, parse_mode='HTML')
    else:
        # Для любого другого сообщения отправляем эмодзи
        user_stats[user_id]['count'] += 1
        await update.message.reply_text(
            f"{PREMIUM_EMOJI}\n\n"
            f"Ваше премиум эмодзи!",
            parse_mode='HTML'
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

    print("🤖 Бот запущен!")
    print("TOKEN: 8679806194:AAH35zUFUYhnHWnL210bRwrcTsD_p3ZZM9A")
    print("Эмодзи ID: 5440431182602842059")
    application.run_polling()

if __name__ == '__main__':
    main()

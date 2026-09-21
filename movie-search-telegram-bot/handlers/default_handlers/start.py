from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """
    Обработчик для приветствования пользователей.
    """
    bot.reply_to(
        message,
        (
            f"Привет, {message.from_user.full_name}!, Я бот по поиску фильмов/сериалов.",
            "Я могу выполнять поиск по наименованию, бюджету и рейтингу."
            "Чтобы увидеть полный список моих функций, напишите /help.",
        ),
    )

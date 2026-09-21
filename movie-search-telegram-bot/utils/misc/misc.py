from functools import wraps

from telebot.types import Message, CallbackQuery, InputMediaPhoto

from loader import bot
from keyboards.inline.history_keyboards import build_history_pagination_keyboard
from database.history_models import *

from config_data import config

def telegram_error_handler(func):
    """Обработчик исключений в Telegram боте."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            chat_id = None
            arg0 = args[0] if len(args) > 0 else None

            if isinstance(arg0, Message):
                chat_id = arg0.chat.id
            elif isinstance(arg0, CallbackQuery):
                if arg0.message:
                    chat_id = arg0.message.chat.id
            elif hasattr(arg0, "message") and getattr(arg0, "message"):
                chat_id = arg0.message.chat.id

            if chat_id:
                bot.send_message(chat_id, f"❌ Произошла ошибка: {e}. Попробуйте попытку позже.")
            raise e

    return wrapper

def show_history(message: Message, movie: MovieInfo, replace: bool = False):
    search_history = movie.search_history
    movie_caption = (
        f"<b>О фильме</b>\n"
        f"<b>Наименование:</b> {movie.name}\n"
        f"<b>Описание:</b> {truncate(movie.description)}\n"
        f"<b>Рейтинг:</b> {movie.rating or 'не указан'}\n"
        f"<b>Год производства:</b> {movie.year}\n"
        f"<b>Жанр(ы):</b> {movie.genre}\n"
        f"<b>Возрастной рейтинг:</b> {movie.age_rating}"
    )
    if not replace:
        bot.send_photo(
            message.chat.id,
            photo=movie.poster or config.DEFAULT_MOVIE_POSTER_URL,
            caption=movie_caption,
            parse_mode="HTML",
            reply_markup=build_history_pagination_keyboard(
                search_history.id, movie.position_in_history, search_history.total_movies
            ),
        )
        bot.send_message(message.chat.id, "Чтобы продолжить, введите новый запрос")
    else:
        media = InputMediaPhoto(
            movie.poster or config.DEFAULT_MOVIE_POSTER_URL,
            movie_caption,
            parse_mode="HTML",
        )
        bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=media,
            reply_markup=build_history_pagination_keyboard(
                search_history.id, movie.position_in_history, search_history.total_movies
            ),
        )


def truncate(text: str, max_length: int = 700, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix

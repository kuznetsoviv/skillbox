from peewee import fn
from datetime import datetime, date

from telebot.types import Message, CallbackQuery

from loader import bot
from utils import misc
from database import crud
from keyboards.inline.history_keyboards import build_view_history_keyboard
from database.history_models import *

from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_callback = CallbackData("history_calendar", "action", "year", "month", "day")


@bot.message_handler(commands=["history"])
def bot_history_start(message: Message) -> None:
    """
    Обработчик отображения истории поиска.
    Выполняет запрос даты, за какую показывать результаты.
    """
    now = datetime.now()
    markup = calendar.create_calendar(name=calendar_callback.prefix, year=now.year, month=now.month)
    bot.send_message(message.chat.id, f"Выберите дату", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def bot_history_get_date_and_fetch(call):
    """
    Обработчик даты, за какую показывать результаты.
    Выполняет запрос на получение данных и выводит результат.
    """
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    _, _, year, month, day = call.data.split(":")
    on_date = date(int(year), int(month), int(day))
    history_records = crud.select_search_history(call.from_user.id, on_date)
    if not history_records.exists():
        bot.send_message(call.message.chat.id, f"История на дату {on_date} отсутствует!")
        return
    bot.send_message(call.message.chat.id, f"История на дату {on_date}:")
    for history_record in history_records:
        bot.send_message(
            call.message.chat.id,
            f"Показать запрос с параметрами:\n {history_record.params}",
            reply_markup=build_view_history_keyboard(history_record.id),
        )
    bot.send_message(call.message.chat.id, "Чтобы продолжить, введите новый запрос")


@bot.callback_query_handler(func=lambda call: call.data.startswith("history_record_"))
@misc.telegram_error_handler
def bot_history_record_viewer_handler(call: CallbackQuery) -> None:
    """
    Обработчик вывода результатов записи в истории запроса.
    """
    parts = call.data.split("_")
    history_id = int(parts[2])

    movie = MovieInfo.get_or_none(
        MovieInfo.search_history == history_id,
        MovieInfo.position_in_history == 0,
    )

    misc.show_history(call.message, movie, True)


@bot.callback_query_handler(func=lambda call: call.data.startswith("history_page_"))
@misc.telegram_error_handler
def bot_history_record_viewer_handler(call: CallbackQuery) -> None:
    """
    Обработчик выполнения пагинации фильмов в записи истории запроса.
    """
    parts = call.data.split("_")
    history_id, position_in_history = int(parts[2]), int(parts[3])

    movie = MovieInfo.get_or_none(
        MovieInfo.search_history == history_id,
        MovieInfo.position_in_history == position_in_history,
    )

    misc.show_history(call.message, movie, True)

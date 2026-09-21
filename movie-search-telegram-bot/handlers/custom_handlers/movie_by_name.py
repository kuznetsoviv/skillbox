from telebot.types import Message

from loader import bot
from api import movie_api
from database import crud
from states.search_info import MovieSearchByNameState

from utils import misc


@bot.message_handler(state="*", commands=["movie_search"])
def bot_movie_search_start(message: Message) -> None:
    """
    Обработчик для инициации поиска фильмов/сериалов по наименованию.
    Выполняет запрос наименования.
    """
    bot.set_state(message.from_user.id, MovieSearchByNameState.name, message.chat.id)
    bot.send_message(message.from_user.id, f"Введите название")


@bot.message_handler(state=MovieSearchByNameState.name)
def bot_movie_search_get_name(message: Message) -> None:
    """
    Обработчик введенного наименования.
    Сохраняет его в пользовательских данных и выполняет запрос количества результатов.    
    """
    bot.set_state(message.from_user.id, MovieSearchByNameState.limit, message.chat.id)
    bot.send_message(message.from_user.id, f"Введите количество результатов")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text


@bot.message_handler(state=MovieSearchByNameState.limit)
@misc.telegram_error_handler
def bot_movie_search_get_limit_and_fetch(message: Message) -> None:
    """
    Обработчик введенного количества результатов.
    Проверяет корректность ввода, выполняет поиск фильмов и сохраяет результат в истории.
    """
    limit = message.text
    if not limit.isdigit():
        bot.send_message(message.chat.id, "Введите корректное число (от 1 до 250).")
        return
    bot.set_state(message.from_user.id, None, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        movies = movie_api.get_movies_by_name(data["name"], int(limit))
        if not movies:
            bot.send_message(message.from_user.id, f"По данному запросу отсутствуют данные")
            return

        search_history = crud.add_search_history(
            user_id=message.from_user.id,
            params=f"наименование: {data["name"]}, количество результатов: {limit}",
            movies=movies,
        )
        misc.show_history(message, search_history.movies[0])

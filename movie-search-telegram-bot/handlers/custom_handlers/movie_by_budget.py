from telebot.types import Message

from loader import bot
from api import movie_api
from database import crud
from states.search_info import MovieSearchByBudgetState

from utils import misc
from config_data.config import LOW_BUDGET_VALUE, HIGH_BUDGET_VALUE

from database.history_models import *


@bot.message_handler(commands=["low_budget_movie", "high_budget_movie"])
def bot_budget_movie_start(message: Message) -> None:
    """
    Обработчик для инициации поиска фильмов/сериалов с низким и высоким бюджетом.
    Выполняет запрос жанра.
    """
    command = message.text.split()[0]
    bot.set_state(message.from_user.id, MovieSearchByBudgetState.genre, message.chat.id)
    bot.send_message(message.from_user.id, f"Введите жанр")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["budget"] = LOW_BUDGET_VALUE if command == "/low_budget_movie" else HIGH_BUDGET_VALUE
        data["budget_type"] = "низкий" if command == "/low_budget_movie" else "высокий"


@bot.message_handler(state=MovieSearchByBudgetState.genre)
def bot_budget_movie_get_genre(message: Message) -> None:
    """
    Обработчик введенного жанра.
    Проверяет корректность ввода, сохраняет его в пользовательских данных и выполняет запрос количества результатов.    
    """
    genre = message.text
    if not genre.isalpha:
        bot.send_message(message.chat.id, f"Жанр должен быть строкой")
        return
    bot.set_state(message.from_user.id, MovieSearchByBudgetState.limit, message.chat.id)
    bot.send_message(message.from_user.id, f"Введите количество результатов")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["genre"] = message.text.lower()


@bot.message_handler(state=MovieSearchByBudgetState.limit)
@misc.telegram_error_handler
def bot_budget_movie_get_limit_and_fetch(message: Message) -> None:
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
        movies = movie_api.get_movies_by_budget(data["budget"], data["genre"], int(limit))
        if not movies:
            bot.send_message(message.from_user.id, f"По данному запросу отсутствуют данные")
            return
        search_history = crud.add_search_history(
            user_id=message.from_user.id,
            params=f"{data["budget_type"]} бюджет, жанр: {data["genre"]}, количество результатов: {limit}",
            movies=movies,
        )
        misc.show_history(message, search_history.movies[0])

import re

from telebot.types import Message

from loader import bot
from api import movie_api
from database import crud
from states.search_info import MovieSearchByRatingState

from utils import misc


@bot.message_handler(state="*", commands=["movie_by_rating"])
def bot_movie_by_rating_start(message: Message) -> None:
    """
    Обработчик для инициации поиска фильмов/сериалов по рейтингу.
    Выполняет запрос рейтинга у пользователя.
    """
    bot.set_state(message.from_user.id, MovieSearchByRatingState.rating, message.chat.id)
    bot.send_message(message.from_user.id, f"Введите рейтинг")


@bot.message_handler(state=MovieSearchByRatingState.rating)
def bot_movie_by_rating_get_rating(message: Message) -> None:
    """
    Обработчик введенного рейтинга.
    Проверяет корректность ввода, сохраняет его в пользовательских данных и выполняет запрос жанра.
    """
    rating = message.text
    pattern = r"^(\d(?:\.\d+)?)(?:-(\d(?:\.\d+)?))?$"
    if not re.match(pattern, rating):
        bot.send_message(
            message.chat.id,
            f"Рейтинг должен быть в формате вида (7, 10, 7.2-10) и быть в пределах [0-10)",
        )
        return
    bot.set_state(message.from_user.id, MovieSearchByRatingState.genre, message.chat.id)
    bot.send_message(message.from_user.id, f"Введите жанр")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["rating"] = message.text


@bot.message_handler(state=MovieSearchByRatingState.genre)
def bot_movie_by_rating_get_genre(message: Message) -> None:
    """
    Обработчик введенного рейтинга.
    Проверяет корректность ввода, сохраняет его в пользовательских данных и выполняет запрос количества результатов.
    """
    genre = message.text
    if not genre.isalpha:
        bot.send_message(message.chat.id, f"Жанр должен быть строкой")
        return
    bot.set_state(message.from_user.id, MovieSearchByRatingState.limit, message.chat.id)
    bot.send_message(message.from_user.id, f"Введите количество результатов")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["genre"] = message.text.lower()


@bot.message_handler(state=MovieSearchByRatingState.limit)
@misc.telegram_error_handler
def bot_movie_by_rating_get_limit_and_fetch(message: Message) -> None:
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
        movies = movie_api.get_movies_by_rating(data["rating"], data["genre"], int(limit))
        if not movies:
            bot.send_message(message.from_user.id, f"По данному запросу отсутствуют данные")
            return

        search_history = crud.add_search_history(
            user_id=message.from_user.id,
            params=f"рейтинг: {data["rating"]}, жанр: {data["genre"]}, количество результатов: {limit}",
            movies=movies,
        )
        misc.show_history(message, search_history.movies[0])

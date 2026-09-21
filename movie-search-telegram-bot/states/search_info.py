from telebot.handler_backends import State, StatesGroup


class MovieSearchByNameState(StatesGroup):
    """
    Состояния для поиска фильмов/сериалов по наименованию.

    States:
        name: Обработка наименования.
        limit: Обработка количества результатов.
    """

    name = State()
    limit = State()


class MovieSearchByRatingState(StatesGroup):
    """
    Состояния для поиска фильмов/сериалов по рейтингу.

    States:
        raiting: Обработка рейтинга.
        genre: Обработка жанра.
        limit: Обработка количества результатов.
    """

    rating = State()
    genre = State()
    limit = State()


class MovieSearchByBudgetState(StatesGroup):
    """
    Состояния для поиска фильмов/сериалов по бюджету.

    States:
        genre: Обработка жанра.
        limit: Обработка количества результатов.
    """

    genre = State()
    limit = State()

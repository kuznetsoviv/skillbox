from datetime import date

from database.history_models import *


def add_search_history(user_id: int, params: str, movies: list[dict]) -> SearchHistory:
    """
    Добавить запись в историю поиска.

    Args:
        user_id (int): Идентификатор пользователя.
        params (str): Параметры запроса.
        movies (list[dict]): Список найденных фильмов/сериалов.

    Returns:
        SearchHistory: Добавленная запись в истории поиска.
    """
    search_history = SearchHistory.create(
        user_id=user_id,
        total_movies=len(movies),
        params=params,
    )
    for index, movie in enumerate(movies):
        MovieInfo.create(
            position_in_history=index,
            search_history=search_history,
            name=movie["name"],
            description=movie["description"],
            rating=movie.get("rating", {}).get("kp") or None,
            year=movie["year"],
            genre=", ".join([genre["name"] for genre in movie.get("genres", [])]) or "не указан\ны",
            age_rating=movie["ageRating"],
            poster=movie.get("poster", {}).get("url") or None,
        )
    return search_history


def select_search_history(user_id: int, on_date: date):
    """
    Выбрать данные в истории поиска на дату для заданного пользователя.

    Args:
        user_id (int): Идентификатор пользователя.
        on_date (date): Дата.

    Returns:
        _type_: Данные в истории поиска на дату для заданного пользователя.
    """
    return SearchHistory.select().where(
        (SearchHistory.user_id == user_id) & fn.DATE(SearchHistory.timestamp == on_date.isoformat())
    )

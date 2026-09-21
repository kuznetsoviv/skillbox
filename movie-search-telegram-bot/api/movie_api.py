import requests

from config_data.config import API_BASE_URL, RAPID_API_KEY


def api_request(module: str = "", params: dict = {}) -> requests.Response:
    """
    Запрос к rest-сервису для получения информации о фильмах/сериалах.

    Args:
        module (str, optional): Часть в url для выполнения запроса. По-умолчанию пустая строка.
        params (dict, optional): Параметры выполнения запроса.

    Raises:
        requests.exceptions.HTTPError: Ошибка выполнения запроса.

    Returns:
        requests.Response: Список с информацией о фильмах/сериалах.
    """
    headers = {"accept": "application/json", "X-API-KEY": RAPID_API_KEY}
    base_params = {
        "selectFields": [
            "name",
            "description",
            "poster",
            "rating",
            "genres",
            "ageRating",
            "year",
            "budget",
        ],
        "notNullFields": ["name", "poster.url", "genres.name", "description"],
    }
    url = f"{API_BASE_URL}/{module}" if module else API_BASE_URL
    response = requests.get(url, params={**base_params, **params}, headers=headers, verify=False)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(response.json().get("message", "Неизвестная ошибка"))
    return response


def get_movies_by_name(name: str, limit: int = 1) -> dict:
    """
    Получить список фильмов по наименованию.

    Args:
        name (str): Наименование.
        limit (int, optional): Количество результатов. По-умолчанию 1.

    Returns:
        dict: Список с информацией о фильмах/сериалах.
    """
    params = {"query": name, "limit": limit, "page": 1}
    response = api_request("search", params)
    return response.json()["docs"]


def get_movies_by_rating(rating: str, genre: str, limit: int = 1) -> dict:
    """
    Получить список фильмов по рейтингу и жанру.
    
    Args:
        rating (str): Рейтинг.
        genre (str): Жанра.
        limit (int, optional): Количество результатов. По-умолчанию 1.

    Returns:
        dict: Список с информацией о фильмах/сериалах.
    """
    params = {
        "rating.kp": rating,
        "genres.name": genre,
        "limit": limit,
        "page": 1,
        "sortField": "rating.kp",
        "sortType": 1,
    }
    response = api_request(params=params)
    return response.json()["docs"]


def get_movies_by_budget(budget: str, genre: str, limit: int = 1) -> dict:
    """
    Получить список фильмов по бюджету и жанру.

    Args:
        budget (str): Бюджет.
        genre (str): Жанр.
        limit (int, optional): Количество результатов. По-умолчанию 1.

    Returns:
        dict: Список с информацией о фильмах/сериалах.
    """
    params = {
        "genres.name": genre,
        "limit": limit,
        "budget.value": budget,
        "countries.name": "США",
        "page": 1,
        "sortField": "budget.value",
        "sortType": 1,
    }
    response = api_request(params=params)
    return response.json()["docs"]

import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

# Токен телеграмм бота.
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Api-ключ для выполнения запросов к rest-сервису поиска фильмов/сериалов.
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

# Информация о прокси (если необходимо).
PROXY_TYPE = os.getenv("PROXY_TYPE")
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

# Url для выполнения запросов к rest-сервису поиска фильмов/сериалов.
API_BASE_URL = "https://api.kinopoisk.dev/v1.4/movie"
# Url по-умолчанию для отображения постера, если он не указан в ответе.
DEFAULT_MOVIE_POSTER_URL = "https://www.freepik.com/free-photos-vectors/movie"

# Бюджет низкобюджетных фильмов (указан в долларах).
LOW_BUDGET_VALUE = f"{0}-{5_000_000}"
# Бюджет высокобюджетных фильмов (указан в долларах).
HIGH_BUDGET_VALUE = f"{50_000_000}-{1_000_000_000_000}"

# Файл с базой данных.
SEARCH_HISTORY_DATA_BASE = "search_history.db"

# Список команд телеграм бота.
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie_search", "Поиск фильмов/сериалов по наименованию"),
    ("movie_by_rating", "Поиск фильмов/сериалов по рейтингу"),
    ("low_budget_movie", "Поиск фильмов/сериалов с низким бюджетом"),
    ("high_budget_movie", "Поиск фильмов/сериалов с высоким бюджетом"),
    ("history", "Показать историю запросов"),
)

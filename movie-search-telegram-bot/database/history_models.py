from datetime import datetime
from peewee import *
from config_data.config import SEARCH_HISTORY_DATA_BASE

db = SqliteDatabase(SEARCH_HISTORY_DATA_BASE)


def initialize_db():
    with db:
        db.create_tables([SearchHistory, MovieInfo], safe=True)


class BaseModel(Model):
    """Базовая модель данных."""

    class Meta:
        database = db


class SearchHistory(BaseModel):
    """
    Модель поисковой истории запросов пользователей.
    
    Attributes:
        user_id (int): Идентфикатор пользователя
        params (str): Параметры запроса
        total_movies (int): Общее количество фильмов
        timestamp (str): Время выполнения запроса
    """

    class Meta:
        table_name = "search_history"

    user_id = IntegerField(index=True)
    params = TextField()
    total_movies = IntegerField()
    timestamp = DateTimeField(default=datetime.now)


class MovieInfo(BaseModel):
    """
    Модель для хранения информации о фильме в контексте поисковой истории.
    
    Attributes:
        position_in_history (int): Позиция фильма в списке результатов
        search_history (UserSearchHistory): Ссылка на запись истории поиска
        name (str): Название фильма
        description (str): Описание фильма
        rating (float or None): Рейтинг фильма
        year (int or None): Год выпуска
        genre (str or None): Жанр фильма
        age_rating (int or None): Возрастной рейтинг
        poster (str): Постер
    """

    class Meta:
        table_name = "movie_info"

    position_in_history = IntegerField()
    search_history = ForeignKeyField(SearchHistory, backref="movies")
    name = CharField()
    description = TextField()
    rating = FloatField(null=True)
    year = IntegerField(null=True)
    genre = CharField(null=True)
    age_rating = IntegerField(null=True)
    poster=TextField(null=True)

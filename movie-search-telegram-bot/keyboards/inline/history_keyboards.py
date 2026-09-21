from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_history_pagination_keyboard(
    history_id: int,
    movie_position_in_history: int,
    total_movies: int,
) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для постраничного просмотра истории поиска фильмов.

    Args:
        history_id (int): Идентификатор записи поиска фильмов.
        movie_position_in_history (int): Позиция фильма в результате поиска.
        total_movies (int): Общее количество найденных фильмов.

    Returns:
        types.InlineKeyboardMarkup: Инлайн-клавиатура для постраничного просмотра истории поиска фильмов.
    """

    cur_movie_id = movie_position_in_history
    next_movie_id = (cur_movie_id + 1) % total_movies
    prev_movie_id = (cur_movie_id - 1) % total_movies

    keyboard = InlineKeyboardMarkup()
    left_btn = InlineKeyboardButton("←", callback_data=f"history_page_{history_id}_{prev_movie_id}")
    page_info_btn = InlineKeyboardButton(f"{cur_movie_id + 1}/{total_movies}", callback_data="noop")
    right_btn = InlineKeyboardButton(
        "→", callback_data=f"history_page_{history_id}_{next_movie_id}"
    )
    keyboard.add(left_btn, page_info_btn, right_btn)
    return keyboard


def build_view_history_keyboard(history_id: int) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для просмотра результата запроса поиска фильмов.

    Args:
        history_id (int): Идентификатор записи, содержащей результат запроса поиска фильмов.

    Returns:
        types.InlineKeyboardMarkup: Инлайн-клавиатура для просмотра результата запроса поиска фильмов.
    """
    keyboard = InlineKeyboardMarkup()
    view_button = InlineKeyboardButton("Показать", callback_data=f"history_record_{history_id}")
    keyboard.add(view_button)
    return keyboard

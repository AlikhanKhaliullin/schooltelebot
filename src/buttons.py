from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

time_left = KeyboardButton(text="⏳ Сколько осталось времени")
next_lesson = KeyboardButton(text="👨‍💻 Следуйщий урок")
next_day = KeyboardButton(text="уроки на завтра")
today = KeyboardButton(text="уроки на сегодня")
settings  = KeyboardButton(text="ℹ️ Изменить класс")
startMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(time_left, next_day, settings,today)
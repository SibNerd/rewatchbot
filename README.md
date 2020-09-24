# Что это за бот?

Данный бот позволяет добавлять различные шоу (фильмы/сериалы/аниме/you_name_it) в список желаемого к просмотру, а так же добавлять рейтинг и комментарий к уже просмотренным.

Для работы с Telegram API используется библиотека aiogram.
Для сложных запросов используются конечные автоматы.
Для хранения данных используется БД Sqlite3.

Адрес БД и токен бота вынесены в файл **configs.py**.

# А что он умеет?

Список доступных команд бота:
* /to_watchlist - добавляет шоу в список желаемого к просмотру.
* /watched - отмечает шоу как просмотренное. Если шоу до этого отсутствовало в списке, добавляет его уже как просмотренное.
* /get_rate - показывает выставленный пользователем рейтинг шоу от 1 до 5.
* /get_note - показывает комментарий пользователя о шоу.
*Если у шоу отсутствует рейтинг или шоу, бот уведомляет об этом пользователя.*

# Зависимости

Дополнительные библиотеки, необходимые для работы бота, описаны в файле **requirements.txt**.

# Начало работы
1. Установка необходимых библиотек.
> pip install -r requirements.txt

2. Создание базы данных.
> python init_db.py

3. Запуск бота.
> python main.py

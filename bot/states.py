from aiogram.dispatcher.filters.state import State, StatesGroup


class ToWatchlist(StatesGroup):
    add_name_and_type = State()

class ToWatched(StatesGroup):
    add_name_and_type = State()
    add_rate = State()
    add_note = State()

class ChangeRateNote(StatesGroup):
    change_rate = State()
    change_note = State()



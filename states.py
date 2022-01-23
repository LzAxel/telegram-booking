from aiogram.dispatcher.filters.state import State, StatesGroup


class BookingData(StatesGroup):
    Price = State()
    Region = State()
    Room_Count = State()
    
class UserData(StatesGroup):
    First_Name = State()
    Second_Name = State()
    Phone = State()
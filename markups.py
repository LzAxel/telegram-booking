from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

#Main keyboard
kb_main = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton("Забронировать квартиру")
        ],
        [
            KeyboardButton("Профиль"),
            KeyboardButton("Мои брони")
        ]
    ], resize_keyboard=True)


#Profile keyboard
kb_profile = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Изменить ⚙️', callback_data='profile_change'),
        InlineKeyboardButton('Удалить ❌', callback_data='profile_delete')
    ]
])




#Price keyboard
cb_price = CallbackData('price', 'value')
kb_price = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("До 100", callback_data=cb_price.new('100')),
        InlineKeyboardButton("До 200", callback_data=cb_price.new('200')),
        InlineKeyboardButton("До 300", callback_data=cb_price.new('300')),
    ]])

#Region keyboard
cb_region = CallbackData('region', 'value')
kb_region = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("Балка", callback_data=cb_region.new('Балка')),
        InlineKeyboardButton("Нахимовский", callback_data=cb_region.new('Нахимовский')),
        InlineKeyboardButton("Ленинский", callback_data=cb_region.new('Ленинский')),
    ]])

#Room count keyboard
cb_room_count = CallbackData('room_count', 'value')
kb_room_count = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("Студия и 1 к.к.", callback_data=cb_room_count.new('1'))
    ],
    [
        InlineKeyboardButton("2-х комнатная", callback_data=cb_room_count.new('2')),
        InlineKeyboardButton("3-х комнатная", callback_data=cb_room_count.new('3')),
        InlineKeyboardButton("4+", callback_data=cb_room_count.new('4+'))
    ]])





from bot import dp, db
from states import UserData, BookingData
from markups import kb_main, kb_profile, kb_price, kb_region, kb_room_count
from markups import cb_price, cb_region, cb_room_count

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters

#Handlers
@dp.message_handler(commands="start", state="*")
async def start_process(msg: types.Message, state: FSMContext):
    await msg.answer("Привет, я бот, у которого ты можешь забронировать квартиру.", reply_markup=kb_main)
    data = db.get_user(msg.from_user.id)
    if not data:
        await msg.answer("Но для начала тебе нужно зарегистрироваться.\nОтправь своё имя.\nНапример: Вася")
        await UserData.First_Name.set()
    
    else:
        await msg.answer(f"Рад видеть тебя снова, {data[1]}")


@dp.message_handler(state=UserData.First_Name)
async def get_user_first_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = msg.text
        
    await msg.answer("Отлично, теперь тебе нужно отправить свою фамилию.\nНапример: Ушаков")
    await UserData.next()


@dp.message_handler(state=UserData.Second_Name)
async def get_user_second_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_name'] = msg.text
        
    await msg.answer("И последнее, отправь свой номер телефона.\nНапример: 37377798352")
    await UserData.next()


@dp.message_handler(state=UserData.Phone)
async def get_user_phone(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = msg.text
        db.add_user(msg.from_user.id, data['first_name'], data['second_name'], data['phone'])

        await msg.answer(f"Хорошо, {data['first_name']} , теперь ты можешь воспользоваться всеми функциями бота!")
        
    await state.finish()


@dp.message_handler(filters.Text("Забронировать квартиру"))
async def input_booking_date(msg: types.Message):
    await msg.answer("Выберите цену желаемой брони", reply_markup=kb_price)

    await BookingData.Price.set()


@dp.callback_query_handler(cb_price.filter(), state=BookingData.Price)
async def input_booking_region(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as state_data:
        state_data['price'] = callback_data['value']
    await query.message.edit_text("Выберите район желаемой брони", reply_markup=kb_region)
    await BookingData.Region.set()


@dp.callback_query_handler(cb_region.filter(), state=BookingData.Region)
async def input_booking_room_count(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as state_data:
        state_data['region'] = callback_data['value']
    await query.message.edit_text("Выберите количество комнат желаемой брони", reply_markup=kb_room_count)
    await BookingData.Room_Count.set()


@dp.callback_query_handler(cb_room_count.filter(), state=BookingData.Room_Count)
async def get_booking(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    booking_data = await state.get_data()
    booking_data['room_count'] = callback_data['value']
    for id in db.get_apartament_by_categories(booking_data['price'], booking_data['region'], booking_data['room_count']):
        msg = query.message
        data, photo = db.get_apartament_info(id)
        await show_apartament(msg, data, photo)

    await query.message.delete()
    await state.finish()


@dp.message_handler(commands="my_id")
async def show_id(msg: types.Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")


@dp.message_handler(commands="apart")
async def show_apartament(msg: types.Message, *data):
    if data:
        info = data[0]
        photo = data[1]
        print(info, photo)
    else:
        id = msg.get_args()
        info, photo = db.get_apartament_info(id)
        
    if photo:
        await msg.answer_media_group([types.InputMediaPhoto(media=i[0]) for i in photo])
    else:
        await msg.answer_media_group([types.InputMediaPhoto(media='https://st3.depositphotos.com/23594922/31822/v/600/depositphotos_318221368-stock-illustration-missing-picture-page-for-website.jpg')])
    if info:
        await msg.answer(f"<b>Название:</b> {info[1]}\n<b>Описание:</b> {info[2]}\n<b>Кол-во жилых комнат:</b> {info[4]} шт.\n"
                        f"<b>Адрес:</b> {info[6]}\n<b>Район:</b> {info[5]}\n<b>Цена за день:</b> {info[3]} руб.")
    else:
        await msg.answer("Такой квартиры не сущетсвует")



@dp.message_handler(filters.Text('Профиль'))
async def show_profile(msg: types.Message):
    data = db.get_user(id=msg.from_user.id)
    await msg.answer('<b>Ваш профиль</b> \n\nID: {}\nИмя: {}\nФамилия: {}\nТелефон: {}'.format(*data), reply_markup=kb_profile)
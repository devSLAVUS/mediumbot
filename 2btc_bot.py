import asyncio
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
from aiogram import Bot, types, executor
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from auth_data import token
from giro_for_mine import get_all, get_weather, maska, get_pic, get_graf, get_zab
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
    
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
keyboard = InlineKeyboardMarkup()
def rate_limit(limit: int, key=None):

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator
class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        # Get current handler
        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)

            # Cancel current handler
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await message.reply('Too many requests! ')

        # Sleep.
        await asyncio.sleep(delta)

    # Check lock status
        thr = await dispatcher.check_key(key)

    # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('spokoyno!')


@dp.message_handler(commands=['m'])
async def handle_text(message):
    await bot.send_message(message.chat.id, "<b>Введите маску: </b>", parse_mode="html")
    await bot.register_next_step_handler(message, print_mask)
async def print_mask(message):
    txt = message.text
    s = maska(txt)
    await bot.send_message(message.chat.id, s)
@dp.message_handler(commands=['start']) 
@rate_limit(5, 'start')  
async def process_start_command(message: types.Message):
    await message.reply("Команды:\n/help")
@dp.message_handler(commands=['btc'])
@rate_limit(5, 'btc')
async def process_help_command(message: types.Message):
    r = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    r = requests.get(r)
    data = r.json()
    price = data["price"]
    price1 = price[:9]
    await bot.send_message(
        message.chat.id, f"{datetime.now().strftime('%d-%m-%Y      %H:%M')}\nSell BTC price: {price1}")
@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)
    inf = "**Slavus Laboratories introduce**\n\
bot: lab_slavus\n\
Version: 2.1 stable\n\
Last Update: 13.10.21\n\
Команды:\n\
1. /btc - курс биткоина\n\
2. /pogoda - погода\n\
3. /giro - гороскоп\n\
4. /guys - графана парни\n\
5. /graf - графана график"
    await bot.send_message(
        message.chat.id, inf)

inline_btn_1 = InlineKeyboardButton('Рыбы', callback_data='fish')
inline_btn_2 = InlineKeyboardButton('Весы', callback_data='vesi')
inline_btn_3 = InlineKeyboardButton('Овен', callback_data='aries')
inline_btn_4 = InlineKeyboardButton('Телец', callback_data='taurus')
inline_btn_5 = InlineKeyboardButton('Близнецы', callback_data='gemini')
inline_btn_6 = InlineKeyboardButton('Рак', callback_data='cancer')
inline_btn_7 = InlineKeyboardButton('Лев', callback_data='leo')
inline_btn_8 = InlineKeyboardButton('Дева', callback_data='virgo')
inline_btn_9 = InlineKeyboardButton('Скорпион', callback_data='scorpio')
inline_btn_10 = InlineKeyboardButton('Стрелец', callback_data='sagittarius')
inline_btn_11 = InlineKeyboardButton('Козерог', callback_data='capricorn')
inline_btn_12 = InlineKeyboardButton('Водолей', callback_data='aquarius')

inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5, 
inline_btn_6, inline_btn_7, inline_btn_8, inline_btn_9, inline_btn_10, inline_btn_11, inline_btn_12)

inline_btn_13 = InlineKeyboardButton('Москва', callback_data='moscow')
inline_btn_14 = InlineKeyboardButton('Санкт-Петербург', callback_data='spb')
inline_btn_15 = InlineKeyboardButton('Курган', callback_data='kurgan')
inline_btn_16 = InlineKeyboardButton('Дубаи', callback_data='dubai')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_13, inline_btn_14, inline_btn_15, inline_btn_16)

@dp.message_handler(commands=['rus'])
async def help_message(message: types.Message):
    #await bot.send_message(message.from_user.id, message.text)
     await bot.send_message(
           message.chat.id, "РА СИ Я\nРА СИ Я\nРА СИ Я")

@dp.message_handler(commands=['giro'])
async def process_command_1(message: types.Message):
    await message.reply("Знак?", reply_markup=inline_kb1)
@dp.callback_query_handler(lambda c: c.data == 'vesi')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "libra"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'fish')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "pisces"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'aries')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "aries"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'taurus')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "taurus"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'gemini')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "gemini"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'cancer')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "cancer"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'leo')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "leo"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'virgo')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "virgo"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'scorpio')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "scorpio"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'sagittarius')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "sagittarius"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'capricorn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "capricorn"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'aquarius')
async def process_callback_button1(callback_query: types.CallbackQuery):
    zn = "aquarius"
    s = get_all(zn)         
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"{str(s.text)}")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

@dp.message_handler(commands=['pogoda'])
async def process_command_2(message: types.Message):
    await message.reply("Город?", reply_markup=inline_kb2)
@dp.callback_query_handler(lambda c: c.data == 'moscow')
async def process_callback_button1(callback_query: types.CallbackQuery):
    g = "Moscow"
    s = get_weather(g)
    await bot.send_message(
            callback_query.message.chat.id, f"***{datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {s[0]}\nТемпература: {s[1]}C°\n"
                            f"Влажность: {s[3]}%\nДавление: {s[4]} мм.рт.ст\nВетер: {s[5]} м/с\n"
                            f"Восход солнца: {s[6]}\nЗакат солнца: {s[7]}\nПродолжительность дня: {s[8]}\n"
                            f"Хорошего дня!"
                        )
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'spb')
async def process_callback_button1(callback_query: types.CallbackQuery):
    g = "Saint%20Petersburg"
    s = get_weather(g)
    await bot.send_message(
            callback_query.message.chat.id, f"***{datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {s[0]}\nТемпература: {s[1]}C°\n"
                            f"Влажность: {s[3]}%\nДавление: {s[4]} мм.рт.ст\nВетер: {s[5]} м/с\n"
                            f"Восход солнца: {s[6]}\nЗакат солнца: {s[7]}\nПродолжительность дня: {s[8]}\n"
                            f"Хорошего дня!"
                        )
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'kurgan')
async def process_callback_button1(callback_query: types.CallbackQuery):
    g = "kurgan"
    s = get_weather(g)
    await bot.send_message(
            callback_query.message.chat.id, f"***{datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {s[0]}\nТемпература: {s[1]}C°\n"
                            f"Влажность: {s[3]}%\nДавление: {s[4]} мм.рт.ст\nВетер: {s[5]} м/с\n"
                            f"Восход солнца: {s[6]}\nЗакат солнца: {s[7]}\nПродолжительность дня: {s[8]}\n"
                            f"Хорошего дня!"
                        )
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'dubai')
async def process_callback_button1(callback_query: types.CallbackQuery):
    g = "dubai"
    s = get_weather(g)
    await bot.send_message(
            callback_query.message.chat.id, f"***{datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {s[0]}\nТемпература: {s[1]}C°\n"
                            f"Влажность: {s[3]}%\nДавление: {s[4]} мм.рт.ст\nВетер: {s[5]} м/с\n"
                            f"Восход солнца: {s[6]}\nЗакат солнца: {s[7]}\nПродолжительность дня: {s[8]}\n"
                            f"Хорошего дня!"
                        )
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    

if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp)


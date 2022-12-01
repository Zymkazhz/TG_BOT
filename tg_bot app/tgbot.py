from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN_API, PROXY_URL, PROXY_AUTH
from models import *
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
from datetime import datetime

bot = Bot(TOKEN_API, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(
    resize_keyboard=True)
b1 = KeyboardButton('/description')
b2 = KeyboardButton('/top10token')
b3 = KeyboardButton('/estimate')
b4 = KeyboardButton(text='/help')

kb.add(b1).insert(b2).add(b3).insert(b4)

HELP_COMMAND = """
<b>/start</b> - <em>Начать работу с ботом</em>
<b>/help</b> - <em>Список команд</em>
<b>/top10token</b> - <em>Топ 10 монет на рынке</em>
<b>/estimate</b> - <em>Оценить бота</em>
<b>/description</b> - <em>Описание бота</em>
"""


async def on_startup(_):
    print('Бот запущен')


@dp.message_handler(commands=['estimate'])
async def vote_command(message: types.Message):
    ikb = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(text='👍',
                                callback_data='like')
    ikb2 = InlineKeyboardButton(text='👎',
                                callback_data='dislike')
    ikb.add(ikb1, ikb2)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Как вам бот !?😉',
                           reply_markup=ikb)


@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer(text='Спасибо за оценку')
    await callback.answer(text='Не ври!')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND, parse_mode='HTML')


@dp.message_handler(commands=['description'])
async def description(message: types.Message):
    await message.answer(text='Бот криптоинформер умеет по запросу выдавать <b>актуальную</b>\n'
                              'информацию о топ 250 монетах, а так выводить топ10 монет по капитализации.\n'
                              'Так же еженедельно бот предлагает пару монет к рассмотрению.',
                         parse_mode='HTML')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEGjdpjgbf9NkywAm3WgFZGm_Lpy1i0VwACBAQAAsSraAse'
                                                         'YIn8uE2RPisE')
    await message.answer(text='<b>Добро пожаловать в наш бот</b> 😉\n'
                              'Тут ты можешь узнавать актуальную информацию о монетах',
                         parse_mode='HTML',
                         reply_markup=kb)
    try:
        Persons.get(Persons.id_person == message.from_user.id)
        pass
    except:
        add_user_db(message.from_user.id)

    async def test(bot: Bot):
        with db:
            query_person = Persons.select()
            query_token = Token.select()
            list_name_token = []
            set_random_token = []
            answer = []
            for i in query_token:
                list_name_token.append(i.id_name)
            random_token_one = random.choice(list_name_token)
            random_token_two = random.choice(list_name_token)
            set_random_token.append(random_token_one)
            set_random_token.append(random_token_two)
            for i in set_random_token:
                i = i.capitalize()
                i = '🔥' + str(i) + ' \n'
                answer.append(i)
            answer = ''.join(answer)
            for i in query_person:
                await bot.send_message(chat_id=i.id_name, text=f'Рекомендую рассмотреть монеты к покупке:\n'
                                                               f'{answer}'
                                                               f'Не финансовая рекомендация😉')

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(test, trigger='cron', day_of_week=0, hour=11,
                      start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()


@dp.message_handler(commands=['top10token'])
async def top10token(message: types.Message):
    with db:
        query = Token.select().where(Token.market_cap_rank < 11)
        list_top10_token = []
        answer_top10_token = []
        for i in query:
            list_top10_token += i.id_name.split()
        for i in list_top10_token:
            i = i.capitalize()
            i = '🔝' + str(i) + ' \n'
            answer_top10_token += i
        answer_top10_token = ''.join(answer_top10_token)
        await message.answer(text=answer_top10_token)


@dp.message_handler()
async def token_info(message: types.Message):
    query_user = message.text.lower()
    with db:
        try:
            query_name = Token.get(Token.id_name == query_user)
            await message.answer(text=f'Имя: {query_name.name}\n'
                                      f'Символ: {query_name.symbol}\n'
                                      f'Цена: {query_name.current_price}\n'
                                      f'Позиция на маркете: {query_name.market_cap_rank}\n'
                                      f'Самая высокая цена за сутки: {query_name.high_24h}\n'
                                      f'Самая низкая цена за сутки: {query_name.low_24h}\n'
                                      f'Изменение цены за сутки: {round(float(query_name.price_change_24h), 2)}')
        except:
            try:
                query_symbol = Token.get(Token.symbol == query_user)
                await message.answer(text=f'Имя: {query_symbol.name}\n'
                                          f'Символ: {query_symbol.symbol}\n'
                                          f'Цена: {query_symbol.current_price}\n'
                                          f'Позиция на маркете: {query_symbol.market_cap_rank}\n'
                                          f'Самая высокая цена за сутки: {query_symbol.high_24h}\n'
                                          f'Самая низкая цена за сутки: {query_symbol.low_24h}\n'
                                          f'Изменение цены за сутки: {round(float(query_symbol.price_change_24h), 2)}')
            except:
                await message.answer(text='Введите правильное название монеты 🙄')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

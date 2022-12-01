from peewee import *
import json
import requests
import schedule

import config

db = PostgresqlDatabase(
    database=config.db_name,
    user=config.user,
    password=config.password,
    host=config.host,
    port=config.port,
)


class Token(Model):
    id_score = AutoField()
    id_name = CharField()  # имя мелкими буквами
    name = CharField(max_length=50)  # Имя токена
    symbol = CharField(max_length=10)  # Символ токена
    current_price = CharField()  # Цена токена
    market_cap_rank = IntegerField()  # Позиция на маркете
    high_24h = IntegerField()  # Самая высокая цена за сутки
    low_24h = IntegerField()  # Самая низкая цена за сутки
    price_change_24h = CharField()  # Изменение цены за сутки

    class Meta:
        database = db


class Persons(Model):
    id_score = AutoField()
    id_person = IntegerField()

    class Meta:
        database = db


def add_user_db(id_person):
    row = Persons(id_person=id_person)
    row.save()


def delete_date():
    with db:
        query = Token.delete().where(Token.market_cap_rank > 0).execute()
        print(query)


def record_in_db():
    response = requests.get(url='https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc'
                                '&per_page=250&page=1&sparkline=false')
    data_token = json.loads(response.text)
    with db.atomic():
        for index in range(0, len(data_token), 50):
            prepared_data = [
                {
                    'id_name': d['id'],
                    'name': d['name'],
                    'symbol': d['symbol'],
                    'current_price': d['current_price'],
                    'market_cap_rank': int(d['market_cap_rank']),
                    'high_24h': int(d['high_24h']),
                    'low_24h': int(d['low_24h']),
                    'price_change_24h': d['price_change_24h']
                } for d in data_token[index:index+50]
            ]
            Token.insert_many(prepared_data).execute()


def main():
    schedule.every().day.at('12:46').do(delete_date)
    schedule.every().day.at('12:46').do(record_in_db)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()




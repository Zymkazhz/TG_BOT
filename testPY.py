import json
from peewee import *




a = """[
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1547033579",
    "current_price": 16625.25,
    "market_cap": 318484704195,
    "market_cap_rank": 1,
    "fully_diluted_valuation": 348277016763,
    "total_volume": 73090450635,
    "high_24h": 17789.6,
    "low_24h": 15663.49,
    "price_change_24h": -941.702501059779,
    "price_change_percentage_24h": -5.36065,
    "market_cap_change_24h": -22094670827.43402,
    "market_cap_change_percentage_24h": -6.48738,
    "circulating_supply": 19203618,
    "total_supply": 21000000,
    "max_supply": 21000000,
    "ath": 69045,
    "ath_change_percentage": -76.07191,
    "ath_date": "2021-11-10T14:24:11.849Z",
    "atl": 67.81,
    "atl_change_percentage": 24264.16287,
    "atl_date": "2013-07-06T00:00:00.000Z",
    "roi": null,
    "last_updated": "2022-11-10T12:59:32.946Z"
  },
  {
    "id": "ethereum",
    "symbol": "eth",
    "name": "Ethereum",
    "image": "https://assets.coingecko.com/coins/images/279/large/ethereum.png?1595348880",
    "current_price": 1211.19,
    "market_cap": 145917869643,
    "market_cap_rank": 2,
    "fully_diluted_valuation": 145917869643,
    "total_volume": 25845704365,
    "high_24h": 1235.52,
    "low_24h": 1087.08,
    "price_change_24h": -11.232405329065614,
    "price_change_percentage_24h": -0.91886,
    "market_cap_change_24h": -3093031583.399353,
    "market_cap_change_percentage_24h": -2.07571,
    "circulating_supply": 120517018.940905,
    "total_supply": 120517018.940905,
    "max_supply": null,
    "ath": 4878.26,
    "ath_change_percentage": -75.27901,
    "ath_date": "2021-11-10T14:24:19.604Z",
    "atl": 0.432979,
    "atl_change_percentage": 278425.03355,
    "atl_date": "2015-10-20T00:00:00.000Z",
    "roi": {
      "times": 96.3980155572741,
      "currency": "btc",
      "percentage": 9639.801555727412
    },
    "last_updated": "2022-11-10T12:59:35.180Z"
  }
]"""
data = json.loads(a)
for i in data:
    print(i)

db = PostgresqlDatabase(database='tgbot', user='postgres', password='2bbkbxfE', host='localhost')


class Token(Model):
    name = CharField(max_length=50)  # Имя токена
    symbol = CharField(max_length=10)  # Символ токена
    price = CharField()  # Цена токена
    market_cap_rank = CharField()  # Позиция на маркете
    total_supply = CharField()  # Общее предложение
    image = TextField()

    class Meta:
        database = db


db.connect()
db.create_tables([Token])
with db.atomic():
    for index in range(0, len(data), 50):
        Token.insert_many(data[index:index+50]).execute()
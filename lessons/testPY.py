import requests
import json
from models import *
import random
import json
from peewee import *
import requests
import schedule

# a = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false')
# data = json.loads(a.text)
# print(data)
##a = str(a)
##data = json.loads(a)

# spisok = ['bitcoin', 'weway']
# spisok2 = []
# for i in spisok:
#    i = str(i) + ' \n'
#    spisok2 += i
# spisok2 = ''.join(spisok2)
# print(spisok2)
#
# with db.atomic():
#    for index in range(0, len(data), 50):
#        prepared_data = [
#            {
#                'id_name': d['id'],
#                'name': d['name'],
#                'symbol': d['symbol'],
#                'current_price': d['current_price'],
#                'market_cap_rank': d['market_cap_rank'],
#                'high_24h': d['high_24h'],
#                'low_24h': d['low_24h'],
#                'price_change_24h': d['price_change_24h']
#            } for d in data[index:index + 50]
#        ]
#        Token.insert_many(prepared_data).execute()
#

# a = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false')
# data = a.json()
# print(data)

# with db:
#    query = Token.select().where(Token.market_cap_rank < 11)
#    list_top10_token = []
#    answer_top10_token = []
#    for i in query:
#        print(i.market_cap_rank)
#list_name_token = ['111', '222', '333', '444', '555', '666', '777']
#a = []
#random_name_token = random.choice(list_name_token)
#a.append(random_name_token)
#print(a)



with db:
    query = Token.select()
    list_name_token = []
    set_random_token = []
    answer = []
    for i in query:
        list_name_token.append(i.id_name)
    random_token_one = random.choice(list_name_token)
    random_token_two = random.choice(list_name_token)
    set_random_token.append(random_token_one)
    set_random_token.append(random_token_two)
    for i in set_random_token:
        i = i.capitalize()
        i = '🔝' + str(i) + ' \n'
        answer.append(i)
    answer = ''.join(answer)

print(answer)


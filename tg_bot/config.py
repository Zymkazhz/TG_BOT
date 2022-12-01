import os

from aiohttp import BasicAuth

TOKEN_API = '5688968215:AAFBDylGJtbA6sk_CbQhr8-d32u4yqk8t48'
PROXY_URL = 'socks5://91.188.215.243:46621'
PROXY_AUTH = BasicAuth(login='H8WkeG7N', password='SCAbafX8')

host = os.getenv('POSTGRES_HOST', '127.0.0.1')
port = os.getenv('POSTGRES_PORT', '5481')
user = os.getenv('POSTGRES_USER', 'tgbotuser')
password = os.getenv('POSTGRES_PASSWORD', 'mBFSH9lPvQj744OZ')
db_name = os.getenv('POSTGRES_DB', 'tg_bot')

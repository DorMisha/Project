import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
    682419989
]


chat_ids = [
    -860316794
]


banned_messages = [
    'бан', 'спам'
]



ip = os.getenv('ip')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI=f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'
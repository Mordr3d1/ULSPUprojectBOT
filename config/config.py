# config file
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()

dotenv.load_dotenv('.env')

BOT_API_TOKEN = os.getenv("BOT_TOKEN")
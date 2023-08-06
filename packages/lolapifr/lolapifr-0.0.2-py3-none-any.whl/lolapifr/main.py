import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def test():
    print(API_KEY)
    return 'test'
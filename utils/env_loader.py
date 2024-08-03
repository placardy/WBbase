from dotenv import load_dotenv
import os

load_dotenv()

def get_api_tokens():
    return {
        'wb_api_token_1': os.getenv('wb_api_token_1'),
        'wb_api_token_2': os.getenv('wb_api_token_2'),
        'wb_api_token_3': os.getenv('wb_api_token_3')
    }

def get_database_url():
    return os.getenv('DATABASE_URL')

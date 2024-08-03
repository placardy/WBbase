# import requests
# from datetime import datetime, timedelta
# from utils.env_loader import get_api_tokens, get_database_url
# from utils.db_utils import get_session, upsert_funnel_data, upsert_product
# from utils.logging_utils import setup_logging, log_info, log_error
#
# setup_logging()
#
# def get_start_end_dates(date=None):
#     if date:
#         start_date = datetime.strptime(date, '%Y-%m-%d')
#         end_date = start_date + timedelta(days=1)  # До конца дня
#     else:
#         now = datetime.now()
#         start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
#         end_date = now
#     return start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')
#
# def fetch_funnel_data(api_token, date_from, date_to):
#     url = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail'
#     print('details!')
#     headers = {'Authorization': api_token}
#     params = {
#         "brandNames": [],
#         "objectIDs": [],
#         "tagIDs": [],
#         "nmIDs": [],
#         "timezone": "Europe/Moscow",
#         "period": {
#             "begin": date_from,
#             "end": date_to
#         },
#         "orderBy": {
#             "field": "ordersSumRub",
#             "mode": "desc"
#         },
#         "page": 1
#     }
#
#     try:
#         response = requests.post(url, headers=headers, json=params)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         log_error(f"Error fetching funnel data: {e}")
#         print(f"Error fetching funnel data: {e}")
#         return {}
#
# def process_funnel_data(date=None):
#     database_url = get_database_url()
#     session = get_session(database_url)
#     tokens_from_env = get_api_tokens()
#
#
#     tokens = [
#         {'token': tokens_from_env.get('wb_api_token_1'), 'name': 'Д'},
#         {'token': tokens_from_env.get('wb_api_token_2'), 'name': 'С'},
#         {'token': tokens_from_env.get('wb_api_token_3'), 'name': 'Б'}
#     ]
#
#
#     date_from, date_to = get_start_end_dates(date)
#     all_data = []
#
#     for token_data in tokens:
#         token = token_data['token']
#         owner = token_data['name']
#         data = fetch_funnel_data(token, date_from, date_to)
#         for c in data.get("data", {}).get("cards", []):
#
#             card_stat = {
#                 "nmID": c.get("nmID"),
#                 "date": datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S').date(),
#                 "vendorCode": c.get("vendorCode"),
#                 "productType": c.get("object", {}).get("name"),
#                 "brandName": c.get("brandName"),
#                 "openCardCount": c.get("statistics", {}).get("selectedPeriod", {}).get("openCardCount"),
#                 "addToCartCount": c.get("statistics", {}).get("selectedPeriod", {}).get("addToCartCount"),
#                 "ordersCount": c.get("statistics", {}).get("selectedPeriod", {}).get("ordersCount"),
#                 "buyoutsCount": c.get("statistics", {}).get("selectedPeriod", {}).get("buyoutsCount"),
#                 "cancelCount": c.get("statistics", {}).get("selectedPeriod", {}).get("cancelCount"),
#                 "addToCartPercent": c.get("statistics", {}).get("selectedPeriod", {}).get("conversions", {}).get("addToCartPercent"),
#                 "cartToOrderPercent": c.get("statistics", {}).get("selectedPeriod", {}).get("conversions", {}).get("cartToOrderPercent"),
#                 "buyoutsPercent": c.get("statistics", {}).get("selectedPeriod", {}).get("conversions", {}).get("buyoutsPercent"),
#                 "ordersSumRub": c.get("statistics", {}).get("selectedPeriod", {}).get("ordersSumRub"),
#                 "buyoutsSumRub": c.get("statistics", {}).get("selectedPeriod", {}).get("buyoutsSumRub"),
#                 "cancelSumRub": c.get("statistics", {}).get("selectedPeriod", {}).get("cancelSumRub"),
#                 "avgPriceRub": c.get("statistics", {}).get("selectedPeriod", {}).get("avgPriceRub"),
#                 "avgOrdersCountPerDay": c.get("statistics", {}).get("selectedPeriod", {}).get("avgOrdersCountPerDay"),
#                 "stocksMp": c.get("stocks", {}).get("stocksMp"),
#                 "stocksWb": c.get("stocks", {}).get("stocksWb"),
#                 "owner": owner
#             }
#             upsert_product(session, card_stat["nmID"], card_stat["vendorCode"])
#             all_data.append(card_stat)
#     upsert_funnel_data(session, all_data)
#     session.close()
#     log_info(f"Funnel data processed for {date}")
#
# if __name__ == '__main__':
#     process_funnel_data()

import requests
from datetime import datetime, timedelta
from utils.env_loader import get_api_tokens, get_database_url
from utils.db_utils import get_session, upsert_funnel_data, upsert_product
from utils.logging_utils import setup_logging, log_info, log_error

setup_logging()

def get_start_end_dates(date: str = None) -> tuple:
    if date:
        start_date = datetime.strptime(date, '%Y-%m-%d')
        end_date = start_date + timedelta(days=1)  # До конца дня
    else:
        now = datetime.now()
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now
    return start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')

def fetch_funnel_data(api_token: str, date_from: str, date_to: str) -> dict:
    url = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail'
    headers = {'Authorization': api_token}
    params = {
        "brandNames": [],
        "objectIDs": [],
        "tagIDs": [],
        "nmIDs": [],
        "timezone": "Europe/Moscow",
        "period": {
            "begin": date_from,
            "end": date_to
        },
        "orderBy": {
            "field": "ordersSumRub",
            "mode": "desc"
        },
        "page": 1
    }

    try:
        response = requests.post(url, headers=headers, json=params)
        response.raise_for_status()

        return response.json()
    except requests.RequestException as e:
        log_error(f"Error fetching funnel data: {e}")
        return {}

def extract_card_stats(card: dict, date_from: str, owner: str) -> dict:
    statistics = card.get("statistics", {}).get("selectedPeriod", {})
    conversions = statistics.get("conversions", {})
    stocks = card.get("stocks", {})

    return {
        "nmID": card.get("nmID"),
        "date": datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S').date(),
        "vendorCode": card.get("vendorCode"),
        "productType": card.get("object", {}).get("name"),
        "brandName": card.get("brandName"),
        "openCardCount": statistics.get("openCardCount"),
        "addToCartCount": statistics.get("addToCartCount"),
        "ordersCount": statistics.get("ordersCount"),
        "buyoutsCount": statistics.get("buyoutsCount"),
        "cancelCount": statistics.get("cancelCount"),
        "addToCartPercent": conversions.get("addToCartPercent"),
        "cartToOrderPercent": conversions.get("cartToOrderPercent"),
        "buyoutsPercent": conversions.get("buyoutsPercent"),
        "ordersSumRub": statistics.get("ordersSumRub"),
        "buyoutsSumRub": statistics.get("buyoutsSumRub"),
        "cancelSumRub": statistics.get("cancelSumRub"),
        "avgPriceRub": statistics.get("avgPriceRub"),
        "avgOrdersCountPerDay": statistics.get("avgOrdersCountPerDay"),
        "stocksMp": stocks.get("stocksMp"),
        "stocksWb": stocks.get("stocksWb"),
        "owner": owner
    }

def process_funnel_data(date: str = None):
    database_url = get_database_url()
    session = get_session(database_url)
    tokens_from_env = get_api_tokens()

    tokens = [
        {'token': tokens_from_env.get('wb_api_token_1'), 'name': 'Д'},
        {'token': tokens_from_env.get('wb_api_token_2'), 'name': 'С'},
        {'token': tokens_from_env.get('wb_api_token_3'), 'name': 'Б'}
    ]
    date_from, date_to = get_start_end_dates(date)
    all_data = []

    for token_data in tokens:
        token = token_data['token']
        owner = token_data['name']
        data = fetch_funnel_data(token, date_from, date_to)
        for card in data.get("data", {}).get("cards", []):
            card_stat = extract_card_stats(card, date_from, owner)
            upsert_product(session, card_stat["nmID"], card_stat["vendorCode"])
            all_data.append(card_stat)

    upsert_funnel_data(session, all_data)
    session.close()
    log_info(f"Funnel data processed for {date_from.split()[0]}")

if __name__ == '__main__':
    process_funnel_data()


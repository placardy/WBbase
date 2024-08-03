# import requests
# from datetime import datetime
# from utils.env_loader import get_api_tokens, get_database_url
# from utils.db_utils import get_session, upsert_ads_data
# from utils.logging_utils import setup_logging, log_info, log_error
#
# setup_logging()
#
# def get_date_string(date=None):
#     if date:
#         print("IF DATE", date)
#         return datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
#     else:
#         print("DATE = NONE", date)
#         return datetime.now().strftime('%Y-%m-%d')
#
# def fetch_campaign_data(api_token, date, status):
#     url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'
#     headers = {'Authorization': api_token}
#     params = {"status": status}
#
#     try:
#         response = requests.post(url, headers=headers, params=params)
#         response.raise_for_status()
#         if response.status_code == 204:
#             return []
#
#         campaigns = response.json()
#         stats_url = 'https://advert-api.wildberries.ru/adv/v2/fullstats'
#         params = [{'id': c['advertId'], 'dates': [date]} for c in campaigns]
#         res = requests.post(stats_url, headers=headers, json=params)
#         res.raise_for_status()
#         if res.status_code == 204:
#             return []
#
#         campaigns_stats = res.json()
#         print('stats', status)
#         print(campaigns_stats)
#
#         camp_data = []
#         for company in campaigns_stats:
#             if 'days' not in company or not company['days']:
#                 continue
#             if 'apps' not in company['days'][0] or not company['days'][0]['apps']:
#                 continue
#             if 'nm' not in company['days'][0]['apps'][0] or not company['days'][0]['apps'][0]['nm']:
#                 continue
#
#             company_stat = {
#                 'productName': company['days'][0]['apps'][0]['nm'][0]['name'],
#                 'adID': company['advertId'],
#                 'nmID': company['days'][0]['apps'][0]['nm'][0]['nmId'],
#                 'views': company.get('views', 0),
#                 "clicks": company.get("clicks", 0),
#                 "ctr": company.get("ctr", 0.0),
#                 "cpc": company.get("cpc", 0.0),
#                 "sum": company.get("sum", 0.0),
#                 "atbs": company.get("atbs", 0),
#                 "orders": company.get("orders", 0),
#                 "cr": company.get("cr", 0),
#                 "shks": company.get("shks", 0),
#                 "sum_price": company.get("sum_price", 0.0),
#                 "date": datetime.strptime(date, '%Y-%m-%d').date(),
#                 "status": status
#             }
#             camp_data.append(company_stat)
#
#         return camp_data
#     except requests.RequestException as e:
#         log_error(f"Error fetching campaign data: {e}")
#         return []
#
# def process_ads_data(date=None):
#     database_url = get_database_url()
#     session = get_session(database_url)
#
#     tokens = get_api_tokens().values()
#     date_str = get_date_string(date)
#     all_data = []
#
#     for token in tokens:
#         active_data = fetch_campaign_data(token, date_str, status=9)
#         inactive_data = fetch_campaign_data(token, date_str, status=11)
#         all_data.extend(active_data)
#         all_data.extend(inactive_data)
#
#     upsert_ads_data(session, all_data)
#     session.close()
#     log_info(f"Ads data processed for {date_str}")
#
# if __name__ == '__main__':
#     process_ads_data()


import requests
from datetime import datetime
from utils.env_loader import get_api_tokens, get_database_url
from utils.db_utils import get_session, upsert_ads_data
from utils.logging_utils import setup_logging, log_info, log_error

setup_logging()

def get_date_string(date: str = None) -> str:
    if date:
        return datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
    else:
        return datetime.now().strftime('%Y-%m-%d')

def fetch_campaign_data(api_token: str, date: str, status: int) -> list:
    url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'
    headers = {'Authorization': api_token}
    params = {"status": status}

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 204:
            return []

        campaigns = response.json()
        if not campaigns:
            return []

        stats_url = 'https://advert-api.wildberries.ru/adv/v2/fullstats'
        params = [{'id': c['advertId'], 'dates': [date]} for c in campaigns]
        res = requests.post(stats_url, headers=headers, json=params)
        res.raise_for_status()
        if res.status_code == 204:
            return []

        campaigns_stats = res.json()
        camp_data = []
        for company in campaigns_stats:
            days = company.get('days', [])
            if not days or not days[0].get('apps', []) or not days[0]['apps'][0].get('nm', []):
                continue

            nm = days[0]['apps'][0]['nm'][0]
            company_stat = {
                'productName': nm.get('name', ''),
                'adID': company['advertId'],
                'nmID': nm.get('nmId', 0),
                'views': company.get('views', 0),
                "clicks": company.get("clicks", 0),
                "ctr": company.get("ctr", 0.0),
                "cpc": company.get("cpc", 0.0),
                "sum": company.get("sum", 0.0),
                "atbs": company.get("atbs", 0),
                "orders": company.get("orders", 0),
                "cr": company.get("cr", 0),
                "shks": company.get("shks", 0),
                "sum_price": company.get("sum_price", 0.0),
                "date": datetime.strptime(date, '%Y-%m-%d').date(),
                "status": status
            }
            camp_data.append(company_stat)

        return camp_data
    except requests.RequestException as e:
        log_error(f"Error fetching campaign data: {e}")
        return []

def process_ads_data(date: str = None):
    database_url = get_database_url()
    session = get_session(database_url)

    tokens = get_api_tokens().values()
    date_str = get_date_string(date)
    all_data = []

    def fetch_and_append_data(status: int):
        for token in tokens:
            data = fetch_campaign_data(token, date_str, status)
            all_data.extend(data)

    fetch_and_append_data(status=9)
    fetch_and_append_data(status=11)

    upsert_ads_data(session, all_data)
    session.close()
    log_info(f"Ads data processed for {date_str}")

if __name__ == '__main__':
    process_ads_data()

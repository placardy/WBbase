from datetime import datetime, timedelta
from data_fetchers.funnel_fetcher import process_funnel_data
from data_fetchers.ads_fetcher import process_ads_data
from utils.logging_utils import setup_logging, log_info

setup_logging()

def main():
    current_time = datetime.now()
    current_hour = current_time.hour
    if current_hour == 0:
        previous_day = (current_time - timedelta(days=1)).strftime('%Y-%m-%d')
        process_funnel_data(previous_day)
        process_ads_data(previous_day)
    else:
        process_funnel_data('2024-08-02')
        process_ads_data('2024-08-02')

if __name__ == '__main__':
    log_info("Application started")
    main()
    log_info("Application finished")

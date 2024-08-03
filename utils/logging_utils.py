import logging

def setup_logging(log_file='app.log'):
    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)
import logging
import os


# https://stackoverflow.com/questions/45701478/log-from-multiple-python-files-into-single-log-file-in-python
# https://stackoverflow.com/questions/11029717/how-do-i-disable-log-messages-from-the-requests-library

def get_logger(name):
    log_file = os.getenv("LOG_FILE")
    log_level = os.getenv("LOGGING_LEVEL")
    log_format = '%(asctime)s  %(name)14s  %(levelname)5s  %(message)s'
    logging.basicConfig(level=log_level,
                        format=log_format,
                        filename=log_file,
                        filemode='w')
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("github.Requester").setLevel(logging.WARNING)
    return logging.getLogger(name)

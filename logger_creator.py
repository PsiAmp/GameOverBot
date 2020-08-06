import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

# Init logger that will be visible in Global scope
def init_logger(name, is_debug=False):
    # Is assigned to a platform logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not is_debug:
        client = google.cloud.logging.Client()
        handler = CloudLoggingHandler(client)
        logger.addHandler(handler)
    return logger
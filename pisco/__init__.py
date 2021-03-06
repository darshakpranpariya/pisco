from pisco.knife.knife_client import KnifeClient
from pisco.loggers.config import config_logger
import logging

# Configure the logger
config_logger(log_level=logging.INFO)

# Knife client defined as singleton
client = KnifeClient()

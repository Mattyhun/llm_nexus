import os
import sys
import json
import colorlog
import logging as log
from datetime import datetime


def initialize_logging(debug=False):
    '''
    Initialize logging for the project. Creates a log directory if it does not exist.
    If -d is in the command line arguments, displays debug level logs
    '''
    if not os.path.exists("log"):
        os.makedirs("log")
    start_time = datetime.now().strftime("%Y-%m-%dT%H-%M")
    logging_level = log.INFO
    if any(arg in ['-d', '--d', '--debug', '-debug'] for arg in sys.argv) or debug:
        logging_level = log.DEBUG

    log.basicConfig(level=log.DEBUG, filename='log/test_' + start_time,
                    format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')  # This goes to the log file

    # Set up colorlog for console log
    console_log = log.getLogger()

    # Format log colors
    colored_formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s][%(levelname)s] %(message)s%(reset)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    # Create console handler with the colored formatter
    ch = log.StreamHandler()
    ch.setLevel(logging_level)
    ch.setFormatter(colored_formatter)
    console_log.addHandler(ch)


# Load API keys from secrets file
with open('secrets/api_keys.json') as file:
    api_keys = json.load(file)

OPENAI_API_KEY = api_keys['openaiApiKey']
HUGGINGFACE_API_KEY = api_keys['huggingfaceApiKey']

VM_NAME = "isolated-test-vm"
VM_ZONE = "europe-west3-c"
GCP_USERNAME = "sardibarnabas"

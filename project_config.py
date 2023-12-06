import os
import sys
import logging as log
import colorlog
import json
from datetime import datetime

def initialize_logging(debug=False):
    if not os.path.exists("log"):
        os.makedirs("log")
    start_time = datetime.now().strftime("%Y-%m-%dT%H-%M")
    logging_level = log.INFO
    if any(arg in ['-d', '--d', '--debug', '-debug'] for arg in sys.argv) or debug:
        logging_level = log.DEBUG

    log.basicConfig(level=log.DEBUG, filename='log/test_' + start_time, format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')  # This goes to the log file
    
    # Set up colorlog for console log
    console_log = log.getLogger()
    
    # Create a formatter where you can specify colors for various levels
    # Here, errors are set to be displayed in red and warnings in yellow
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

linelen = 30
# phase_start_display = lambda phase_name: max(linelen-len(phase_name),1)
def phase_start_display(phase_name):
    hashtaglen = max(1, linelen-len(phase_name)//2)
    hashtags = '#' * hashtaglen
    log.info("%s %s %s", hashtags, phase_name, hashtags)

def phase_end_display():
    log.info("")

# with open('local_secrets/secrets.json') as file:
#     migrationSecrets = json.load(file)



VM_NAME = "isolated-test-vm"
VM_ZONE = "europe-west3-c"
GCP_USERNAME = "sardibarnabas"
import os
import logging as log

def validate_file_path(file_path):
    """
    Check if a given path is a valid file
    """
    if not os.path.exists(file_path):
        log.error("Path does not exist: %s", file_path)
        return False
    elif not os.path.isfile(file_path):
        log.error("Path is not a file: %s", file_path)
        return False
    elif os.path.getsize(file_path) == 0:
        log.error("File is empty: %s", file_path)
        return False
    else:
        log.info("File path is valid: %s", file_path)
        return True
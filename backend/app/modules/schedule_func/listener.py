import logging
from apscheduler.events import *

# set apscheduler_error_log logger
fmt = "%(asctime)s : %(levelname)s : %(message)s"
formatter = logging.Formatter(fmt)
aps_error_logger = logging.getLogger('apscheduler_error_log')
aps_error_fh = logging.FileHandler('logs/apscheduler_error_log.log')
aps_error_fh.setLevel(logging.DEBUG)
aps_error_fh.setFormatter(formatter)
aps_error_logger.addHandler(aps_error_fh)

def aps_listener(event):
    if event.code == EVENT_JOB_ERROR:
        aps_error_logger.error(event.job_id + ': The job has error !')
    elif event.code == EVENT_JOB_MISSED:
        aps_error_logger.error(event.job_id + ': The job has missed :(')
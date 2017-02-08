import sys
import os
import logging
import logging.handlers

logger = logging.getLogger()

is_debug = bool(int(os.environ.get('DEBUG', '0')))

if is_debug is True:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(format)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# TODO(dustin): This all does not work for a Linux system. Just omit the "address" parameter completely.
if sys.platform == 'darwin':
    address = '/var/run/syslog'
elif os.path.exists('/dev/log'):
    address = '/dev/log'
else:
    address = ('localhost', 514)

ch = logging.handlers.SysLogHandler(
        address, 
        facility=logging.handlers.SysLogHandler.LOG_LOCAL0)

ch.setFormatter(formatter)
logger.addHandler(ch)

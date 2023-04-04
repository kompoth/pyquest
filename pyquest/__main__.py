import argparse
import logging

from pyquest.bot import start_bot
from pyquest.config import config


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', default='info')
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        filename='logs/app.log',
        encoding='utf-8',
        filemode='w',
        level=args.log_level.upper(),
        format='%(asctime)s %(levelname)8s [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Set higher logging level for apscheduler: it gives very detailed log
    if logging.root.level > logging.DEBUG:
        logging.getLogger('apscheduler').setLevel(logging.WARNING)
    else:
        logging.getLogger('apscheduler').setLevel(logging.INFO)

    # Run app
    start_bot()

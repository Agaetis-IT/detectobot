# -*- coding: utf-8 -*-

from __future__ import print_function
from app import create_app
import logging
from logging.config import fileConfig
from config import params
import os


dirname = os.path.dirname(__file__)
logging_conf = os.path.join(dirname, 'logging.conf')
fileConfig(logging_conf, disable_existing_loggers=False)

_logger = logging.getLogger(__name__)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#entry point.
application = create_app()

if __name__ == '__main__':
    # Entry point
    _logger.info("starting Detectobot")
    application.run(host=params["app.host"], port=params["app.port"], debug=True,processes=1,threaded=False)

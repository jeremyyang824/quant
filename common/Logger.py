# -*- coding: utf-8 -*-

import logging


class Logger:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def __call__(self, name=__name__):
        return logging.getLogger(name)


logger_factory = Logger()

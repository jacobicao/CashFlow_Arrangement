#!/usr/bin/env python
# encoding: utf-8
import os
if not os.path.exists('log'):
    os.mkdir('log')
if os.path.exists('log/Cash_out_log.txt'):
    os.remove('log/Cash_out_log.txt')

import logging
logger = logging.getLogger('Cash_out_log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('log/Cash_out_log.txt')
fh.setLevel(logging.INFO)
logger.addHandler(fh)

# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# logger.addHandler(ch)

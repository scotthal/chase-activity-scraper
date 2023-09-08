#!/usr/bin/env python3
from scrape.chase import OutputRecordFormatter
from scrape.chase import OutputRecord
from scrape.chase import Chase
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

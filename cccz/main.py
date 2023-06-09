import os

import cccz.cfg as cfg
from .scraper import ChmiScaper
from .data import StreamLitVis


class App:
    def __init__(self):
        self._scraper = ChmiScaper()
        self._vis = StreamLitVis()

    def start(self, do_scrape=False):
        self._check_data_dir()
        self._run(do_scrape)

    def stop(self):
        pass

    def _run(self, do_scrape):
        if do_scrape:
            self._scraper.scrape()
        self._vis.start()

    @staticmethod
    def _check_data_dir():
        if not os.path.exists(cfg.DATA_DIR):
            os.mkdir(cfg.DATA_DIR)

from .scraper import ChmiScaper


class App:
    def __init__(self):
        self._scraper = ChmiScaper()

    def start(self, do_scrape=False):
        self._run(do_scrape)

    def stop(self):
        pass

    def _run(self, do_scrape):
        if do_scrape:
            self._scraper.scrape()

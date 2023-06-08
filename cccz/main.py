from .scraper import ChmiScaper


class App:
    def __init__(self):
        self._scraper = ChmiScaper()

    def start(self):
        self._run()

    def stop(self):
        pass

    def _run(self):
        self._scraper.scrape()

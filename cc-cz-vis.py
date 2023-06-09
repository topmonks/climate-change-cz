import sys

from cccz.main import App

if __name__ == '__main__':
    do_scrape = sys.argv[0] == '1' or sys.argv[0].lower() == 'y'
    app = App()
    app.start(do_scrape)

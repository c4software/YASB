import logging
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup


class Plugin():
    def __init__(self, settings):
        logging.info("[Image Lazy Loading] Init")

    def run(self, settings, content, fields):
        soup = BeautifulSoup(content.decode('utf-8', 'ignore'), "html.parser")
        imgs = soup.findAll('img')
        for img in imgs:
            img.attrs['loading'] = 'lazy'

        return str(soup)

    def teardown(self, settings):
        logging.info("[Image Lazy Loading] Teardown")
        pass
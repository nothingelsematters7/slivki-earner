# -*- coding: utf-8 -*-

from selenium import webdriver

__all__ = (
    'BasePage',
)


class BasePage(object):
    def __init__(self, browser=None):
        super(BasePage, self).__init__()
        if browser:
            self.browser = browser
        else:
            self.browser = webdriver.Firefox()

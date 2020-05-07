#!/usr/bin/env python3


class RadioStation():
    def __init__(self, s):
        self.id = s['id']
        self.name = s['name']
        self.url = s['url']
        self.views = s['views']

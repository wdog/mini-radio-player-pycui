#!/usr/bin/env python3


class RadioStation():
    def __init__(self, s):
        self.name = s['name']
        self.url = s['url']

    def __str__(self):
        return self.name

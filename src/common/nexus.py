# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-10 23:28:10
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 01:16:56
import random
from threading import Lock


class Nexus(object):
    _lock = Lock()
    crestalInControl = None
    crestalRemain = None
    population = None
    zealot = None
    status = {}
    _amond = None

    def __init__(self):
        self._amond = random.randint(20, 100)
        self.crestalRemain = self._amond * 100 + (self._amond / 5 + 1) * 100
        self.crestalInControl = 0
        self.population = 0
        self.zealot = 0

    def collect(self, amount=1000):
        with self._lock:
            if self.crestalRemain < amount:
                self.crestalInControl += self.crestalRemain
                self.crestalRemain = 0
            else:
                self.crestalRemain -= amount
                self.crestalInControl += amount

    def getStatus(self, role):
        if role == 'archon':
            return {
                'crestalInControl': self.crestalInControl,
                'crestalRemain': self.crestalRemain,
                'population': self.population,
                'zealot': self.zealot
            }
        elif role == 'pylon_transporter':
            return {
                'crestalInControl': self.crestalInControl,
                'population': self.population
            }
        elif role == 'portal':
            return {
                'crestalInControl': self.crestalInControl,
                'population': self.population,
                'zealot': self.zealot
            }
        else:
            return {}

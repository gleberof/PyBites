from collections import namedtuple
from datetime import datetime

Transaction = namedtuple('Transaction', 'giver points date')
Transaction.__new__.__defaults__ = (datetime.now(),)  # http://bit.ly/2rmiUrL


class User:
    def __init__(self, name):
        self.name = name
        self._transactions = []

    def __str__(self):
        return f'{self.name} has a karma of {self.karma} and {self.fans} fans'

    def __add__(self, transaction):
        self._transactions.append(transaction)

    @property
    def karma(self):
        return sum(self.points)

    @property
    def fans(self):
        return len(set([t.giver for t in self._transactions]))

    @property
    def points(self):
        return [t.points for t in self._transactions]




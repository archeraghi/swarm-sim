from collections import deque
from enum import Enum

from lib.oppnet.communication import Message
from lib.oppnet.meta import process_event, EventType


class BufferStrategy(Enum):
    fifo = 0
    lifo = 1


class MessageStore(deque):
    """
    A simple expansion of collections.deque that implements fifo and lifo strategies.
    """

    def __init__(self, init=None, maxlen=None, strategy=BufferStrategy.fifo):
        """
        :param init: Initial deque.
        :type init: Iterable
        :param maxlen: Maximum length of the deque.
        :type maxlen: int
        :param strategy: Buffering strategy of the deque.
        :type strategy: :class:`~messagestore.BufferStrategy` or string
        """
        self.keys = {}
        if type(strategy) == str:
            try:
                self.strategy = BufferStrategy[strategy]
            except ValueError:
                self.strategy = BufferStrategy.fifo
        else:
            self.strategy = strategy
        if not init:
            super().__init__(maxlen=maxlen)
        else:
            super().__init__(init, maxlen=maxlen)

    def __len__(self):
        return super().__len__()

    def append(self, m: Message):
        # pop the right element if max len reached
        if self.contains_key(m.key):
            return
        if self.maxlen == len(self):
            k = list(self)[0].key
            if self.strategy == BufferStrategy.lifo:
                k = list(self)[-1].key
                super().pop()
            try:
                self.keys.pop(k)
            except KeyError:
                pass

        super().append(m)
        self.__append_key__(m.key, self.index(m))

        if self.maxlen == len(self):
            # manually raise an OverFlowError for protocol purposes
            raise OverflowError

    def remove(self, message):
        try:
            super().remove(message)
            self.keys.pop(message.key)
        except ValueError:
            pass
        except KeyError:
            pass

    def contains_key(self, key):
        return key in self.keys

    def get_by_key(self, key):
        return list(self)[self.keys[key]]

    def __append_key__(self, key, m_index):
        if key not in self.keys:
            self.keys[key] = m_index

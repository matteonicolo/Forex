from __future__ import print_function

from abc import ABCMeta, abstractmethod
import datetime
try:
    import Queue as queue
except ImportError:
    import queue

from event import FillEvent, OrderEvent

class ExecutionHandler(object):
    """
    Itera gli elementi e simula il collegamento e apertura/chiusura
    ordini con un broker
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event):
        """
        Parametri:
        event - Contiene un oggetto Event con le informazioni dell'ordine.
        """
        raise NotImplementedError("Should implement execute_order()")


class SimulatedExecutionHandler(ExecutionHandler):
    def __init__(self,events):
        """
        Parametri:
        events - La coda degli oggetti Event
        """
        self.events = events

    def execute_order(self, event):
        """
        Parametri:
        event - Contiene un oggetto Event con le informazioni dell'ordine.
        """
        if event.type == 'ORDER':
            fill_event = FillEvent(
                datetime.datetime.utcnow(), event.symbol,
                'OANDA', event.quantity, event.direction, None, event.commission
            )
            self.events.put(fill_event)

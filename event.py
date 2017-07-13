from __future__ import print_function

class Event(object):
    """
    Event è una classe che si occupa di gestire i segnali da Portfolio e
    Strategy creando eventi conseguenti
    """
    pass



class MarketEvent(Event):
    """
    Gestisce l'evento di ricezione di un aggiornamento di mercato con la barra
    (candela) corrispondente
    """

    def __init__(self):
        """
        Inizializza il MarketEvent
        """
        self.type = "MARKET"



class SignalEvent(Event):
    """
    Gestisce l'evento di invio di un Signal da un oggetto Strategy.
    Questo è ricevuto da un oggetto Portfolio e agisce di conseguenza
    """

    def __init__(self, strategy_id, symbol, datetime, signal_type, strength):
        """
        Inizializza il SignalEvent.

        Parameters:
        strategy_id - L'id della strategia che ha generato il segnale
        symbol - Il simbolo del ticker, es. ’EUR_USD’.
        datetime - La data nella quale il segnale è stato generato.
        signal_type - ’LONG’ o ’SHORT’.
        strength - Un fattore di "aggiustamento" per scalare le quantità del portfolio.
        Per le strategie di pairs trading.
        """

        self.type = "SIGNAL"
        self.strategy_id = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength



class  OrderEvent(Event):
    """
    Gestisce l'evento di un invio di un Order all'execution system.
    L'ordine contiene un simbolo(es.EUR_USD) e un tipo(Market), quantità e direzione.
    """

    def __init__(self, symbol, order_type, quantity, direction, commission):
        """
        Inizializza il tipo di ordine, impostandolo su Market order (’MKT’), ha
        una quantità (intera) e una direzione (’BUY’ o ’SELL’).
        Parametri:
        symbol - Lo strumento da tradare.
        order_type - ’MKT’ per gli ordini Market.
        quantity - Intero non negativo per la quantità.
        direction - ’BUY’ o ’SELL’ per long e short.
        commission - commissione (per il forex spread)
        """

        self.type = "ORDER"
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
        self.commission = commission


    def print_order(self):
        """
        Crea l'output dei valori con l'ordine
        """

        print(
           "Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" %
           (self.symbol, self.order_type, self.quantity, self.direction)
        )



class FillEvent(Event):
    """
    Gestisce l'esecuzione di un ordine presso un broker.
    Acquisisce la quantità dello strumento tradato e a che prezzo.
    """

    def __init__(self, timeindex, symbol, exchange, quantity,
                direction, fill_cost, commission):
                """
                Parametri:
                timeindex - Il momento nel quale l'ordine viene eseguito
                symbol - Lo strumento tradato.
                exchange - Il mercato nel quale l'ordine viene riempito.
                quantity - La quantità tradata.
                direction - La direzione dell'operazione (’BUY’ o ’SELL’)
                fill_cost - Il valore dell'holding.
                commission - Eventuali commisioni del broker.
                """

                self.type = "FILL"
                self.timeindex = timeindex
                self.symbol = symbol
                self.exchange = exchange
                self.quantity = quantity
                self.direction = direction
                self.fill_cost = fill_cost
                self.commission = commission

                #Calcola la commisione
                if commission is None:
                    pass
                else:
                    self.commission = commission

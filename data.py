from __future__ import print_function

from abc import ABCMeta, abstractmethod
import datetime
import os, os.path

import numpy as np
import pandas as pd
import json
import oandapyV20.endpoints.instruments as instruments
from oandapyV20 import API
from setup import account_id, key, api

from event import MarketEvent

class DataHandler(object):
    """
    Classe che si occupa di gestire lo storico dei prezzi.
    Invia i dati dei prezzi in base alla data storica simulando
    la connessione ad un broker.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        for i in range (1):
            HistoricCSVDataHandler_instance = HistoricCSVDataHandler()
            subchans.append(HistoricCSVDataHandler_instance)

    @abstractmethod
    def get_latest_bar(self, symbol):
       """
       Ritorna l'ultima candela aggiornata.
       """
       raise NotImplementedError("Should implement get_latest_bar()")

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
       """
       Ritorna le ultime N candele
       """
       raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def get_latest_bar_datetime(self, symbol):
       """
       Restituisce una data nel formato pythoniano
       """
       raise NotImplementedError("Should implementget_latest_bar_datetime()")

    @abstractmethod
    def get_latest_bar_value(self, symbol, val_type):
       raise NotImplementedError("Should implementget_latest_bar_value()")

    @abstractmethod
    def get_latest_bars_values(self, symbol, val_type, N=1):
       """
       Restituisce le ultime N candele.
       """
       raise NotImplementedError("Should implement get_latest_bars_values()")

    @abstractmethod
    def update_bars(self):
        raise NotImplementedError("bla")

class HistoricCSVDataHandler(DataHandler):
        """
        Legge il file CSV dello strumento richiesto restituendo il
        prezzo simulando la connessione ad un broker
        """

        def __init__(self, events, csv_dir, symbol_list):
           """
           Parametri:
           events - La coda di eventi.
           csv_dir - Locazione assoluta dei file CSV dei prezzi
           symbol_list - Una lista delle stringhe degli strumenti
           """

           self.events = events
           self.csv_dir = csv_dir
           self.symbol_list = symbol_list

           self.symbol_data = {}
           self.latest_symbol_data = {}
           self.continue_backtest = True

           self._open_convert_csv_files()

        def _open_convert_csv_files(self):
               """
               Apre il file csv dalla directory assegnata, convertendoli
               in un DataFrame di Pandas  con un dizionario dei simboli
               """
               comb_index = None
               for s in self.symbol_list:
                   #carica il file senza informazioni header
                   self.symbol_data[s] = pd.io.parsers.read_csv(self.csv_dir,
                       header = 0, index_col = 0, parse_dates = True,
                       names = [
                          'datetime', 'open', 'high', 'low',
                          'close', 'volume', 'adj_close', 'bid'
                       ]
                   ).sort()

               if comb_index is None:
                     comb_index = self.symbol_data[s].index
               else:
                     comb_index.union(self.symbol_data[s].index)

               self.latest_symbol_data[s] = []

               for s in self.symbol_list:
                 self.symbol_data[s] = self.symbol_data[s].\
                    reindex(index=comb_index, method='pad').iterrows()

        def _get_new_bar(self,symbol):
               """
               Ritorna l'ultima candela dal file dei dati
               """

               for b in self.symbol_data[symbol]:
                   yield b

        def get_latest_bar(self, symbol):
               """
               Ritorna l'ultima barra dalla lista di latest_symbol
               """

               try:
                   bars_list = self.latest_symbol_data[symbol]
               except KeyError:
                   print("Symbol not avaible")
                   raise
               else:
                   return bars_list[-1]

        def get_latest_bars(self, symbol, N=1):
               """
               Ritorna l'ultima N barra dalla lista di latest_symbol
               """

               try:
                   bars_list = self.latest_symbol_data[symbol]
                   print(bars_list)
               except KeyError:
                   print("Symbol not avaible")
                   raise
               else:
                   return bars_list[-N:]


        def get_latest_bar_datetime(self, symbol):
               try:
                   bars_list = self.latest_symbol_data[symbol]
               except KeyError:
                   print("Symbol not avaible")
                   raise
               else:
                   return bars_list[-1][0]

        def get_latest_bar_value(self, symbol, val_type):
               try:
                   bars_list = self.latest_symbol_data[symbol]
               except KeyError:
                   print("Symbol not avaible")
                   raise
               else:
                   return getattr(bars_list[-1][1], val_type)

        def update_bars(self):
               for s in self.symbol_list:
                   try:
                       bar = next(self._get_new_bar(s))
                   except StopIteration:
                       self.continue_backtest = False
                   else:
                       if bar is not None:
                           self.latest_symbol_data[s].append(bar)
                   self.events.put(MarketEvent())

        def get_latest_bars_values(self, symbol, val_type, N=1):
            try:
                bars_list = self.get_latest_bars(symbol, N)
            except KeyError:
                print("That symbol is not available in the historical data set.")
                raise
            else:
                return np.array([getattr(b[1], val_type) for b in bars_list])


class BetaDataHandler(DataHandler):
    """
    beta della nuova versione del data handler
    """

    def __init__(self, events, csv_dir, symbol_list):
        """
         events - La coda di eventi.
         csv_dir - Locazione assoluta dei file CSV dei prezzi
         symbol_list - Una lista delle stringhe degli strumenti
         """

         self.events = events
         self.csv_dir = csv_dir
         self.symbol_list = symbol_list

         self.symbol_data = {}
         self.latest_symbol_data = {}

         self.continue_backtest = True
         self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        """
        Apre il file csv dalla directory assegnata, convertendoli
        in un DataFrame di Pandas  con un dizionario dei simboli
        """
        for s in self.symbol_list:
            self.symbol_data[s] = pd.read_csv(self.csv_dir,
                names = [
                    'datetime', 'open', 'high', 'low',
                    'close', 'volume', 'adj_close', 'bid'
                ])

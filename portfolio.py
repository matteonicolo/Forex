from __future__ import print_function

import datetime
from math import floor
try:
    import Queue as queue
except ImportError:
    import queue

import numpy as np
import pandas as pd

from event import FillEvent, OrderEvent
from performance import create_sharpe_ratio, create_drawdowns


class Portfolio(object):
    """
    La classe Portfolio si occupa della gestione delle posizioni
    """
    def __init__(self, bars, events, start_date, initial_capital = 100000.0):
        """
        Parameters:
        bars - L'oggetto DataHandler con il currente valore di mercato.
        events - L'oggetto EventQueue (per i poco studiati è la coda di eventi).
        start_date - La data di inizio (bar) del portfolio.
        initial_capital - Il capitale di partenza in USD (dollaroni).
        """
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital

        self.all_positions = self.construct_all_positions()
        self.current_positions = dict(  (k,v) for k, v in \
            [(s, 0) for s in self.symbol_list] )

        self.all_holdings = self.construct_all_holdings()

        self.current_holdings = self.construct_current_holdings()

    def construct_all_positions(self):
            d = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
            d['datetime'] = self.start_date
            return [d]

    def construct_all_holdings(self):
            d = dict( (k,v) for k, v in [(s, 0.0) for s in self.symbol_list] )
            d['datetime'] = self.start_date
            d['cash'] = self.initial_capital
            d['commission'] = 0.0
            d['total'] = self.initial_capital
            return [d]

    def construct_current_holdings(self):
            d = dict( (k,v) for k, v in [(s, 0.0) for s in self.symbol_list] )
            d['cash'] = self.initial_capital
            d['commission'] = 0.0
            d['total'] = self.initial_capital
            return d

    def update_timeindex(self, event):
            """
            Aggiorna le posizioni aperte e il valore di mercato
            Usa MarketEvent dalla coda di eventi
            """

            latest_datetime = self.bars.get_latest_bar_datetime(
                self.symbol_list[0]
            )

            #aggiorna le posizioni
            #=====================
            dp = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
            dp['datetime'] = latest_datetime

            for s in self.symbol_list:
                dp[s] = self.current_positions[s]

            self.all_positions.append(dp)

            dh = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
            dh['datetime'] = latest_datetime
            dh['cash'] = self.current_holdings['cash']
            dh['total'] = self.current_holdings['cash']

            for s in self.symbol_list:
                market_value = self.current_positions[s] * \
                    self.bars.get_latest_bar_value(s, "adj_close")
                dh[s] = market_value
                dh['total'] += market_value

            self.all_holdings.append(dh)


    def update_positions_from_fill(self, fill):
            """
            Aggiorna la matrice della posizioni prendendo in
            considerazione il FillObject

            Parametri:
            fill - Il FillObject con cui aggiornare la posizione
            """

            fill_dir = 0
            if fill.direction == 'BUY':
                fill_dir = 1
            if fill.direction == 'SELL':
                fill_dir = -1

            self.current_positions[fill.symbol] += fill_dir*fill.quantity


    def update_holdings_from_fill(self, fill):
            """
            Parametri:
            fill - Il FillObject con cui aggiornare la posizione
            """

            fill_dir = 0
            if fill.direction == 'BUY':
                fill_dir = 1
            if fill.direction == 'SELL':
                fill_dir = -1

            fill_cost = self.bars.get_latest_bar_value(fill.symbol, "adj_close")
            cost = fill_dir * fill_cost * fill.quantity
            self.current_holdings[fill.symbol] += cost
            self.current_holdings['commission'] += fill.commission
            self.current_holdings['cash'] -= (cost + fill.commission)
            self.current_holdings['total'] -= (cost + fill.commission)


    def update_fill(self, event):
            """
            Aggiorna le posizioni del portfolio dal FillEvent
            """

            if event.type == 'FILL':
                self.update_positions_from_fill(event)
                self.update_holdings_from_fill(event)


    def generate_naive_order(self, signal):
            """
            Parametri:
            signal - La tupla che contiene le informazioni del Sygnal
            """

            order = None

            symbol = signal.symbol
            direction = signal.signal_type
            strength = signal.strength

            mkt_quantity = 100
            cur_quantity = self.current_positions[symbol]
            order_type = 'MKT'
            spread = self.bars.get_latest_bar_value(symbol, "close") - self.bars.get_latest_bar_value(symbol, "bid")

            if direction == 'LONG' and cur_quantity == 0:
                order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY', None)
            if direction == 'SHORT' and cur_quantity == 0:
                order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL', None)

            if direction == 'EXIT' and cur_quantity > 0:
                order = OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL', spread)
            if direction == 'EXIT' and cur_quantity < 0:
                order = OrderEvent(symbol, order_type, abs(cur_quantity), 'BUY', spread)

            return order


    def update_signals(self, event):
            """
            Reagisce al SignalEvent creando un ordine
            """

            if event.type == 'SIGNAL':
                order_event = self.generate_naive_order(event)
                self.events.put(order_event)


    def create_equity_curve(self):
            curve = pd.DataFrame(self.all_holdings)
            curve.set_index('datetime', inplace = True)
            curve['returns'] = curve['total'].pct_change()
            curve['equity_curve'] = (1.0 + curve['returns']).cumprod()
            self.equity_curve = curve


    def output_summary_stats(self, filename):
            """
            Statistiche create per il portfolio
            """

            total_return = self.equity_curve['equity_curve'][-1]
            returns = self.equity_curve['returns']
            pnl = self.equity_curve['equity_curve']

            sharpe_ratio = create_sharpe_ratio(returns, periods=252)
            drawdown, max_dd, dd_duration = create_drawdowns(pnl)
            self.equity_curve['drawdown'] = drawdown

            stats = [("Total Return", "%0.2f%%" % \
                       ((total_return - 1.0) * 100.0)),
                    ("Sharpe Ratio", "%0.2f%%" % sharpe_ratio),
                    ("Max Drawdown", "%0.2f%%" % (max_dd * 100.0)),
                    ("Drawdown Duration", "%f" % dd_duration)]
            self.equity_curve.to_csv(filename)
            return stats

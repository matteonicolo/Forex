from __future__ import print_function

import numpy as np
import pandas as pd

import os.path
import matplotlib.pyplot as plt


def create_sharpe_ratio(returns, periods = 252):
    """
    Parametri:
    returns - Una serie di Pandas che rappresents il ritorno in percentuale.
    periods - Daily (252), Hourly (252*6.5), Minutely(252*6.5*60) etc.
    """

    return np.sqrt(periods) * (np.mean(returns)) / np.std(returns)


def create_drawdowns(pnl):
    """
    Parametri:
    pnl - Una serie di Pandas che rappresents il ritorno in percentuale.
    Returns:
    drawdown, duration - Il valore massimo di drawdown e la sua durata.
    """

    #calcola la curva di ritono cumulativa
    hwm = [0]

    #crea il drawdown e la serie massima
    idx = pnl.index
    drawdown = pd.Series(index = idx)
    duration = pd.Series(index = idx)

    for t in range(1, len(idx)):
        hwm.append(max(hwm[t-1], pnl[t]))
        drawdown[t] = (hwm[t] - pnl[t])
        duration[t] = (0 if drawdown[t] == 0 else duration [t-1]+1)
    return drawdown, drawdown.max(), duration.max()


def plot_performance(filename):
    data = pd.io.parsers.read_csv(
          filename, header = 0,
          parse_dates=True, index_col=0
          ).sort()
          #disegna 3 grafici: curva dell'equity,
          #ritorno del periodo e i drowdown
          fig = plt.figure()
          fig.patch.set_facecolor('white')

          #stampa l'equity
          ax1 = fig.add_subplot(311, ylabel='Portfolio value, %')
          data['equity_curve'].plot(ax=ax1, color="blue", lw=2.)
          plt.grid(True)

          #stampa il ritorno
          ax2 = fig.add_subplot(312, ylabel='Period returns, %')
          data['returns'].plot(ax=ax2, color="black", lw=2.)
          plt.grid(True)

          #stampa il drawdown
          ax3 = fig.add_subplot(313, ylabel='Drawdowns, %')
          data['drawdown'].plot(ax=ax3, color="red", lw=2.)
          plt.grid(True)

          plt.show()


if __name__ == "__main__":
    print("Inserisci il nome del file.")
    nome_file = input()
    print ("Caricamento...")
    plot_performance(nome_file)

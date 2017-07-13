import sys
sys.path.append("C:/Users/GiovanniRocco/Anaconda3/envs/forex")

import time
import pandas as pd
import numpy as np
import json
import oandapyV20.endpoints.instruments as instruments
from oandapyV20 import API
from setup import account_id, key, api
import datetime
from rfc3339 import rfc3339

def download(date, currency):
    date2 = date + datetime.timedelta(minutes = 1)
    rc39 = rfc3339(date, utc=True, use_system_timezone=True)
    print(rc39)
    rc2 = rfc3339(date2, utc=True, use_system_timezone=True)
    r = instruments.InstrumentsCandles(instrument = currency,
    params = {"granularity" : "M1",
    "price" : "M",
    "from" : rc39,
    "to" : rc2})
    rs = api.request(r)
    response = rs.get("candles")
    print (response)
    return response

def bid(date, currency):
        date2 = date + datetime.timedelta(minutes = 1)
        rc39 = rfc3339(date, utc=True, use_system_timezone=True)
        rc2 = rfc3339(date2, utc=True, use_system_timezone=True)
        r = instruments.InstrumentsCandles(instrument=currency,
        params = {"granularity" : "M1",
        "price" : "B",
        "from" : rc39,
        "to" : rc2})
        rs = api.request(r)
        response = rs.get("candles")
        return response

def save(dw, data, date, openo, high, low, close, volume, adj_close, y, bid, vd):
    sc = dw[0]
    voluma = sc.get("volume")
    candle = sc.get("mid")

    apertura = candle.get("o")
    massimo = candle.get("h")
    minimo = candle.get("l")
    chiusura = candle.get("c")
    aggiusta_close = chiusura
    quantità = voluma
    baid = bid[0]
    daib = baid.get("bid")
    bd = daib.get("c")

    data.append(date)
    openo.append(apertura)
    high.append(massimo)
    low.append(minimo)
    close.append(chiusura)
    volume.append(quantità)
    adj_close.append(aggiusta_close)
    vd.append(bd)

def csv(date, openo, high, low, close, volume, adj_close, vd, cur):
    lista = {'Date': date,
    'Open' : openo,
    'High' : high,
    'Low' : low,
    'Close': close,
    'Volume': volume,
    'Adj Close': adj_close,
    'Bid': vd
    }
    filename = "%s.csv" % cur
    df = pd.DataFrame(lista, columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close', 'Bid'])
    df.to_csv(filename, index=False)

def null(dw, data, date, openo, high, low, close, volume, adj_close, y, bid, vd):
        data.append(date)
        openo.append("null")
        high.append("null")
        low.append("null")
        close.append("null")
        volume.append("null")
        adj_close.append("null")
        vd.append("null")


if __name__ == "__main__":
    start_date = datetime.datetime(2017, 6, 5, 0, 0, 0)
    end_date = datetime.datetime(2017, 6, 5, 1, 0, 0)
    cur = "EUR_USD"

    x = 0
    y = 0
    dw = 0
    oldD = None

    date = start_date
    print("Inizio download...")

    data = []
    openo = []
    high = []
    low = []
    close = []
    volume = []
    adj_close = []
    vd = []
    while date <= end_date:
        dw = download(date, cur)
        print (dw)
        bd = bid(date, cur)
        print (y)
        try:
            if dw[0] != oldD:
                save(dw, data, date, openo, high, low, close, volume, adj_close, y, bd, vd)
                oldD = dw[0]
        except IndexError:
            print (date)
            null(dw, data, date, openo, high, low, close, volume, adj_close, y, bd, vd)
        date = date + datetime.timedelta(minutes = 1)
        y = y + 1
        dw = None
        time.sleep(0.5)

    x = x + 1
    date = start_date
    print("saved")
    csv(data, openo, high, low, close, volume, adj_close, vd, cur)

    print("download completato.")

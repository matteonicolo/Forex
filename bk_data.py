import datetime
import time
import pandas as pd
import numpy as np
import json
import oandapyV20.endpoints.instruments as instruments
from oandapyV20 import API
from setup import account_id, key, api


def download(date, currency):
    date2 = date + datetime.timedelta(minutes = 1)
    rc39 = date.isoformat('T')
    rc2 = date2.isoformat('T')
    r = instruments.InstrumentsCandles(instrument=currency,
    params = {"granularity" : "M1",
    "start" : rc39,
    "end" : rc2,
    "candleFormat" : "midpoint"}
    )
    rs = api.request(r)
    response = rs.get("candles")
    return response

def save(dw, date, cur, openo, high, low, close, volume, adj_close):
    sc = dw[0]
    voluma = sc.get("volume")
    candle = sc.get("mid")

    apertura = candle.get("o")
    massimo = candle.get("h")
    minimo = candle.get("l")
    chiusura = candle.get("c")
    aggiusta_close = close
    quantità = voluma

    time = date.strftime("%Y-%m-%d.%H:%M:%S")
    data.append(time)
    openo.append(apertura)
    high.append(massimo)
    low.append(minimo)
    close.append(chiusura)
    volume.append(quantità)
    adj_close.append(aggiusta_close)

def csv(date, cur, openo, high, low, close, volume, adj_close):
    lista = {'Date': data,
    'Open' : openo,
    'High' : high,
    'Low' : low,
    'Close': close,
    'Volume': volume,
    'Adj Close': adj_close
    }
    filename = "%s.csv" % cur
    df = pd.DataFrame(lista, columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'])
    df.to_csv(filename, index=False)



if __name__ == "__main__":#settings
    start_date = datetime.datetime(2007,4,1,0,0,0)
    end_date = datetime.datetime(2007,4,1,1,0,0)
    major = ["EUR_USD"] #you can insert multiple currencies
    #settings end

    x = 0
    cur = major[x]
    dw = 0
    oldD = None

    date = start_date
    print("Starting...")

    while x <= (len(major) - 1):
        cur = major[x]
        data = []
        openo = []
        high = []
        low = []
        close = []
        volume = []
        adj_close = []
        while date <= end_date:
            dw = download(date, cur)
            if dw is not None and dw != oldD:
                print (date)
                save(dw, date, cur, openo, high, low, close, volume, adj_close)
            date = date + datetime.timedelta(minutes = 1)
            time.sleep(0.5)

        x = x + 1
        date = start_date
        print("file saved")
        csv(date, cur, openo, high, low, close, volume, adj_close)
        oldD = dw

    print("Completed")

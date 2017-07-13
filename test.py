from oandapyV20 import API
import json
from setup import account_id, key, api
import oandapyV20.endpoints.instruments as instruments
from datetime import datetime

r = instruments.InstrumentsCandles(instrument = "EUR_USD",
params = {"granularity" : "M1",
"price" : "M",
"count" : 1})
rs = api.request(r)
response = rs.get("candles")
print(response)

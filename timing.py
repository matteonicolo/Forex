import datetime, time
import pandas as pd
import numpy as np
from datetime import datetime

if __name__ == "__main__":
    #Settings
    cur = "EUR_USD" #currency (just one)
    data = pd.read_csv('/%s.csv' % cur) #Absolute directoryof csv file
    #DO NOT MODIFY THIS PART: /%s.csv' % cur
    start_date = datetime(2007, 4, 1, 0, 0, 0)
    end_date = datetime(2007, 4, 1, 1, 0, 0)
    ora_start = 0
    minuto_start = 0
    ora_fine = 1
    minuto_fine = 50
    #settings end

    time = data['Date'].tolist()
    apertura = data['Open'].tolist()
    chiusura = data['Close'].tolist()
    x = 0
    dati = []
    oggetto = start_date
    print("-----")

    while True:
        if datetime.strptime(time[x], '%Y-%m-%d.%H:%M:%S') == start_date:
            ###
            while oggetto < end_date:
                oggetto = datetime.strptime(time[x], '%Y-%m-%d.%H:%M:%S')
                print(oggetto.minute)

                if oggetto.hour == ora_start and oggetto.minute == minuto_start:
                    ap = apertura[x]
                    print(ap)
                    while oggetto.hour < ora_fine and oggetto.minute < minuto_fine:
                        x = x + 1
                        oggetto = datetime.strptime(time[x], '%Y-%m-%d.%H:%M:%S')
                    ch = chiusura[x]
                    diff = ch - ap
                    dati.append(diff)

                else:
                    x = x + 1
            ###
            break

        else:
            x = x + 1

    media = np.mean(dati)
    print("Average day difference: %f " % media)
    print("-----")

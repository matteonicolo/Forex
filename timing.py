import datetime, time
import pandas as pd
import numpy as np
from datetime import datetime

if __name__ == "__main__":
    #INSERIRE I SETTAGGI IN QUESTA SEZIONE
    cur = "EUR_USD" #METTI QUA IL NOME DELLA VALUTA
    data = pd.read_csv('C:/Users/GiovanniRocco/Anaconda3/envs/forex/tick/%s.csv' % cur)
    #INSERISCI LA DIRECTORY ASSOLUTA DELLA CARTELLA DEL FILE E AGGIUNGENDO QUESTO PEZZO:
    # /%s.csv' % cur
    start_date = datetime(2017, 6, 7, 0, 0, 0) #ANNO, MESE, GIORNO, ORA, MINUTO, SECONDO
    end_date = datetime(2017, 6, 8, 0, 0, 0)
    ora_start = 6
    minuto_start = 0
    ora_fine = 9
    minuto_fine = 0
    #DA QUA IN POI NON SI TOCCA!
    time = data['Date'].tolist()
    apertura = data['Open'].tolist()
    chiusura = data['Close'].tolist()
    x = 0
    diff = []
    ap = []
    cl = []
    dat = []
    oggetto = start_date
    print("-----")

    while True:
        mom = datetime.strptime(time[x], '%Y-%m-%d.%H:%M:%S')
        if mom == start_date:
            while mom < end_date:
                mom = datetime.strptime(time[x], '%Y-%m-%d.%H:%M:%S')
                op = apertura[x]
                le = chiusura[x]
                dat.append(mom)
                cl.append(le)
                ap.append(op)
                x = x + 1
            break

        else:
            x = x + 1


    x = 0

    while True:
        if dat[x].hours == ora_start and dat[x].minutes == minuto_start:
            openo = ap[x]
            while dat[x].hours < ora_fine and dat[x].minutes < minuto_fine:
                x = x + 1
            cloze = cl[x]
            diff.append(openo - cloze)
            break

        else:
            x = x + 1


    media = np.mean(dati)
    print("Variazione media: %f " % media)
    print("-----")

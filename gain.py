import dat
import dev
import time
import pandas as pd

def spectral():

    ldc = dev.ldc()
    att = dev.att()
    osa = dev.osa(False)

    x, y = dat.Arange(30, 5, -1)

    ldc.value(400)
    att.value(x[0])
    osa.write('INIT:CONT OFF')
    osa.write('INIT:IMM')
    time.sleep(2)

    pint = 6

    for i in range(len(x)):

        att.value(x[i])
        osa.write('INIT:IMM')
        osa.write('CALC:MARK:MAX')
        data = osa.query('CALC:MARK:Y?')

        x[i] = pint - float(x[i])
        y[i] = float(data)

        print(x[i], x[i], y[i], round(y[i]-x[i], 2))

    ldc.off()
    att.value(pint - x[0])
    osa.write('INIT:CONT ON')

    att.close()
    osa.close()

    df = {'Input power (mW)':x}
    df['Output power (mW)'] = y

    return pd.DataFrame(df)

def current():

    ldc = dev.ldc()
    osa = dev.osa(False)

    x, y = dat.Arange(100, 500, 25)

    ldc.value(int(x[0]))
    osa.write('INIT:CONT OFF')
    osa.write('INIT:IMM')
    time.sleep(2)

    for i in range(len(x)):

        ldc.value(int(x[i]))
        osa.write('INIT:IMM')
        osa.write('CALC:MARK:MAX')
        data = osa.query('CALC:MARK:Y?')

        y[i] = round(float(data) + 24.0, 3)

        print(x[i], y[i])

    osa.write('INIT:CONT ON')
    ldc.off()
    time.sleep(1)

    osa.close()
    ldc.close()

    df = {'Current (mA)':x}
    df['Power (mW)'] = y

    return pd.DataFrame(df)

def opm():

    att = dev.att()
    opm = dev.opm(15)

    pset, loss = 14, 3

    x, y = dat.Arange(40, 10, -1)

    opm.dBm(1, 1)
    att.value(x[0])
    time.sleep(2)

    for i in range(len(x)):

        att.value(x[i])
        output = opm.query(1, 1)

        x[i] = float(pset - loss - x[i])
        y[i] = float(output)

        print(x[i], y[i], y[i]-x[i])

    att.value(x[0])

    att.close()
    opm.close()

    df = {'Input power (mW)':x}
    df['Output power (mW)'] = y

    return pd.DataFrame(df)
import os
import sys
import dev
import dat
import time

def pdloss(filename, length):

    filename = dat.getfolder() + filename

    laser = dev.tld()
    laser.wavelength(1550)
    laser.close()

    dev.switch(3)

    pl2000 = dev.pdl()
    pdl, loss = pl2000.query()
    pl2000.close()

    dev.switch(2)

    time.sleep(1)

    loss = round(loss, 3)

    fp = open(filename + '-pdl.txt', 'a')
    fp.write(length + '\t' + str(pdl) + '\n')
    fp.close()

    fp = open(filename + '-loss.txt', 'a')
    fp.write(length + '\t' + str(loss) + '\n')
    fp.close()

    print(length + '\t' + str(pdl) + '\t' + str(loss))

def spectral(x):

    pdl  = [0 for i in range(len(x))]
    loss = [0 for i in range(len(x))]

    laser = dev.tld()
    pl200 = dev.pdl()

    dev.switch(3)

    pl200.write('SOUR 0')
    laser.write('outp1 on')
    time.sleep(1)

    laser.wavelength(x[0])

    for i in range(len(x)):

        laser.wavelength(x[i])

        pdl[i], loss[i] = pl200.query()

        print(str(x[i]) + '\t' + str(pdl[i]) + '\t' + str(loss[i]))

    laser.wavelength(x[0])

    dev.switch(2)
    laser.close()
    pl200.close()

    return pdl, loss

def sweep(filename, x, intrinsic, calibrating):

    pdl, loss = spectral(x)

    if calibrating:
        xlink, calink = dat.getdata('link-loss')

        for i in range(len(x)):
            for j in range(len(xlink)):
                if abs(xlink[j] - x[i]) < 0.01: 
                    loss[i] = round(loss[i] - calink[j] - intrinsic, 4)

    dat.save(filename + '-pdl', x, pdl)
    dat.save(filename + '-loss', x, loss)

if __name__ == '__main__':

    x, _ = dat.aranges(1520, 1570, 0.1)

    intrinsic = float(sys.argv[2])

    sweep(sys.argv[1], x, intrinsic, 1)

    pdloss(sys.argv[1], sys.argv[2])

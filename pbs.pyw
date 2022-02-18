import os
import sys
import dev
import dat
import numpy
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class Analyzer(Qw.QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.init_ui()

        self.init_osa()

    def init_ui(self):

        self.setGeometry(1000, 300, 240, 150)
        self.setWindowTitle('PBS Analyzer')
        self.setWindowIcon(Qg.QIcon('ni.png'))

        dat.Qbutton(self, self.OnGetTE, 'TE', 0, 0, 100)
        dat.Qbutton(self, self.OnGetTM, 'TM', 100, 0, 100)
        dat.Qbutton(self, self.OnCalER, 'Extinction Ratio', 0, 40, 200)
        dat.Qbutton(self, self.OnSave, 'Save', 0, 80, 200)

    def init_osa(self):

        osa = dev.osa(False)

        osa.write('CENT 1545NM')
        osa.write('SPAN 50NM')
        osa.write('BWID:RES 0.1NM')
        osa.write('POW:DC:RANG:LOW -70DBM')
        osa.write('INIT:CONT OFF')
        osa.write('INIT:IMM')

        xmin = float(osa.query('TRAC:DATA:X:STAR? TRA')) * 1e9
        xmax = float(osa.query('TRAC:DATA:X:STOP? TRA')) * 1e9
        xnum = float(osa.query('SENS:SWE:POIN?'))

        dx  = (xmax - xmin) / (xnum - 1.0)

        self.x = numpy.arange(xmin, xmax + dx * 0.1, dx)
        self.y = numpy.arange(xmin, xmax + dx * 0.1, dx)

        osa.write('INIT:CONT ON')
        osa.close()

    def OnGetSpectrum(self):

        self.osa.write('INIT:CONT OFF')
        self.osa.write('INIT:IMM')

        data = self.osa.query('TRAC:DATA:Y? TRA')
        data = data.replace('\n', '')
        data = data.split(',')

        self.osa.write('INIT:CONT ON')

        for i in range(len(data)): data[i] = float(data[i]) 

        return data

    def OnGetTE(self):

        self.te = self.OnGetSpectrum()
        plt.plot(self.x, self.te)
        plt.show()

    def OnGetTM(self):

        self.tm = self.OnGetSpectrum()
        plt.plot(self.x, self.tm)
        plt.show()

    def OnCalER(self):

        for i in range(len(self.y)): self.y[i] = self.te[i] - self.tm[i]
        
        plt.plot(self.x, self.y)
        plt.show()

    def OnSave(self):

        filename = Qw.QFileDialog.getSaveFileName(self, '', dat.getfolder(), '*.txt')[0]

        if filename:

            fp = open(filename, 'w')

            for i in range(len(self.x)):
                fp.write(str(self.x[i]) + '\t')
                fp.write(str(self.te[i]) + '\t')
                fp.write(str(self.tm[i]) + '\t')
                fp.write(str(self.y[i]) + '\n')

            fp.close()

if __name__ == '__main__':

    app = Qw.QApplication(sys.argv)
    exc = Analyzer()
    exc.show()
    sys.exit(app.exec_())

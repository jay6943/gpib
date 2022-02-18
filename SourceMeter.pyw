import sys
import dev
import dat
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class App(Qw.QWidget):

    def __init__(self):

        super().__init__()
        
        self.xtitles, self.ytitles = dat.titles()

        self.init_ui()
        
    def init_ui(self):

        self.setWindowTitle('KEITHLEY 2612B')
        self.setWindowIcon(Qg.QIcon('ni.png'))
        self.setGeometry(100, 100, 540, 290)

        dat.Qlabel(self, 'IA', 0, 0)
        dat.Qlabel(self, 'VA', 0, 40)
        dat.Qlabel(self, 'IB', 270, 0)
        dat.Qlabel(self, 'VB', 270, 40)
        dat.Qlabel(self, 'mA', 210, 0)
        dat.Qlabel(self, 'V', 210, 40)
        dat.Qlabel(self, 'mA', 480, 0)
        dat.Qlabel(self, 'V', 480, 40)

        dat.Qbutton(self, self.IAon, 'ON', 30, 0, 40)
        dat.Qbutton(self, self.IAoff, 'OFF', 80, 0, 40)
        dat.Qbutton(self, self.VAon, 'ON', 30, 40, 40)
        dat.Qbutton(self, self.VAoff, 'OFF', 80, 40, 40)
        dat.Qbutton(self, self.IBon, 'ON', 300, 0, 40)
        dat.Qbutton(self, self.IBoff, 'OFF', 350, 0, 40)
        dat.Qbutton(self, self.VBon, 'ON', 300, 40, 40)
        dat.Qbutton(self, self.VBoff, 'OFF', 350, 40, 40)

        self.IA = dat.Qedit(self, '0', 130, 0, 70)
        self.VA = dat.Qedit(self, '0', 400, 0, 70)
        self.IB = dat.Qedit(self, '0', 130, 40, 70)
        self.VB = dat.Qedit(self, '0', 400, 40, 70)

        dat.Qlabel(self, 'Start', 160, 90)
        dat.Qlabel(self, 'Stop', 280, 90)
        dat.Qlabel(self, 'Step', 400, 90)

        dat.Qlabel(self, 'I-V', 0, 120)
        dat.Qlabel(self, 'V-I', 0, 160)
        dat.Qlabel(self, 'mA', 480, 120)
        dat.Qlabel(self, 'V', 480, 160)

        dat.Qbutton(self, self.IVA, 'A', 30, 120, 40)
        dat.Qbutton(self, self.IVB, 'B', 80, 120, 40)
        dat.Qbutton(self, self.VIA, 'A', 30, 160, 40)
        dat.Qbutton(self, self.VIB, 'B', 80, 160, 40)

        self.Istart = dat.Qedit(self, '1.0', 130, 120, 100)
        self.Istop = dat.Qedit(self, '100.0', 250, 120, 100)
        self.Istep = dat.Qedit(self, '1.0', 370, 120, 100)
        self.Vstart = dat.Qedit(self, '-2.0', 130, 160, 100)
        self.Vstop = dat.Qedit(self, '3.0', 250, 160, 100)
        self.Vstep = dat.Qedit(self, '0.05', 370, 160, 100)

        self.filename = dat.Qedit(self, 'filename', 0, 220, 250)
        dat.Qbutton(self, self.onPlot, 'Plot', 340, 220, 40)
        dat.Qbutton(self, self.onFolder, 'Set Folder', 390, 220, 80)

        self.checkplot = dat.Qcheck(self, 'graph', 280, 220, 100)
        self.checkplot.setChecked(False)

    def IV(self, ch):

        start = float(self.Istart.text()) * 0.001
        stop = float(self.Istop.text()) * 0.001
        step = float(self.Istep.text()) * 0.001
        
        self.x = np.arange(start, stop + step * 0.1, step)

        n = len(self.x)

        xstr = str(start) + ',' + str(stop) + ',' + str(step) + ',' + str(n)
        xstr = '(' + ch + ',' + xstr + ')'

        ksm = dev.ivs()

        ksm.write('reset()')
        ksm.write(ch + '.source.limitv = 10')
        ksm.write('SweepILinMeasureV' + xstr)

        self.y = ksm.Vread(n, ch)

        ksm.close()

        filename = dat.getfolder() + '/' + self.filename.text() + '-IV'
        for i in range(n): self.x[i] = round(self.x[i] * 1000, 3)
        for i in range(n): self.y[i] = round(self.y[i], 6)
        dat.save(filename + '.txt', self.x, self.y)
        
        if self.checkplot.isChecked():
            plt.plot(self.x, self.y)
            plt.xlabel(dat.title(4))
            plt.ylabel(dat.title(5))
            plt.xlim(0, self.x[n-1])
            plt.ylim(min(self.y), max(self.y))
            plt.grid()
            plt.savefig(filename + '.png')
            plt.show()
            plt.close()

    def VI(self, ch):

        start = float(self.Vstart.text())
        stop = float(self.Vstop.text())
        step = float(self.Vstep.text())

        self.x = np.arange(start, stop + step * 0.1, step)

        n = len(self.x)

        xstr = str(start) + ',' + str(stop) + ',' + str(step) + ',' + str(n)
        xstr = '(' + ch + ',' + xstr + ')'

        ksm = dev.ivs()

        ksm.write('reset()')
        ksm.write(ch + '.source.limiti = 10e-3')
        ksm.write('SweepVLinMeasureI' + xstr)

        self.y = ksm.Iread(n, ch)

        ksm.close()

        filename = dat.getfolder() + '/' + self.filename.text() + '-VI'
        for i in range(n): self.x[i] = round(self.x[i], 3)
        for i in range(n): self.y[i] = round(self.y[i] * 1000, 6)
        dat.save(filename + '.txt', self.x, self.y)

        if self.checkplot.isChecked():
            plt.plot(self.x, self.y)
            plt.xlabel(dat.title(5))
            plt.ylabel(dat.title(4))
            plt.xlim(start, stop)
            plt.ylim(min(self.y), max(self.y))
            plt.grid()
            plt.savefig(filename + '.png')
            plt.show()
            plt.close()

    def ON(self, ch, src, value):

        if src == 'i': value = str(float(value) * 0.001)
        dc = '.OUTPUT_DCAMPS' if src == 'i' else '.OUTPUT_DCVOLTS'

        ksm = dev.ivs()
        ksm.write('reset()')
        ksm.write(ch + '.source.func = ' + ch + dc)
        ksm.write(ch + '.source.level' + src + ' = ' + value)
        ksm.write(ch + '.source.output = ' + ch + '.OUTPUT_ON')
        ksm.close()

    def OFF(self, ch):
        ksm = dev.ivs()
        ksm.write(ch + '.source.output = ' + ch + '.OUTPUT_OFF')
        ksm.close()

    def IAon(self):
        self.ON('smua', 'i', self.IA.text())

    def IBon(self):
        self.ON('smub', 'i', self.IB.text())

    def VAon(self):
        self.ON('smua', 'v', self.VA.text())

    def VBon(self):
        self.ON('smub', 'v', self.VB.text())

    def IAoff(self):
        self.OFF('smua')

    def IBoff(self):
        self.OFF('smub')

    def VAoff(self):
        self.OFF('smua')

    def VBoff(self):
        self.OFF('smub')

    def IVA(self):
        self.IV('smua')

    def IVB(self):
        self.IV('smub')

    def VIA(self):
        self.VI('smua')

    def VIB(self):
        self.VI('smub')

    def onFolder(self):

        folder = Qw.QFileDialog.getExistingDirectory(self, "Select Folder", dat.getfolder())

        if folder != '': dat.setfolder(folder)

    def onPlot(self):

        filename = Qw.QFileDialog.getOpenFileName(self, '', dat.getfolder(), '*.txt')[0]

        if filename:
            x, y = dat.getdata(filename)

            plt.plot(x, y)
            plt.xlabel(self.xtitle)
            plt.ylabel(self.ytitle)
            plt.grid()
            plt.show()
            plt.close()

if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())

import sys
import dev
import dat
import time
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

        self.setWindowTitle('VOA')
        self.setWindowIcon(Qg.QIcon('ni.png'))
        self.setGeometry(100, 100, 390, 170)

        dat.Qbutton(self, self.VOn, 'ON', 0, 0, 80)
        dat.Qbutton(self, self.VOff, 'OFF', 90, 0, 80)

        self.volt = dat.Qedit(self, '0', 180, 0, 170)

        dat.Qlabel(self, 'Start', 110, 30)
        dat.Qlabel(self, 'Stop', 200, 30)
        dat.Qlabel(self, 'Step', 290, 30)

        dat.Qbutton(self, self.OnScan, 'Run (Volt)', 0, 60, 80)

        self.Vstar = dat.Qedit(self, '0.0', 90, 60, 80)
        self.Vstop = dat.Qedit(self, '4.0', 180, 60, 80)
        self.Vstep = dat.Qedit(self, '0.1', 270, 60, 80)

        dat.Qbutton(self, self.onSave, 'Save', 0, 100, 80)
        dat.Qbutton(self, self.onFolder, 'Set Folder', 270, 100, 80)

    def OnScan(self):

        star = float(self.Vstar.text())
        stop = float(self.Vstop.text())
        step = float(self.Vstep.text())

        v = np.arange(star, stop + step * 0.1, step)

        self.x = []
        self.y = []

        dcp = dev.dcp()
        opm = dev.ando()

        dcp.write('APPL P25V, ' + self.Vstar.text() + ', 1.0')
        dcp.write('OUTP ON')

        for i in range(len(v)):
            v[i] = round(v[i], 3)
            dcp.write('APPL P25V, ' + str(v[i]) + ', 1.0')
            time.sleep(0.2)
            #time.sleep(0.5)

            a, b = opm.query()

            self.x.append(v[i])
            self.y.append(b)

            plt.cla()
            plt.plot(self.x, self.y)
            plt.grid()
            plt.xlabel(dat.title(5))
            plt.ylabel(dat.title(7))
            plt.pause(0.1)

        plt.show()
        
        dcp.write('APPL P25V, ' + self.Vstar.text() + ', 1.0')
        dcp.write('OUTP OFF')

        dcp.close()
        opm.close()

    def VOn(self):
        dcp = dev.dcp()
        dcp.write('APPL P25V, ' + self.volt.text() + ', 1.0')
        dcp.write('OUTP ON')
        dcp.close()

    def VOff(self):
        dcp = dev.dcp()
        dcp.write('OUTP OFF')
        dcp.close()

    def onSave(self):

        filename = Qw.QFileDialog.getSaveFileName(self, '', dat.getfolder(), '*.txt')[0]

        if filename:
            dat.save(filename, self.x, self.y)

            plt.cla()
            plt.plot(self.x, self.y)
            plt.xlabel(dat.title(5))
            plt.ylabel(dat.title(7))
            plt.grid()
            plt.savefig(filename[:len(filename)-4] + '.png')

    def onFolder(self):
        folder = Qw.QFileDialog.getExistingDirectory(self, "Select Folder", dat.getfolder())
        if folder != '': dat.setfolder(folder)

if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())

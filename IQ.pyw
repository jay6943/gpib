import os
import sys
import dev
import dat
import time
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class ExWindow(Qw.QMainWindow):
    
    def __init__(self):

        super().__init__()
            
        self.init_ui()
        
    def init_ui(self):

        self.setGeometry(300, 300, 260, 310)
        self.setWindowIcon(Qg.QIcon('ni.png'))
        self.setWindowTitle('IQ')

        dat.Qbutton(self, self.OnSave, 'Get && Save', 0, 0, 100)
        dat.Qbutton(self, self.OnData, 'Get I/Q', 0, 40, 100)
        dat.Qbutton(self, self.OnFolder, 'Set Folder', 120, 40, 100)
        dat.Qbutton(self, self.OnRun, 'Run', 0, 80, 100)
        dat.Qbutton(self, self.OnStop, 'Stop', 120, 80, 100)
        dat.Qbutton(self, self.OnTY, 'TY-plot', 0, 120, 100)
        dat.Qbutton(self, self.OnXY, 'XY-plot', 120, 120, 100)
        
        dat.Qbutton(self, self.OnTime, 'Time (us)', 120, 160, 100)
        dat.Qbutton(self, self.OnAmp, 'mV/Div', 120, 200, 100)
        dat.Qbutton(self, self.OnOff, 'Offset (mV)', 120, 240, 100)

        self.var = dat.Qedit(self, '', 0, 160, 100)
        self.amp = dat.Qedit(self, '', 0, 200, 100)
        self.off = dat.Qedit(self, '', 0, 240, 100)
        self.fit = dat.Qedit(self, '', 120, 0, 100)
        
        self.m = 4096

        dso = dev.dso(False)
        dso.write('CHAN1:COUP DC')
        dso.write('CHAN2:COUP DC')
        dso.write('WAV:POINTS:MODE RAW')
        dso.write('WAV:FORM ASCII')
        dso.write('WAV:POINTS ' + str(self.m))
        self.var.setText(str(round(dso.query('TIM:SCAL?') * 1e6, 3)))
        self.amp.setText(str(round(dso.query('CHAN1:SCAL?') * 1e3, 3)))
        self.off.setText(str(round(dso.query('CHAN1:OFFS?') * 1e3, 3)))
        dso.close()

    def GetData(self):

        dso = dev.dso(False)
        dso.write('TIM:FORM YT')
        dso.write('TIM:SCAL ' + str(float(self.var.text()) * 1e-6))
        dso.write('SINGLE')

        time.sleep(2)

        self.t = np.arange(self.m) * float(self.var.text()) * 0.04
        self.x = dso.getwave(1)
        self.y = dso.getwave(2)

        A = np.arange(float(self.m * 5)).reshape(5, self.m)
        B = -self.x * self.x
    
        A[0] = self.x * self.y * 2
        A[1] = self.y * self.y
        A[2] = self.x * 2
        A[3] = self.y * 2
        A[4] = 1

        k = np.dot(B, np.linalg.pinv(A))
        p = np.arcsin(np.sqrt(1 - k[0] * k[0] / k[1])) * 180 / np.pi
        
        if k[0] > 0: p = 180 - p
        
        self.phase = str(round(p, 1))
        self.fit.setText(self.phase)
        self.OnDraw()

        dso.write('RUN')
        dso.write('TIM:FORM XY')
        dso.close()

    def OnDraw(self):

        xtop = np.amax(self.x)
        xbas = np.amin(self.x)
        ytop = np.amax(self.y)
        ybas = np.amin(self.y)

        self.x = self.x - (xtop + xbas) * 0.5
        self.y = self.y - (ytop + ybas) * 0.5

        plt.close()
        plt.scatter(self.x, self.y, c='b', s=5)
        plt.axis('square')
        plt.title(self.phase + '$^o$')
        plt.xlabel('I (mV)', size=14)
        plt.ylabel('Q (mV)', size=14)
        plt.grid(True)

    def OnData(self):

        self.GetData()

        plt.show()

    def OnSave(self):

        self.GetData()

        filename = Qw.QFileDialog.getSaveFileName(self, '', dat.getfolder(), '*.txt')[0]

        if filename:

            fp = open(filename, 'w')
            for i in range(self.m):
                fp.write(str(round(self.t[i], 6)) + '\t')
                fp.write(str(round(self.x[i], 3)) + '\t')
                fp.write(str(round(self.y[i], 3)) + '\n')
            fp.close()
            
            plt.savefig(filename[:len(filename)-4] + '.png')

    def OnFolder(self):

        folder = Qw.QFileDialog.getExistingDirectory(self, "Select Folder", dat.getfolder())

        if folder != '': dat.setfolder(folder)

    def OnRun(self):
        dev.dso('RUN')
        
    def OnStop(self):
        dev.dso('SINGLE')
        
    def OnTY(self):        
        dev.dso('TIM:FORM YT')
        
    def OnXY(self):        
        dev.dso('TIM:FORM XY')
        
    def OnTime(self):
        dev.dso('TIM:SCAL ' + str(float(self.var.text()) * 1e-6))
        
    def OnAmp(self):
        dso = dev.dso(False)
        dev.dso('TIM:FORM YT')
        dso.write('CHAN1:SCAL ' + str(float(self.amp.text()) * 1e-3))
        dso.write('CHAN2:SCAL ' + str(float(self.amp.text()) * 1e-3))
        dev.dso('TIM:FORM XY')
        dso.close()

    def OnOff(self):
        dso = dev.dso(False)
        dev.dso('TIM:FORM YT')
        dso.write('CHAN1:OFFS ' + str(float(self.off.text()) * 1e-3))
        dso.write('CHAN2:OFFS ' + str(float(self.off.text()) * 1e-3))
        dev.dso('TIM:FORM XY')
        dso.close()

if __name__ == '__main__':

    app = Qw.QApplication(sys.argv)
    ex = ExWindow()
    ex.show()
    sys.exit(app.exec_())

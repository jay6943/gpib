import sys
import dat
import dev
import PyQt5.QtGui as Qg
import PyQt5.QtCore as Qc
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class ExWindow(Qw.QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.init_ui()
    
        osa = dev.osa(False)
        osa.write(':SENS:WAV:CENT ' + self.center.text() + 'NM')
        osa.write(':SENS:WAV:SPAN ' + self.span.text() + 'NM')
        '''
        osa.write(':SENS:BAND:RES ' + self.bandwidth.text() + 'NM')

        osa.write(':DISP:TRAC:Y1:RLEV ' + self.reference.text() + 'DBM')
        osa.write(':DISP:TRAC:Y1:PDIV ' + self.division.text() + 'DB')
        '''
        osa.close()

        self.getData = 0
        self.setSwitch = 1

    def init_ui(self):

        self.setWindowTitle('OSA')
        self.setWindowIcon(Qg.QIcon('ni.png'))
        self.setGeometry(300, 300, 420, 350)

        dat.Qbutton(self, self.OnCenter, 'Center (nm)', 0, 0, 120)
        dat.Qbutton(self, self.OnSpan, 'Span (nm)', 0, 40, 120)
        dat.Qbutton(self, self.OnBandwidth, 'Bandwidth (nm)', 0, 80, 120)
        dat.Qbutton(self, self.OnSensitivity, 'Sensitivity (dBm)', 0, 120, 120)
        dat.Qbutton(self, self.OnReference, 'Reference (dBm)', 0, 160, 120)
        dat.Qbutton(self, self.OnDivision, 'Division (dB)', 0, 200, 120)

        self.center = dat.Qedit(self, '1545', 130, 0, 120)
        self.span = dat.Qedit(self, '50', 130, 40, 120)
        self.bandwidth = dat.Qedit(self, '0.1', 130, 80, 120)
        self.sensitivity = dat.Qedit(self, '10', 130, 120, 120)
        self.reference = dat.Qedit(self, '0', 130, 160, 120)
        self.division = dat.Qedit(self, '10', 130, 200, 120)

        dat.Qbutton(self, self.OnScan, 'Get Spectrum', 0, 280, 120)
        dat.Qbutton(self, self.OnSave, 'Save', 260, 280, 120)
        dat.Qbutton(self, self.OnGetMax, 'Max', 260, 40, 120)
        dat.Qbutton(self, self.OnGetMin, 'Min', 260, 80, 120)
        dat.Qbutton(self, self.OnToPeak, 'Ref. to Peak', 260, 160, 120)
        dat.Qbutton(self, self.OnMarkCenter, 'Mark to Center', 260, 0, 120)
        dat.Qbutton(self, self.OnContinuous, 'Continuous', 0, 240, 120)
        dat.Qbutton(self, self.OnSingle, 'Stop', 130, 240, 120)
        dat.Qbutton(self, self.OnSwitch, 'Switch', 260, 240, 120)
        
    def OnSpan(self):
        dev.osa(':SENS:WAV:SPAN ' + self.span.text() + 'NM')

    def OnCenter(self):
        dev.osa(':SENS:WAV:CENT ' + self.center.text() + 'NM')

    def OnBandwidth(self):
        dev.osa(':SENS:BAND:RES ' + self.bandwidth.text() + 'NM')

    def OnSensitivity(self):
        dev.osa(':DISP:TRAC:Y1:RPOS ' + self.sensitivity.text() + 'DIV')

    def OnReference(self):
        dev.osa(':DISP:TRAC:Y1:RLEV ' + self.reference.text() + 'DBM')

    def OnDivision(self):
        dev.osa(':DISP:TRAC:Y1:PDIV ' + self.division.text() + 'DB')

    def OnGetMax(self):
        osa = dev.osa(False)
        osa.write(':CALC:MARK:MAX')
        x = float(osa.query(':CALC:MARK:X?')) * 1e9
        y = float(osa.query(':CALC:MARK:Y?'))
        osa.close()

        title = 'Max. Value'
        text = str(round(y, 2)) + ' dBm @' + str(round(x, 3)) + ' nm'

        Qw.QMessageBox.question(self, title, text, Qw.QMessageBox.Yes)

    def OnGetMin(self):
        osa = dev.osa(False)
        osa.write(':CALC:MARK:MIN')
        x = float(osa.query(':CALC:MARK:X?')) * 1e9
        y = float(osa.query(':CALC:MARK:Y?'))
        osa.close()

        title = 'Min. Value'
        text = str(round(y, 2)) + ' dBm @' + str(round(x, 3)) + ' nm'

        Qw.QMessageBox.question(self, title, text, Qw.QMessageBox.Yes)

    def OnToPeak(self):
        osa = dev.osa(False)
        osa.write(':CALC:MARK:MAX')
        y = float(osa.query(':CALC:MARK:Y?'))
        osa.close()
        
        self.reference.setText(str(round(y, 0)))
        self.OnReference()

    def OnMarkCenter(self):
        dev.osa(':CALC:MARK:SCEN')
        
    def OnContinuous(self):
        osa = dev.osa(False)
        osa.write(':INIT:SMOD REP')
        osa.write(':INIT:IMM')
        osa.close()
    
    def OnSingle(self):
        osa = dev.osa(False)
        osa.write(':INIT:SMOD SING')
        osa.write(':INIT:IMM')
        osa.close()

    def OnSwitch(self):
        dev.switch(self.setSwitch)
        self.setSwitch = 1 if self.setSwitch > 1 else 2

    def OnScan(self):

        osa = dev.osa(False)
        osa.timeout = 50000
        
        self.OnSingle()

        m = int(osa.query(':SENS:SWE:POIN?'))

        x = osa.query(':TRAC:DATA:X? TRA')
        x = x.replace('\n', '')
        x = x.split(',')
        xmin = float(x[0]) * 1e9
        xmax = float(x[-1]) * 1e9
        
        dx  = (xmax - xmin) / float(m - 1)

        self.x = [xmin + i * dx for i in range(m)]
        self.y = [0 for i in range(m)]

        y = osa.query(':TRAC:DATA:Y? TRA')
        y = y.replace('\n', '')
        y = y.split(',')

        for i in range(len(y)): self.y[i] = float(y[i]) 

        self.OnContinuous()

        osa.close()

        plt.plot(self.x, self.y)
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Output power (dBm)')
        plt.xlim(xmin, xmax)
        plt.grid()
        plt.show()

        self.getData = 1

    def OnSave(self):

        filename = Qw.QFileDialog.getSaveFileName(self, '', dat.getfolder(), '*.txt')[0]

        if self.getData and filename: dat.save(filename, self.x, self.y)

if __name__ == '__main__':

    app = Qw.QApplication(sys.argv)
    ex = ExWindow()
    ex.show()
    sys.exit(app.exec_())

import sys
import dat
import dev
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

class App(Qw.QWidget):

    def __init__(self):

        super().__init__()
        
        self.init_ui()
        
    def init_ui(self):

        self.setWindowTitle('SLD')
        self.setWindowIcon(Qg.QIcon('ni.png'))
        self.setGeometry(100, 100, 300, 150)

        dat.Qbutton(self, self.OnPower, 'Power (dBm)', 0, 0, 150)
        dat.Qbutton(self, self.OnWavelength, 'Wavelength (nm)', 0, 40, 150)
        self.power = dat.Qedit(self, '10', 160, 0, 100)
        self.wavelength = dat.Qedit(self, '1550', 160, 40, 100)

        dat.Qbutton(self, self.On, 'ON', 0, 80, 100)
        dat.Qbutton(self, self.Off, 'OFF', 160, 80, 100)

    def OnPower(self):
        tld = dev.N7711A()
        tld.write('sour1:pow ' + self.power.text() + 'dBm')      
        tld.close()

    def OnWavelength(self):
        tld = dev.N7711A()
        tld.write('SOUR1:WAV ' + self.wavelength.text() + 'NM')
        tld.close()

    def On(self):
        tld = dev.N7711A()
        tld.write('sour1:pow:stat 1')
        tld.close()

    def Off(self):
        tld = dev.N7711A()
        tld.write('OUTP1 OFF')
        tld.close()

if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())

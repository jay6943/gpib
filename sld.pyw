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
        self.setGeometry(500, 50, 250, 150)

        dat.Qbutton(self, self.OnCurrent, 'Current', 0, 0, 100)
        dat.Qbutton(self, self.OnTEC, 'TEC', 0, 40, 100)
        self.current = dat.Qedit(self, '200.0', 110, 0, 100)
        self.tec = dat.Qedit(self, '25.0', 110, 40, 100)

        dat.Qbutton(self, self.On, 'Enable', 0, 80, 100)
        dat.Qbutton(self, self.Off, 'Disable', 110, 80, 100)

    def write(self, command):
        sld = dev.usbserial('COM4')
        sld.write(command)
        sld.close()

    def OnCurrent(self):
        self.write('current=' + self.current.text())

    def OnTEC(self):
        self.write('target=' + self.tec.text())

    def On(self):
        self.write('enable=1')

    def Off(self):
        sld = dev.usbserial('COM4')
        sld.write('current=0')
        sld.write('enable=0')
        sld.close()

if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())

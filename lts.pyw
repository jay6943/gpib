import sys
import dat
import dev
import serial
import thorlabs_apt
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

class App(Qw.QWidget):

    def __init__(self):

        super().__init__()
        
        self.init_ui()
        
    def init_ui(self):

        self.setWindowTitle('LTS300/M')
        self.setWindowIcon(Qg.QIcon('thorlabs.png'))
        self.setGeometry(100, 50, 210, 310)

        dat.Qbutton(self, self.OnMove, 'MOVE', 0, 0, 50)
        dat.Qbutton(self, self.OnHome, 'HOME', 120, 0, 50)
        dat.Qbutton(self, self.On1p, '+', 0, 40, 50)
        dat.Qbutton(self, self.On1n, '-', 60, 40, 50)
        dat.Qbutton(self, self.On2p, '+', 0, 80, 50)
        dat.Qbutton(self, self.On2n, '-', 60, 80, 50)
        dat.Qbutton(self, self.On3p, '+', 0, 120, 50)
        dat.Qbutton(self, self.On3n, '-', 60, 120, 50)
        dat.Qbutton(self, self.On4p, '+', 0, 160, 50)
        dat.Qbutton(self, self.On4n, '-', 60, 160, 50)
        dat.Qbutton(self, self.On5p, '+', 0, 200, 50)
        dat.Qbutton(self, self.On5n, '-', 60, 200, 50)
        dat.Qbutton(self, self.On6p, '+', 0, 240, 50)
        dat.Qbutton(self, self.On6n, '-', 60, 240, 50)

        self.move = dat.Qedit(self, '10000', 60, 0, 50)
        self.On1 = dat.Qedit(self, '10', 120, 40, 50)
        self.On2 = dat.Qedit(self, '50', 120, 80, 50)
        self.On3 = dat.Qedit(self, '100', 120, 120, 50)
        self.On4 = dat.Qedit(self, '250', 120, 160, 50)
        self.On5 = dat.Qedit(self, '1550', 120, 200, 50)
        self.On6 = dat.Qedit(self, '7750', 120, 240, 50)

        thorlabs_apt.list_available_devices()
        self.motor = thorlabs_apt.Motor(45151484)

    def OnMove(self):
        value = self.move.text()
        value = float(value) * 0.001
        value = round(value, 3)
        self.motor.move_by(value)

    def OnHome(self):
        self.motor.move_home(True)

    def OnStep(self, text, sign):
        self.motor.move_by(round(sign * float(text) * 0.001, 3))

    def On1p(self):
        self.OnStep(self.On1.text(), 1)

    def On1n(self):
        self.OnStep(self.On1.text(), -1)

    def On2p(self):
        self.OnStep(self.On2.text(), 1)

    def On2n(self):
        self.OnStep(self.On2.text(), -1)

    def On3p(self):
        self.OnStep(self.On3.text(), 1)

    def On3n(self):
        self.OnStep(self.On3.text(), -1)

    def On4p(self):
        self.OnStep(self.On4.text(), 1)

    def On4n(self):
        self.OnStep(self.On4.text(), -1)

    def On5p(self):
        self.OnStep(self.On5.text(), 1)

    def On5n(self):
        self.OnStep(self.On5.text(), -1)

    def On6p(self):
        self.OnStep(self.On6.text(), 1)

    def On6n(self):
        self.OnStep(self.On6.text(), -1)

if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())

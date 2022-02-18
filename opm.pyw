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

        self.setWindowTitle('Optical Power Meter')
        self.setWindowIcon(Qg.QIcon('ni.png'))
        self.setGeometry(100, 100, 250, 110)

        dat.Qbutton(self, self.CH1, 'CH1', 0, 0, 100)
        dat.Qbutton(self, self.CH2, 'CH2', 0, 40, 100)

        self.dbm1 = dat.Qedit(self, '', 110, 0, 100)
        self.dbm2 = dat.Qedit(self, '', 110, 40, 100)

    def CH1(self):
        opm = dev.opm(20)
        self.dbm1.setText(str(opm.query(2, 1)))
        opm.close()

    def CH2(self):
        opm = dev.opm(20)
        self.dbm2.setText(str(opm.query(2, 2)))
        opm.close()

if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())

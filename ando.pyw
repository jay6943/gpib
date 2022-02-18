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

        self.setWindowTitle('ANDO')
        self.setWindowIcon(Qg.QIcon('ni.png'))
        self.setGeometry(100, 100, 250, 110)

        dat.Qbutton(self, self.OnGet, 'ON', 0, 0, 100)

        self.A = dat.Qedit(self, '', 110, 0, 100)
        self.B = dat.Qedit(self, '', 110, 40, 100)

    def OnGet(self):
        opm = dev.ando()
        A, B = opm.query()
        self.A.setText(str(A))
        self.B.setText(str(B))
        opm.close()

if __name__ ==  '__main__':
    
    app = Qw.QApplication(sys.argv)
    MyWindow = App()
    MyWindow.show()
    sys.exit(app.exec_())

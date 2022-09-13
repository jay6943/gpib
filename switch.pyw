import sys
import dat
import dev
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

class ExWindow(Qw.QMainWindow):
  
  def __init__(self):

    super().__init__()

    self.setWindowTitle('Switch')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(260, 300, 250, 110)

    dat.Qbutton(self, self.On1, '1.', 0, 0, 100)
    dat.Qbutton(self, self.On2, '2. OPM', 110, 0, 100)
    dat.Qbutton(self, self.On3, '3.', 0, 40, 100)
    dat.Qbutton(self, self.On4, '4. OSA', 110, 40, 100)

  def On1(self):
    dev.switch(1)

  def On2(self):
    dev.switch(2)

  def On3(self):
    dev.switch(3)

  def On4(self):
    dev.switch(4)

if __name__ == '__main__':

  app = Qw.QApplication(sys.argv)
  ex = ExWindow()
  ex.show()
  sys.exit(app.exec_())

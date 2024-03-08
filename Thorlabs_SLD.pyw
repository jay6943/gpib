import sys
import dat
import dev
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

port = 'COM8'


def write(command):
  sld = dev.usbserial(port)
  sld.write(command)
  sld.close()


def current_on():
  sld = dev.usbserial(port)
  sld.write('enable=1')
  sld.close()


def current_off():
  sld = dev.usbserial(port)
  sld.write('current=0')
  sld.write('enable=0')
  sld.close()


class App(Qw.QWidget):

  def __init__(self):

    super().__init__()
    
    self.setWindowTitle('SLD')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(500, 50, 250, 150)

    dat.Qbutton(self, self.OnCurrent, 'Current', 0, 0, 100)
    dat.Qbutton(self, self.OnTEC, 'TEC', 0, 40, 100)
    self.current = dat.Qedit(self, '200.0', 110, 0, 100)
    self.tec = dat.Qedit(self, '25.0', 110, 40, 100)

    dat.Qbutton(self, current_on, 'Enable', 0, 80, 100)
    dat.Qbutton(self, current_off, 'Disable', 110, 80, 100)

  def OnCurrent(self): write('current=' + self.current.text())
  def OnTEC(self): write('target=' + self.tec.text())

if __name__ ==  '__main__':
  
  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())

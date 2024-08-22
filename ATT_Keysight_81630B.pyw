import sys
import dev
import dat
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw


class Attenuator(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    self.setGeometry(4000, 500, 260, 150)
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setWindowTitle('Attenuator')

    self.address = dat.Qcombo(self, 0, 0, 220)
    self.address.addItem('TCPIP0::192.168.0.25::inst0::INSTR')
    self.address.addItem('GPIB0::17::INSTR')
    self.var = dat.Qedit(self, '30', 0, 40, 100)
    dat.Qlabel(self, 'dB', 70, 30, 20)

    dat.Qbutton(self, self.attenuator, 'Attenuation', 120, 40, 100)
    dat.Qbutton(self, self.attON, 'ON', 0, 80, 100)
    dat.Qbutton(self, self.attOFF, 'OFF', 120, 80, 100)

  def attON(self):
    att = dev.Keysight_81630B_attenuator(self.address.currentText())
    print(att.query('*IDN?'))
    att.write(':OUTP2:STAT ON')
    print(att.query(':OUTP2:STAT?'))
    att.close()

  def attOFF(self):
    att = dev.Keysight_81630B_attenuator(self.address.currentText())
    print(att.query('*IDN?'))
    att.write(':OUTP2:STAT OFF')
    print(att.query(':OUTP2:STAT?'))
    att.close()

  def attenuator(self):
    att = dev.Keysight_81630B_attenuator(self.address.currentText())
    att.write(':INP2:ATT ' + self.var.text() + 'dB')
    att.close()

if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Attenuator()
  window.show()
  sys.exit(app.exec_())

import sys
import dat
import dev
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

class Keysight_N7711A(Qw.QWidget):

  def __init__(self):
    super().__init__()

    self.setWindowTitle('Keysight N7711A')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(100, 100, 300, 150)

    dat.Qbutton(self, self.OnPower, 'Power (dBm)', 0, 0, 150)
    dat.Qbutton(self, self.OnWavelength, 'Wavelength (nm)', 0, 40, 150)
    self.power = dat.Qedit(self, '13', 160, 0, 100)
    self.wavelength = dat.Qedit(self, '1550', 160, 40, 100)

    dat.Qbutton(self, self.Power_On, 'ON', 0, 80, 100)
    dat.Qbutton(self, self.Power_Off, 'OFF', 160, 80, 100)

  def OnPower(self):
    tld = dev.Keysight_N7711A_tunalble_laser()
    tld.write('POW ' + self.power.text() + 'DBM')
    tld.close()

  def OnWavelength(self):
    tld = dev.Keysight_N7711A_tunalble_laser()
    tld.write('POW:STAT 0')
    tld.write('WAV:AUTO 1')
    tld.write('WAV ' + self.wavelength.text() + 'NM')
    tld.write('POW:STAT 1')
    tld.close()

  def Power_On(self):
    tld = dev.Keysight_N7711A_tunalble_laser()
    tld.write('POW:STAT 0')
    tld.write('WAV:AUTO 1')
    tld.write('WAV ' + self.wavelength.text() + 'NM')
    tld.write('POW ' + self.power.text() + 'DBM')
    tld.write('POW:STAT 1')
    tld.close()

  def Power_Off(self):
    tld = dev.Keysight_N7711A_tunalble_laser()
    tld.write('WAV ' + self.wavelength.text() + 'NM')
    tld.write('POW ' + self.power.text() + 'DBM')
    tld.write('POW:STAT 0')
    tld.close()

if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Keysight_N7711A()
  window.show()
  sys.exit(app.exec_())

import os
import sys
import dat
import dev
import time
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class App(Qw.QWidget):

  def __init__(self):

    super().__init__()

    self.setWindowTitle('TLD')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(100, 100, 300, 270)

    dat.Qbutton(self, self.OnPower, 'Power (dBm)', 0, 0, 150)
    dat.Qbutton(self, self.OnWavelength, 'Wavelength (nm)', 0, 40, 150)

    self.power = dat.Qedit(self, '3', 160, 0, 100)
    self.wavelength = dat.Qedit(self, '1528', 160, 40, 100)
    self.start = dat.Qedit(self, '1528', 160, 80, 100)
    self.stop = dat.Qedit(self, '1529', 160, 120, 100)
    self.step = dat.Qedit(self, '0.1', 160, 160, 100)

    dat.Qbutton(self, self.On, 'ON', 0, 200, 100)
    dat.Qbutton(self, self.Off, 'OFF', 160, 200, 100)
    dat.Qbutton(self, self.Sweep, 'Sweep', 0, 80, 150)
    dat.Qbutton(self, self.OnSave, 'Save', 0, 160, 150)

  def OnPower(self):
    tld = dev.tld81640A()
    tld.write('SOUR0:POW ' + self.power.text() + 'DBM')
    tld.close()

  def OnWavelength(self):
    tld = dev.tld81640A()
    tld.write('SOUR0:WAV ' + self.wavelength.text() + 'NM')
    tld.close()

  def On(self):
    tld = dev.tld81640A()
    tld.write('OUTP0 ON')
    tld.close()

  def Off(self):
    tld = dev.tld81640A()
    tld.write('OUTP0 OFF')
    tld.close()

  def Sweep(self):
    tld = dev.tld81640A()
    opm = dev.ando()

    start = float(self.start.text())
    stop = float(self.stop.text())
    step = float(self.step.text())
    
    self.x = np.round(np.arange(start, stop + step, step), 2)
    self.y = []
    
    for k in self.x:
      tld.write('SOUR0:WAV ' + str(k) + 'NM')
      time.sleep(0.5)
      a, _ = opm.query()
      self.y = self.y + [float(str(a))]
      print(k, str(a))
    
    tld.close()
    opm.close()

    xt = np.linspace(self.x[0], self.x[-1], 6)
    yt = np.linspace(-40, 0, 5)

    plt.close()
    plt.figure(dpi=150)
    plt.plot(self.x, self.y)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Output (dBm)')
    plt.xlim(xt[0], xt[-1])
    plt.ylim(yt[0], yt[-1])
    plt.xticks(xt)
    plt.yticks(yt)
    plt.grid()
    plt.show()

  def OnSave(self):

    fp = Qw.QFileDialog.getSaveFileName(self, '', dat.getfolder(), '*.txt')[0]

    if fp:
      data = [self.x, self.y]
      np.savetxt(fp, np.array(data).transpose(), fmt='%.3f')
      plt.savefig(fp[:len(fp)-4] + '.png')

      folder = os.path.dirname(fp)
      if folder != dat.getfolder(): dat.setfolder(folder)

if __name__ ==  '__main__':
  
  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())

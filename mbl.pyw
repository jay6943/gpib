import sys
import cfg
import dev
import dat
import time
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt


def write(command):
  mbl = dev.usbserial('COM3')
  mbl.write(command)
  time.sleep(0.1)
  mbl.close()


def read(command):
  mbl = dev.usbserial('COM3')
  data = mbl.read(command).decode('utf-8')
  mbl.close()

  icut = 0
  for i in range(len(data)):
    if data[i] == ' ': icut = i

  return str(float(data[icut + 1:]))


class App(Qw.QWidget):
  def __init__(self):
    super().__init__()
    
    mbl = dev.usbserial('COM3')
    mbl.write('dur:value 1')
    mbl.write('freq:value 0')
    mbl.close()

    current = self.read('curr:value?')
    temperature = self.read('tec:temp:value?')

    self.setWindowTitle('MAIMAN Electronics')
    self.setWindowIcon(Qg.QIcon('../doc/ni.png'))
    self.setGeometry(100, 100, 440, 180)

    dat.Qbutton(self, self.SetCurrent, 'Current (mA)', 0, 0, 100)
    dat.Qbutton(self, self.OnCurrent, 'ON', 110, 0, 90)
    dat.Qbutton(self, self.OffCurrent, 'OFF', 210, 0, 90)
    dat.Qbutton(self, self.SetTEC, 'TEC (\'C)', 0, 40, 100)
    dat.Qbutton(self, self.OnTEC, 'ON', 110, 40, 90)
    dat.Qbutton(self, self.OffTEC, 'OFF', 210, 40, 90)
    self.current = dat.Qedit(self, current, 310, 0, 90)
    self.tec = dat.Qedit(self, temperature, 310, 40, 90)

    dat.Qlabel(self, 'Start', 130, 80, 100)
    dat.Qlabel(self, 'Stop', 200, 80, 100)
    dat.Qlabel(self, 'Step', 270, 80, 100)

    dat.Qbutton(self, self.LIcurve, 'L-I Curve (mA)', 0, 110, 100)

    self.star = dat.Qedit(self, '0', 110, 110, 60)
    self.stop = dat.Qedit(self, '50', 180, 110, 60)
    self.step = dat.Qedit(self, '1', 250, 110, 60)

    dat.Qbutton(self, self.OnSave, 'Save', 320, 110, 80)

    self.x = []
    self.y = []

  def LIcurve(self):
    mbl = dev.usbserial('COM3')
    opm = dev.Keysight_81630B_photodiode()
    
    star = float(self.star.text())
    stop = float(self.stop.text())
    step = float(self.step.text())
    
    x, y = [], []
    
    mbl.write('dev:start on')
    time.sleep(1)

    for i in np.arange(star, stop + step * 0.1, step):

      mbl.write(f'curr:value {i:.1f}')

      plt.pause(0.2)

      x.append(i)
      y.append(10 ** (opm.read(1, 1) * 0.1))

      if i > star:
        plt.cla()
        plt.plot(x, y)
        plt.xlabel('Current (mA)')
        plt.ylabel('Output power (mW)')
        plt.xlim(star, i)
        plt.grid()

    mbl.write(f'curr:value {star:.1f}')
    mbl.write('dev:start off')
    
    plt.show()

    mbl.close()
    opm.close()

    self.x = x
    self.y = y

    n = len(x)

    for i in range(n): self.x[i] = round(self.x[i], 1)
    for i in range(n): self.y[i] = round(self.y[i], 6)

  def SetCurrent(self):
    self.write(f'curr:value {self.current.text()}')

  def OnCurrent(self):
    self.write('dev:start on')

  def OffCurrent(self):
    self.write('dev:start off')

  def SetTEC(self):
    self.write(f'tec:temp:value {self.tec.text()}')

  def OnTEC(self):
    self.write('tec:start on')

  def OffTEC(self):
    self.write('tec:start off')

  def OnSave(self):
    f = Qw.QFileDialog.getSaveFileName(self, '', cfg.get_folder(), '*.txt')

    if f[0]:
      np.savetxt(f[0], np.array([self.x, self.y]).transpose())

if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())

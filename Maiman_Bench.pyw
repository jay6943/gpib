import sys
import cfg
import dev
import dat
import time
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt


class App(Qw.QWidget):
  def __init__(self):
    super().__init__()

    mbl = dev.Maiman_Laser_TEC()
    mbl.write('dur:value 1')
    mbl.write('freq:value 0')
    current = mbl.read('curr:real?')
    voltage = mbl.read('volt:real?')
    temperature = mbl.read('tec:temp:real?')
    mbl.close()

    self.setWindowTitle('MAIMAN Electronics')
    self.setWindowIcon(Qg.QIcon('../doc/ni.png'))
    self.setGeometry(100, 100, 440, 220)

    dat.Qbutton(self, self.SetCurrent, 'Current (mA)', 0, 0, 100)
    dat.Qbutton(self, self.OnCurrent, 'ON', 110, 0, 90)
    dat.Qbutton(self, self.OffCurrent, 'OFF', 210, 0, 90)
    dat.Qbutton(self, self.GetVoltage, 'Voltage (V)', 0, 40, 100)
    dat.Qbutton(self, self.SetTEC, 'TEC (\'C)', 0, 80, 100)
    dat.Qbutton(self, self.OnTEC, 'ON', 110, 80, 90)
    dat.Qbutton(self, self.OffTEC, 'OFF', 210, 80, 90)
    self.current = dat.Qedit(self, current, 310, 0, 90)
    self.voltage = dat.Qedit(self, voltage, 310, 40, 90)
    self.tec = dat.Qedit(self, temperature, 310, 80, 90)

    dat.Qlabel(self, 'Start', 90, 115, 100)
    dat.Qlabel(self, 'Stop', 160, 115, 100)
    dat.Qlabel(self, 'Step', 230, 115, 100)

    dat.Qbutton(self, self.LIcurve, 'L-I Curve (mA)', 0, 150, 100)

    self.star = dat.Qedit(self, '0', 110, 150, 60)
    self.stop = dat.Qedit(self, '50', 180, 150, 60)
    self.step = dat.Qedit(self, '1', 250, 150, 60)

    dat.Qbutton(self, self.OnSave, 'Save', 320, 150, 80)

    self.x = []
    self.y = []

    self.run = 1

  def LIcurve(self):
    mbl = dev.Maiman_Laser_TEC()
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
    mbl = dev.Maiman_Laser_TEC()
    mbl.write(f'curr:value {self.current.text()}')
    mbl.close()

  def OnCurrent(self):
    mbl = dev.Maiman_Laser_TEC()
    mbl.write('dev:start on')
    current = mbl.read('curr:real?')
    self.current.setText(f'{current}')
    mbl.close()

  def OffCurrent(self):
    mbl = dev.Maiman_Laser_TEC()
    mbl.write('dev:start off')
    current = mbl.read('curr:real?')
    self.current.setText(f'{current}')
    mbl.close()

  def SetTEC(self):
    mbl = dev.Maiman_Laser_TEC()
    mbl.write(f'tec:temp:value {self.tec.text()}')
    mbl.close()

  def OnTEC(self):
    mbl = dev.Maiman_Laser_TEC()
    mbl.write('tec:start on')
    temperature = mbl.read('tec:temp:real?')
    self.tec.setText(f'{temperature}')
    mbl.close()

    self.run = 1

  def OffTEC(self):
    mbl = dev.Maiman_Laser_TEC()
    mbl.write('tec:start off')
    temperature = mbl.read('tec:temp:real?')
    self.tec.setText(f'{temperature}')
    mbl.close()

  def GetVoltage(self):
    mbl = dev.Maiman_Laser_TEC()
    voltage = mbl.read('volt:real?')
    self.voltage.setText(f'{voltage}')
    mbl.close()

  def OnSave(self):
    f = Qw.QFileDialog.getSaveFileName(self, '', cfg.get_folder(), '*.txt')

    if f[0]:
      np.savetxt(f[0], np.array([self.x, self.y]).transpose())

if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())

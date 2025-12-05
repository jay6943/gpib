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
    mbl.write('dur:value 1000')
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

    self.start = dat.Qedit(self, '0', 110, 150, 60)
    self.stop = dat.Qedit(self, '50', 180, 150, 60)
    self.step = dat.Qedit(self, '1', 250, 150, 60)

    dat.Qbutton(self, self.OnSave, 'Save', 320, 150, 80)

  def LIcurve(self):
    mbl = dev.Maiman_Laser_TEC()
    opm = dev.Keysight_81630B_photodiode()
    
    start = float(self.start.text())
    stop = float(self.stop.text())
    step = float(self.step.text())
    
    x = np.arange(start, stop + step * 0.1, step)
    y = np.zeros_like(x)

    mbl.write('dev:start on')
    time.sleep(1)

    for i, current in enumerate(x):
      mbl.write(f'curr:value {current:.1f}')
      plt.pause(0.2)
      y[i] = 10 ** (opm.read(1, 1) * 0.1)

      if i > 0:
        plt.cla()
        plt.plot(x, y)
        plt.xlabel('Current (mA)')
        plt.ylabel('Output power (mW)')
        plt.xlim(start, current)
        plt.grid()

    mbl.write(f'curr:value {start:.1f}')
    mbl.write('dev:start off')
    
    plt.show()

    mbl.close()
    opm.close()

  def SetCurrent(self):
    mbl = dev.Maiman_Laser_TEC()
    mbl.write(f'curr:value {self.current.text()}')
    mbl.close()

  def OnCurrent(self):
    mbl = dev.Maiman_Laser_TEC()
    mbl.write('dev:start on')
    voltage = mbl.read('volt:real?')
    self.voltage.setText(f'{voltage}')
    mbl.close()

  def OffCurrent(self):
    mbl = dev.Maiman_Laser_TEC()
    mbl.write('dev:start off')
    voltage = mbl.read('volt:real?')
    self.voltage.setText(f'{voltage}')
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
    fp = Qw.QFileDialog.getSaveFileName(self, '', cfg.path, '*.txt')
    if fp[0]:
      np.savetxt(fp[0], np.array([self.x, self.y]).transpose())

if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())

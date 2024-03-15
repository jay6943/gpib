import sys
import cfg
import dev
import dat
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt


def ON(ch, src, value):
  if src == 'i': value = str(float(value) * 0.001)
  dc = '.OUTPUT_DCAMPS' if src == 'i' else '.OUTPUT_DCVOLTS'

  ksm = dev.ivs()
  ksm.write('reset()')
  ksm.write(ch + '.source.func = ' + ch + dc)
  ksm.write(ch + '.source.level' + src + ' = ' + value)
  ksm.write(ch + '.source.output = ' + ch + '.OUTPUT_ON')
  ksm.close()


def OFF(ch):
  ksm = dev.ivs()
  ksm.write(ch + '.source.output = ' + ch + '.OUTPUT_OFF')
  ksm.close()


def IAoff(): OFF('smua')
def IBoff(): OFF('smub')
def VAoff(): OFF('smua')
def VBoff(): OFF('smub')


class App(Qw.QWidget):
  def __init__(self):
    super().__init__()
    
    self.setWindowTitle('KEITHLEY 2612B')
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setGeometry(100, 100, 540, 290)

    dat.Qlabel(self, 'IA', 0, 0, 100)
    dat.Qlabel(self, 'VA', 0, 40, 100)
    dat.Qlabel(self, 'IB', 270, 0, 100)
    dat.Qlabel(self, 'VB', 270, 40, 100)
    dat.Qlabel(self, 'mA', 210, 0, 100)
    dat.Qlabel(self, 'V', 210, 40, 100)
    dat.Qlabel(self, 'mA', 480, 0, 100)
    dat.Qlabel(self, 'V', 480, 40, 100)

    dat.Qbutton(self, self.IAon, 'ON', 30, 0, 40)
    dat.Qbutton(self, IAoff, 'OFF', 80, 0, 40)
    dat.Qbutton(self, self.VAon, 'ON', 30, 40, 40)
    dat.Qbutton(self, VAoff, 'OFF', 80, 40, 40)
    dat.Qbutton(self, self.IBon, 'ON', 300, 0, 40)
    dat.Qbutton(self, IBoff, 'OFF', 350, 0, 40)
    dat.Qbutton(self, self.VBon, 'ON', 300, 40, 40)
    dat.Qbutton(self, VBoff, 'OFF', 350, 40, 40)

    self.IA = dat.Qedit(self, '0', 130, 0, 70)
    self.VA = dat.Qedit(self, '0', 400, 0, 70)
    self.IB = dat.Qedit(self, '0', 130, 40, 70)
    self.VB = dat.Qedit(self, '0', 400, 40, 70)

    dat.Qlabel(self, 'Start', 160, 90, 100)
    dat.Qlabel(self, 'Stop', 280, 90, 100)
    dat.Qlabel(self, 'Step', 400, 90, 100)

    dat.Qlabel(self, 'I-V', 0, 120, 100)
    dat.Qlabel(self, 'V-I', 0, 160, 100)
    dat.Qlabel(self, 'mA', 480, 120, 100)
    dat.Qlabel(self, 'V', 480, 160, 100)

    dat.Qbutton(self, self.IVA, 'A', 30, 120, 40)
    dat.Qbutton(self, self.IVB, 'B', 80, 120, 40)
    dat.Qbutton(self, self.VIA, 'A', 30, 160, 40)
    dat.Qbutton(self, self.VIB, 'B', 80, 160, 40)

    self.Istart = dat.Qedit(self, '1.0', 130, 120, 100)
    self.Istop = dat.Qedit(self, '100.0', 250, 120, 100)
    self.Istep = dat.Qedit(self, '1.0', 370, 120, 100)
    self.Vstart = dat.Qedit(self, '-2.0', 130, 160, 100)
    self.Vstop = dat.Qedit(self, '3.0', 250, 160, 100)
    self.Vstep = dat.Qedit(self, '0.05', 370, 160, 100)

    self.filename = dat.Qedit(self, 'filename', 0, 220, 250)
    dat.Qbutton(self, self.onFolder, 'Set Folder', 390, 220, 80)

    self.checkplot = dat.Qcheck(self, 'graph', 280, 220, 100)
    self.checkplot.setChecked(False)

    self.x, self.y = [], []

  def IV(self, ch):
    start = float(self.Istart.text()) * 0.001
    stop = float(self.Istop.text()) * 0.001
    step = float(self.Istep.text()) * 0.001
    
    self.x = np.arange(start, stop + step * 0.1, step)

    n = len(self.x)

    xstr = str(start) + ',' + str(stop) + ',' + str(step) + ',' + str(n)
    xstr = '(' + ch + ',' + xstr + ')'

    ksm = dev.ivs()
    ksm.write('reset()')
    ksm.write(ch + '.source.limitv = 10')
    ksm.write('SweepILinMeasureV' + xstr)
    self.y = ksm.Vread(n, ch)
    ksm.close()

    filename = cfg.get_folder() + '/' + self.filename.text() + '-IV'
    self.x = np.round(self.x * 1000, 3)
    self.y = np.round(self.y, 6)
    np.savetxt(filename + '.txt', np.array([self.x, self.y]).transpose())

    if self.checkplot.isChecked():
      plt.plot(self.x, self.y)
      plt.xlabel('Current (A)')
      plt.ylabel('Voltage (mV)')
      plt.xlim(0, self.x[n-1])
      plt.ylim(min(self.y), max(self.y))
      plt.grid()
      plt.savefig(filename + '.png')
      plt.show()
      plt.close()

  def VI(self, ch):
    start = float(self.Vstart.text())
    stop = float(self.Vstop.text())
    step = float(self.Vstep.text())

    self.x = np.arange(start, stop + step * 0.1, step)

    n = len(self.x)

    xstr = str(start) + ',' + str(stop) + ',' + str(step) + ',' + str(n)
    xstr = '(' + ch + ',' + xstr + ')'

    ksm = dev.ivs()
    ksm.write('reset()')
    ksm.write(ch + '.source.limiti = 10e-3')
    ksm.write('SweepVLinMeasureI' + xstr)
    self.y = ksm.Iread(n, ch)
    ksm.close()

    filename = cfg.get_folder() + '/' + self.filename.text() + '-VI'
    self.x = np.round(self.x * 1000, 3)
    self.y = np.round(self.y, 6)
    np.savetxt(filename + '.txt', np.array([self.x, self.y]).transpose())

    if self.checkplot.isChecked():
      plt.plot(self.x, self.y)
      plt.xlabel('Voltage (mV)')
      plt.ylabel('Current (A)')
      plt.xlim(start, stop)
      plt.ylim(min(self.y), max(self.y))
      plt.grid()
      plt.savefig(filename + '.png')
      plt.show()
      plt.close()

  def IAon(self): ON('smua', 'i', self.IA.text())
  def IBon(self): ON('smub', 'i', self.IB.text())
  def VAon(self): ON('smua', 'v', self.VA.text())
  def VBon(self): ON('smub', 'v', self.VB.text())
  def IVA(self): self.IV('smua')
  def IVB(self): self.IV('smub')
  def VIA(self): self.VI('smua')
  def VIB(self): self.VI('smub')

  def onFolder(self):
    folder = Qw.QFileDialog.getExistingDirectory(self, '', cfg.get_folder())

    if folder != '': cfg.set_folder(folder)

if __name__ == '__main__':
  
  app = Qw.QApplication(sys.argv)
  MyWindow = App()
  MyWindow.show()
  sys.exit(app.exec_())

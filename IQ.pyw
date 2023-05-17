import os
import sys
import dev
import dat
import time
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

class ExWindow(Qw.QMainWindow):
  
  def __init__(self):

    super().__init__()
        
    self.setGeometry(500, 500, 260, 390)
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setWindowTitle('IQ')

    dat.Qbutton(self, self.OnData, 'Get', 0, 0, 100)
    dat.Qbutton(self, self.OnSave, 'Save', 120, 0, 100)
    dat.Qbutton(self, self.OnRun, 'Run', 0, 80, 100)
    dat.Qbutton(self, self.OnStop, 'Stop', 120, 80, 100)
    dat.Qbutton(self, self.OnTY, 'TY-plot', 0, 120, 100)
    dat.Qbutton(self, self.OnXY, 'XY-plot', 120, 120, 100)
    
    dat.Qbutton(self, self.OnTime, 'Time', 120, 160, 100)
    dat.Qbutton(self, self.OnAmp1, 'Ch 1 (mV/Div)', 120, 200, 100)
    dat.Qbutton(self, self.OnAmp2, 'Ch 2 (mV/Div)', 120, 240, 100)
    dat.Qbutton(self, self.OnOff1, 'Offset 1 (mV)', 120, 280, 100)
    dat.Qbutton(self, self.OnOff2, 'Offset 2 (mV)', 120, 320, 100)

    self.var = dat.Qedit(self, '0.01', 0, 160, 100)
    self.amp1 = dat.Qedit(self, '', 0, 200, 100)
    self.amp2 = dat.Qedit(self, '', 0, 240, 100)
    self.off1 = dat.Qedit(self, '0', 0, 280, 100)
    self.off2 = dat.Qedit(self, '0', 0, 320, 100)
    self.fit = dat.Qedit(self, '', 80, 40, 100)
    
    dat.Qlabel(self, 'Phase error', 0, 30, 80)
    dat.Qlabel(self, 'deg.', 190, 30, 40)
    
    self.OnCH1 = dat.Qcheck(self, '', 104, 200, 15)
    self.OnCH2 = dat.Qcheck(self, '', 104, 240, 15)

    self.OnCH1.setChecked(True)
    self.OnCH2.setChecked(True)

    self.m = 4096

    dso = dev.dso(False)
    dso.write('AUT:DIS')
    dso.write('TIM:SCAL ' + self.var.text())
    dso.write('CHAN1:COUP DC')
    dso.write('CHAN2:COUP DC')
    dso.write('WAV:POINTS:MODE RAW')
    dso.write('WAV:FORM ASCII')
    dso.write('WAV:POINTS ' + str(self.m))
    self.amp1.setText(str(round(dso.query('CHAN1:SCAL?') * 1e3, 3)))
    self.amp2.setText(str(round(dso.query('CHAN2:SCAL?') * 1e3, 3)))
    self.off1.setText(str(round(dso.query('CHAN1:OFFS?') * 1e3, 3)))
    self.off2.setText(str(round(dso.query('CHAN2:OFFS?') * 1e3, 3)))
    dso.close()

  def OnRun(self):
    dev.dso('RUN')

  def OnStop(self):
    dev.dso('SINGLE')
    
  def OnTY(self):
    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('CHAN1:DISP 1')
    dso.write('CHAN2:DISP 1')
    dso.write('TIM:SCAL ' + self.var.text())
    dso.write('CHAN1:SCAL ' + str(float(self.amp1.text()) * 1e-3))
    dso.write('CHAN2:SCAL ' + str(float(self.amp2.text()) * 1e-3))
    dso.write('SINGLE')

    time.sleep(2)

    ch1 = dso.getwave(1)
    ch2 = dso.getwave(2)

    rf1 = -round((np.max(ch1) + np.min(ch1)) * 0.5)
    rf2 = -round((np.max(ch2) + np.min(ch2)) * 0.5)

    self.off1.setText(str(rf1))
    self.off2.setText(str(rf2))

    dso.write('TIM:SCAL ' + self.var.text())
    dso.write('CHAN1:OFFS ' + str(rf1) + 'E-3')
    dso.write('CHAN2:OFFS ' + str(rf2) + 'E-3')

    dso.write('RUN')
    dso.close()

  def OnXY(self):
    self.OnTY()
    dev.dso('TIM:FORM XY')
    
  def OnTime(self):
    dev.dso('TIM:SCAL ' + self.var.text())
    
  def OnAmp1(self):
    dso = dev.dso(False)
    if self.OnCH1.isChecked():
      dso.write('CHAN1:DISP 1')
      dso.write('TIM:FORM YT')
      dso.write('CHAN1:SCAL ' + str(float(self.amp1.text()) * 1e-3))
      dso.write('TIM:SCAL ' + self.var.text())
      dso.write('TIM:FORM XY')
    else:
      dso.write('CHAN1:DISP 0')
    dso.close()

  def OnAmp2(self):
    dso = dev.dso(False)
    if self.OnCH2.isChecked():
      dso.write('CHAN2:DISP 1')
      dso.write('TIM:FORM YT')
      dso.write('CHAN2:SCAL ' + str(float(self.amp2.text()) * 1e-3))
      dso.write('TIM:SCAL ' + self.var.text())
      dso.write('TIM:FORM XY')
    else:
      dso.write('CHAN2:DISP 0')
    dso.close()

  def OnOff1(self):
    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('CHAN1:OFFS ' + str(float(self.off1.text()) * 1e-3))
    dso.write('TIM:SCAL ' + self.var.text())
    dso.write('TIM:FORM XY')
    dso.close()

  def OnOff2(self):
    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('CHAN2:OFFS ' + str(float(self.off2.text()) * 1e-3))
    dso.write('TIM:SCAL ' + self.var.text())
    dso.write('TIM:FORM XY')
    dso.close()

  def OnData(self):
    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('TIM:SCAL ' + self.var.text())
    dso.write('SINGLE')

    time.sleep(2)

    self.t = np.arange(self.m) * float(self.var.text())
    self.x = dso.getwave(1)
    self.y = dso.getwave(2)

    dso.write('RUN')
    dso.write('TIM:FORM XY')
    dso.close()

    A = np.arange(float(self.m * 5)).reshape(5, self.m)
    B = -self.x * self.x

    A[0] = self.x * self.y * 2
    A[1] = self.y * self.y
    A[2] = self.x * 2
    A[3] = self.y * 2
    A[4] = 1

    k = np.dot(B, np.linalg.pinv(A))
    p = np.arcsin(np.sqrt(1 - k[0] * k[0] / k[1])) * 180 / np.pi
    
    if k[0] > 0: p = 180 - p
    
    self.phase = str(round(p, 1))
    self.fit.setText(self.phase)
    self.OnDraw()

  def OnDraw(self):
    xmin = np.amin(self.x)
    xmax = np.amax(self.x)
    ymin = np.amin(self.y)
    ymax = np.amax(self.y)

    self.x = self.x - (xmax + xmin) * 0.5
    self.y = self.y - (ymax + ymin) * 0.5

    l = np.max(np.abs(np.array([xmax - xmin, ymax - ymin]))) * 0.6

    plt.close()
    plt.figure(dpi=150)
    plt.scatter(self.x, self.y, c='b', s=5)
    plt.axis('square')
    plt.title(self.phase + '$^{\circ}$')
    plt.gca().axes.xaxis.set_visible(False)
    plt.gca().axes.yaxis.set_visible(False)
    plt.plot([0, 0], [-l, l], 'k:', linewidth='1')
    plt.plot([-l, l], [0, 0], 'k:', linewidth='1')
    plt.xlim(-l, l)
    plt.ylim(-l, l)
    plt.show()

  def OnSave(self):
    fp = Qw.QFileDialog.getSaveFileName(self, '', dat.get_folder(), '*.txt')[0]
    folder = os.path.dirname(fp)

    if fp:
      data = np.array([self.t, self.x, self.y])
      np.savetxt(fp, data.transpose(), fmt='%.3f')
      filename = os.path.splitext(fp)
      plt.savefig(filename[0] + '.png')
      dat.set_folder(folder)

if __name__ == '__main__':

  app = Qw.QApplication(sys.argv)
  ex = ExWindow()
  ex.show()
  sys.exit(app.exec_())

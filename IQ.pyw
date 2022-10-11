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
        
    self.setGeometry(100, 500, 260, 390)
    self.setWindowIcon(Qg.QIcon('jk.png'))
    self.setWindowTitle('IQ')

    dat.Qbutton(self, self.OnData, 'Get', 0, 0, 100)
    dat.Qbutton(self, self.OnSave, 'Save', 120, 0, 100)
    dat.Qbutton(self, self.OnRun, 'Run', 0, 80, 100)
    dat.Qbutton(self, self.OnStop, 'Stop', 120, 80, 100)
    dat.Qbutton(self, self.OnTY, 'TY-plot', 0, 120, 100)
    dat.Qbutton(self, self.OnXY, 'XY-plot', 120, 120, 100)
    
    dat.Qbutton(self, self.OnTime, 'Time (ms)', 120, 160, 100)
    dat.Qbutton(self, self.OnAmp1, 'Ch 1 (mV/Div)', 120, 200, 100)
    dat.Qbutton(self, self.OnAmp2, 'Ch 2 (mV/Div)', 120, 240, 100)
    dat.Qbutton(self, self.OnOff1, 'Offset 1 (mV)', 120, 280, 100)
    dat.Qbutton(self, self.OnOff2, 'Offset 2 (mV)', 120, 320, 100)

    self.var = dat.Qedit(self, '', 0, 160, 100)
    self.amp1 = dat.Qedit(self, '', 0, 200, 100)
    self.amp2 = dat.Qedit(self, '', 0, 240, 100)
    self.off1 = dat.Qedit(self, '', 0, 280, 100)
    self.off2 = dat.Qedit(self, '', 0, 320, 100)
    self.fit = dat.Qedit(self, '', 80, 40, 100)
    
    dat.Qlabel(self, 'Phase error', 0, 30)
    dat.Qlabel(self, 'deg.', 190, 30)
    
    self.m = 4096

    dso = dev.dso(False)
    dso.write('CHAN1:COUP DC')
    dso.write('CHAN2:COUP DC')
    dso.write('WAV:POINTS:MODE RAW')
    dso.write('WAV:FORM ASCII')
    dso.write('WAV:POINTS ' + str(self.m))
    self.var.setText(str(round(dso.query('TIM:SCAL?') * 1e3, 3)))
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
    dev.dso('TIM:FORM YT')
      
  def OnXY(self):        
    dev.dso('TIM:FORM XY')
      
  def OnTime(self):
    dev.dso('TIM:SCAL ' + str(float(self.var.text()) * 1e-3))
      
  def OnAmp1(self):
    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('CHAN1:SCAL ' + str(float(self.amp1.text()) * 1e-3))
    dso.write('TIM:FORM XY')
    dso.close()
      
  def OnAmp2(self):
    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('CHAN2:SCAL ' + str(float(self.amp2.text()) * 1e-3))
    dso.write('TIM:FORM XY')
    dso.close()

  def OnOff1(self):
    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('CHAN1:OFFS ' + str(float(self.off1.text()) * 1e-3))
    dso.write('TIM:FORM XY')
    dso.close()

  def OnOff2(self):
    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('CHAN2:OFFS ' + str(float(self.off2.text()) * 1e-3))
    dso.write('TIM:FORM XY')
    dso.close()

  def OnData(self):

    dso = dev.dso(False)
    dso.write('TIM:FORM YT')
    dso.write('TIM:SCAL ' + str(float(self.var.text()) * 1e-3))
    dso.write('SINGLE')

    time.sleep(2)

    self.t = np.arange(self.m) * float(self.var.text()) * 4e-5
    self.x = dso.getwave(1)
    self.y = dso.getwave(2)

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

    dso.write('RUN')
    dso.write('TIM:FORM XY')
    dso.close()

  def OnDraw(self):

    self.x = self.x * 0.001
    self.y = self.y * 0.001

    xtop = np.amax(self.x)
    xbas = np.amin(self.x)
    ytop = np.amax(self.y)
    ybas = np.amin(self.y)

    self.x = self.x - (xtop + xbas) * 0.5
    self.y = self.y - (ytop + ybas) * 0.5

    ticks = np.linspace(-1,1,3) * 0.1

    plt.close()
    plt.figure(dpi=150)
    plt.scatter(self.x, self.y, c='b', s=5)
    plt.axis('square')
    plt.title(self.phase + '$^{\circ}$')
    plt.xlabel('I (V)')
    plt.ylabel('Q (V)')
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.xlim(ticks[0], ticks[-1])
    plt.ylim(ticks[0], ticks[-1])
    plt.grid(True)
    plt.show()

  def OnSave(self):

    fp = Qw.QFileDialog.getSaveFileName(self, '', dat.getfolder(), '*.txt')[0]

    if fp:
      data = [self.t, self.x, self.y]
      np.savetxt(fp, np.array(data).transpose(), fmt='%.3f')
      plt.savefig(fp[:len(fp)-4] + '.png')

      folder = os.path.dirname(fp)
      if folder != dat.getfolder(): dat.setfolder(folder)

if __name__ == '__main__':

  app = Qw.QApplication(sys.argv)
  ex = ExWindow()
  ex.show()
  sys.exit(app.exec_())

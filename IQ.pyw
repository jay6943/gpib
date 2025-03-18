import os
import sys
import cfg
import dev
import dat
import time
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt


class IQ_measurement(Qw.QMainWindow):
  
  def __init__(self):
    super().__init__()

    self.y = None
    self.x = None
    self.t = None
    self.phase = None
    self.address = 'TCPIP0::192.168.0.25::inst0::INSTR'

    self.setGeometry(500, 500, 260, 490)
    self.setWindowIcon(Qg.QIcon('../doc/jk.png'))
    self.setWindowTitle('IQ')

    dat.Qbutton(self, self.OnData, 'Get', 0, 0, 100)
    dat.Qbutton(self, self.OnSave, 'Save', 120, 0, 100)
    dat.Qbutton(self, self.OnRun, 'Run', 0, 80, 100)
    dat.Qbutton(self, self.OnStop, 'Stop', 120, 80, 100)
    dat.Qbutton(self, self.OnTY, 'TY-plot', 0, 120, 100)
    dat.Qbutton(self, self.OnXY, 'XY-plot', 120, 120, 100)

    self.var = dat.Qedit(self, '', 0, 160, 100)
    self.amp1 = dat.Qedit(self, '', 0, 200, 100)
    self.amp2 = dat.Qedit(self, '', 0, 240, 100)
    self.off1 = dat.Qedit(self, '', 0, 280, 100)
    self.off2 = dat.Qedit(self, '', 0, 320, 100)
    self.att = dat.Qedit(self, '', 0, 380, 100)
    self.mdl = dat.Qedit(self, '', 0, 420, 100)
    self.fit = dat.Qedit(self, '', 80, 40, 100)

    dat.Qbutton(self, self.OnTime, 'Time (msec)', 120, 160, 100)
    dat.Qbutton(self, self.OnAmp, 'Ch 1 && 2 (mV/Div)', 120, 200, 100)
    dat.Qbutton(self, self.OnAmp2, 'Ch 2 (mV/Div)', 120, 240, 100)
    dat.Qbutton(self, self.OnOff1, 'Offset 1 (mV)', 120, 280, 100)
    dat.Qbutton(self, self.OnOff2, 'Offset 2 (mV)', 120, 320, 100)
    dat.Qbutton(self, self.OnAtt, 'Att. (dB)', 120, 380, 100)
    dat.Qbutton(self, self.OnMdl, '(GHz)', 120, 420, 60)
    dat.Qbutton(self, self.OnMdl_Off, 'OFF', 190, 420, 30)

    dat.Qlabel(self, 'Phase error', 0, 30, 80)
    dat.Qlabel(self, 'deg.', 190, 30, 40)
    
    self.OnCH1 = dat.Qcheck(self, '', 104, 200, 15)
    self.OnCH2 = dat.Qcheck(self, '', 104, 240, 15)

    self.OnCH1.setChecked(True)
    self.OnCH2.setChecked(True)

    self.m = 4096

    dso = dev.Agilent_DSO1014A_oscilloscope(False)
    dso.write('AUT:DIS')
    dso.write('CHAN1:COUP DC')
    dso.write('CHAN2:COUP DC')
    dso.write('WAV:POINTS:MODE RAW')
    dso.write('WAV:FORM ASCII')
    dso.write('WAV:POINTS ' + str(self.m))
    self.var.setText(str(dso.query('TIM:SCAL?') * 1e3))
    self.amp1.setText(str(round(dso.query('CHAN1:SCAL?') * 1e3, 3)))
    self.amp2.setText(str(round(dso.query('CHAN2:SCAL?') * 1e3, 3)))
    self.off1.setText(str(round(dso.query('CHAN1:OFFS?') * 1e3, 3)))
    self.off2.setText(str(round(dso.query('CHAN2:OFFS?') * 1e3, 3)))
    dso.close()

    att = dev.Keysight_81630B_attenuator(self.address)
    self.att.setText(str(float(att.query(':INP2:ATT?'))))
    att.write(':OUTP2:STAT ON')
    att.close()

    tld = dev.Keysight_N7711A_tunalble_laser()
    self.mdl.setText(str(float(tld.query('MODU:INT:SBSC?'))*1e-9))
    tld.close()

  def OnRun(self):
    dev.Agilent_DSO1014A_oscilloscope('RUN')
    print(self.m)

  def OnStop(self):
    dev.Agilent_DSO1014A_oscilloscope('SINGLE')
    print(self.m)

  def OnTY(self):
    dso = dev.Agilent_DSO1014A_oscilloscope(False)
    dso.write('TIM:FORM YT')
    dso.write('CHAN1:DISP 1')
    dso.write('CHAN2:DISP 1')
    dso.write(f'CHAN1:SCAL {float(self.amp1.text()) * 1e-3}')
    dso.write(f'CHAN2:SCAL {float(self.amp2.text()) * 1e-3}')
    dso.write('SINGLE')

    time.sleep(2)

    ch1 = dso.getwave(1)
    ch2 = dso.getwave(2)

    rf1 = -round((np.max(ch1) + np.min(ch1)) * 0.5)
    rf2 = -round((np.max(ch2) + np.min(ch2)) * 0.5)

    self.off1.setText(str(rf1))
    self.off2.setText(str(rf2))

    dso.write(f'CHAN1:OFFS {rf1}E-3')
    dso.write(f'CHAN2:OFFS {rf2}E-3')

    dso.write('RUN')
    dso.close()

  def OnXY(self):
    self.OnTY()
    dev.Agilent_DSO1014A_oscilloscope('TIM:FORM XY')
    
  def OnTime(self):
    timescale = str(round(float(self.var.text()) * 1e-3, 6))
    dev.Agilent_DSO1014A_oscilloscope(f'TIM:SCAL {timescale}')

  def OnAmp1(self):
    dso = dev.Agilent_DSO1014A_oscilloscope(False)
    if self.OnCH1.isChecked():
      dso.write('CHAN1:DISP 1')
      dso.write(f'CHAN1:SCAL {float(self.amp1.text()) * 1e-3}')
    else:
      dso.write('CHAN1:DISP 0')
    dso.close()

  def OnAmp2(self):
    dso = dev.Agilent_DSO1014A_oscilloscope(False)
    if self.OnCH2.isChecked():
      dso.write('CHAN2:DISP 1')
      dso.write(f'CHAN2:SCAL {float(self.amp2.text()) * 1e-3}')
    else:
      dso.write('CHAN2:DISP 0')
    dso.close()

  def OnAmp(self):
    self.OnAmp1()
    dso = dev.Agilent_DSO1014A_oscilloscope(False)
    self.amp2.setText(str(round(dso.query('CHAN1:SCAL?') * 1e3, 3)))
    dso.close()
    self.OnAmp2()
    self.OnXY()

  def OnOff1(self):
    ostr = str(float(self.off1.text()) * 1e-3)
    dev.Agilent_DSO1014A_oscilloscope(f'CHAN1:OFFS {ostr}')

  def OnOff2(self):
    ostr = str(float(self.off2.text()) * 1e-3)
    dev.Agilent_DSO1014A_oscilloscope(f'CHAN2:OFFS {ostr}')

  def OnAtt(self):
    att = dev.Keysight_81630B_attenuator(self.address)
    att.write(f':INP2:ATT {self.att.text()}dB')
    att.close()

  def OnMdl(self):
    tld = dev.Keysight_N7711A_tunalble_laser()
    tld.write(f'MODU:INT:SBSC {self.mdl.text()}GHz')
    tld.write('MODU:INT ON')
    tld.close()

  def OnMdl_Off(self):
    tld = dev.Keysight_N7711A_tunalble_laser()
    tld.write(f'MODU:INT:SBSC {self.mdl.text()}GHz')
    tld.write('MODU:INT OFF')
    tld.close()

  def OnData(self):
    dso = dev.Agilent_DSO1014A_oscilloscope(False)
    dso.write('TIM:FORM YT')
    dso.write('SINGLE')

    time.sleep(3)

    self.t = np.arange(self.m) * float(self.var.text())
    self.x = dso.getwave(1)
    self.y = dso.getwave(2)

    self.x /= np.max(np.abs(self.x))
    self.y /= np.max(np.abs(self.y))

    dso.write('RUN')
    dso.write('TIM:FORM XY')
    timescale = round(float(self.var.text()) * 1e-3, 6)
    dso.write('TIM:SCAL ' + str(timescale))
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

    lim = np.max(np.abs(np.array([xmax - xmin, ymax - ymin]))) * 0.6

    plt.close()
    plt.figure(dpi=150)
    plt.scatter(self.x, self.y, c='b', s=5)
    plt.axis('square')
    plt.title(f'{self.phase}{cfg.circ}')
    plt.gca().axes.xaxis.set_visible(False)
    plt.gca().axes.yaxis.set_visible(False)
    plt.plot([0, 0], [-lim, lim], 'k:', linewidth='1')
    plt.plot([-lim, lim], [0, 0], 'k:', linewidth='1')
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    plt.show()

  def OnSave(self):
    fp = Qw.QFileDialog.getSaveFileName(self, '', cfg.get_folder(), '*.txt')[0]
    folder = os.path.dirname(fp)

    if fp:
      data = np.array([self.t, self.x, self.y])
      np.savetxt(fp, data.transpose(), fmt='%.3f')
      filename = os.path.splitext(fp)
      plt.savefig(f'{filename[0]}.png')
      cfg.set_folder(folder)


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = IQ_measurement()
  window.show()
  sys.exit(app.exec_())

  # tld = dev.Keysight_N7711A_tunalble_laser()
  # print(tld.query('MODU:INT:SBSC?'))
  # tld.write('MODU:INT OFF')
  # tld.write('MODU:INT OFF')
  # tld.close()

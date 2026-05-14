import os
import sys
import cfg
import dat
import Yokogawa
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt


class Optical_Spectrum_Analizer(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    self.x = None
    self.y = None

    self.setWindowTitle('Yokogawa AQ6370D')
    self.setWindowIcon(Qg.QIcon('../doc/jk.png'))
    self.setGeometry(500, 500, 290, 550)

    osa = Yokogawa.AQ6370D(False)
    center = float(osa.query(':SENS:WAV:CENT?')) * 1e9
    span = float(osa.query(':SENS:WAV:SPAN?')) * 1e9
    res = float(osa.query(':SENS:BAND:RES?')) * 1e9
    rlev = float(osa.query(':DISP:TRAC:Y1:RLEV?'))
    pdiv = float(osa.query(':DISP:TRAC:Y1:PDIV?'))
    osa.close()

    dat.Qlabel(self, 'Points', 10, 35, 40)
    self.m = dat.Qedit(self, '1001', 55, 45, 90)
    self.center = dat.Qedit(self, str(center), 0, 100, 120)
    self.span = dat.Qedit(self, str(span), 0, 140, 120)
    self.bandwidth = dat.Qedit(self, str(res), 0, 180, 120)
    self.sensitivity = dat.Qedit(self, '10', 0, 220, 120)
    self.reference = dat.Qedit(self, str(rlev), 0, 260, 120)
    self.division = dat.Qedit(self, str(pdiv), 0, 300, 120)

    dat.Qbutton(self, self.OnCenter, 'Center (nm)', 130, 100, 120)
    dat.Qbutton(self, self.OnSpan, 'Span (nm)', 130, 140, 120)
    dat.Qbutton(self, self.OnBandwidth, 'Bandwidth (nm)', 130, 180, 120)
    dat.Qbutton(self, self.OnSensitivity, 'Sensitivity (dBm)', 130, 220, 120)
    dat.Qbutton(self, self.OnReference, 'Reference (dBm)', 130, 260, 120)
    dat.Qbutton(self, self.OnDivision, 'Division (dB)', 130, 300, 120)

    dat.Qbutton(self, self.OnGet, 'Get', 0, 0, 120)
    dat.Qbutton(self, self.OnSave, 'Save', 130, 0, 120)
    dat.Qbutton(self, Yokogawa.OnContinuous, 'Continuous', 0, 340, 120)
    dat.Qbutton(self, Yokogawa.OnSingle, 'Stop', 130, 340, 120)

    dat.Qbutton(self, Yokogawa.OnMax, 'Max', 0, 380, 120)
    dat.Qbutton(self, Yokogawa.OnMin, 'Min', 130, 380, 120)
    dat.Qbutton(self, Yokogawa.OnMarkCenter, 'Mark to Center', 0, 420, 120)
    dat.Qbutton(self, self.OnLevel, 'Ref. to Peak', 130, 420, 120)

    dat.Qlabel(self, 'Y min', 0, 445, 120)
    dat.Qlabel(self, 'Y max', 130, 445, 120)
    self.ymin = dat.Qedit(self, '-80', 0, 480, 120)
    self.ymax = dat.Qedit(self, '0', 130, 480, 120)

    self.saving = dat.Qcheck(self, 'Save figure', 160, 45, 100)

    self.setSwitch = 1
    self.saving.setChecked(True)

    Yokogawa.OnPoints(self.m.text())

  def OnCenter(self):
    Yokogawa.OnCenter(self.center.text())

  def OnSpan(self):
    Yokogawa.OnSpan(self.span.text())

  def OnBandwidth(self):
    Yokogawa.OnBandwidth(self.bandwidth.text())

  def OnSensitivity(self):
    Yokogawa.OnRpos(self.sensitivity.text())

  def OnReference(self):
    Yokogawa.OnRlev(self.reference.text())

  def OnDivision(self):
    Yokogawa.OnPdiv(self.division.text())

  def OnLevel(self):
    osa = Yokogawa.AQ6370D(False)
    osa.write(':CALC:MARK:MAX')
    y = float(osa.query(':CALC:MARK:Y?'))
    osa.close()

    self.reference.setText(str(round(y, 0)))
    self.OnReference()

  def OnGet(self):
    osa = Yokogawa.AQ6370D(False)
    osa.write(f':SENS:SWE:POIN {self.m.text()}')
    osa.write(':INIT:SMOD SING')
    osa.write(':INIT:IMM')
    self.x = osa.read(':TRAC:DATA:X? TRA')
    self.y = osa.read(':TRAC:DATA:Y? TRA')
    osa.write(':INIT:SMOD REP')
    osa.write(':INIT:IMM')
    osa.close()

    self.x = self.x.replace('\n', '').split(',')
    self.y = self.y.replace('\n', '').split(',')
    self.x = np.array(self.x).astype(float) * 1e9
    self.y = np.array(self.y).astype(float)
    self.x = np.round(self.x, 9)
    self.y = np.round(self.y, 9)

    xc = float(self.center.text())
    dx = float(self.span.text())

    plt.close()
    plt.figure(dpi=150)
    plt.plot(self.x, self.y)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Output (dBm)')
    plt.xlim(round(xc - dx * 0.5, 3), round(xc + dx * 0.5, 3))
    plt.ylim(float(self.ymin.text()), float(self.ymax.text()))
    plt.grid()
    plt.show()

  def OnSave(self):
    fp = Qw.QFileDialog.getSaveFileName(self, '', cfg.path, '*.dat')
    if fp[0]:
      np.savetxt(fp[0], np.array([self.x, self.y]).transpose())
      if self.saving.isChecked():
        plt.savefig(f'{os.path.splitext(fp[0])[0]}.png')


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Optical_Spectrum_Analizer()
  window.show()
  sys.exit(app.exec_())

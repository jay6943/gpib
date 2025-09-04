import os
import sys
import cfg
import dat
import dev
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt


def OnMax():
  dev.Yokogawa_AQ6370D(':CALC:MARK:MAX')


def OnMin():
  dev.Yokogawa_AQ6370D(':CALC:MARK:MIN')


def OnMarkCenter():
  dev.Yokogawa_AQ6370D(':CALC:MARK:SCEN')


def OnContinuous():
  osa = dev.Yokogawa_AQ6370D(False)
  osa.write(':INIT:SMOD REP')
  osa.write(':INIT:IMM')
  osa.close()


def OnSingle():
  osa = dev.Yokogawa_AQ6370D(False)
  osa.write(':INIT:SMOD SING')
  osa.write(':INIT:IMM')
  osa.close()


class Yokogawa_AQ6370D(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    self.x = None
    self.y = None

    self.setWindowTitle('Yokogawa AQ6370D')
    self.setWindowIcon(Qg.QIcon('../doc/jk.png'))
    self.setGeometry(500, 500, 290, 490)

    osa = dev.Yokogawa_AQ6370D(False)
    center = float(osa.query(':SENS:WAV:CENT?')) * 1e9
    span = float(osa.query(':SENS:WAV:SPAN?')) * 1e9
    res = float(osa.query(':SENS:BAND:RES?')) * 1e9
    rlev = float(osa.query(':DISP:TRAC:Y1:RLEV?'))
    pdiv = float(osa.query(':DISP:TRAC:Y1:PDIV?'))
    osa.close()

    dat.Qlabel(self, 'Number of Points', 20, 50, 110)
    self.m = dat.Qedit(self, '1001', 130, 60, 120)
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
    dat.Qbutton(self, OnContinuous, 'Continuous', 0, 340, 120)
    dat.Qbutton(self, OnSingle, 'Stop', 130, 340, 120)

    dat.Qbutton(self, OnMax, 'Max', 0, 380, 120)
    dat.Qbutton(self, OnMin, 'Min', 130, 380, 120)
    dat.Qbutton(self, OnMarkCenter, 'Mark to Center', 0, 420, 120)
    dat.Qbutton(self, self.OnLevel, 'Ref. to Peak', 130, 420, 120)

    self.saving = dat.Qcheck(self, 'Save w/o show', 10, 30, 120)
    self.figure = dat.Qcheck(self, 'Save figure', 150, 30, 120)

    self.setSwitch = 1
    self.figure.setChecked(True)

    dev.Yokogawa_AQ6370D(f':SENS:SWE:POIN {self.m.text()}')

  def OnCenter(self):
    osa = dev.Yokogawa_AQ6370D(False)
    osa.write(f':SENS:WAV:CENT {self.center.text()}NM')
    osa.close()

  def OnSpan(self):
    osa = dev.Yokogawa_AQ6370D(False)
    osa.write(f':SENS:WAV:SPAN {self.span.text()}NM')
    osa.close()

  def OnBandwidth(self):
    osa = dev.Yokogawa_AQ6370D(False)
    osa.write(f':SENS:BAND:RES {self.bandwidth.text()}NM')
    osa.close()

  def OnSensitivity(self):
    osa = dev.Yokogawa_AQ6370D(False)
    osa.write(f':DISP:TRAC:Y1:RPOS {self.sensitivity.text()}DIV')
    osa.close()

  def OnReference(self):
    osa = dev.Yokogawa_AQ6370D(False)
    osa.write(f':DISP:TRAC:Y1:RLEV {self.reference.text()}DBM')
    osa.close()

  def OnDivision(self):
    osa = dev.Yokogawa_AQ6370D(False)
    osa.write(f':DISP:TRAC:Y1:PDIV {self.division.text()}DB')
    osa.close()

  def OnLevel(self):
    osa = dev.Yokogawa_AQ6370D(False)
    osa.write(':CALC:MARK:MAX')
    y = float(osa.query(':CALC:MARK:Y?'))
    osa.close()

    self.reference.setText(str(round(y, 0)))
    self.OnReference()

  def OnGet(self):
    osa = dev.Yokogawa_AQ6370D(False)
    osa.write(f':SENS:SWE:POIN {self.m.text()}')
    osa.write(':INIT:SMOD SING')
    osa.write(':INIT:IMM')
    self.x = osa.query(':TRAC:DATA:X? TRA')
    self.y = osa.query(':TRAC:DATA:Y? TRA')
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
    yr = float(self.reference.text())
    dy = float(self.division.text())

    plt.close()
    plt.figure(dpi=150)
    plt.plot(self.x, self.y)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Output (dBm)')
    plt.xlim(xc - dx * 0.5, xc + dx * 0.5)
    plt.ylim(yr - dy * 10, yr)
    plt.grid()
    plt.show()

    if self.saving.isChecked(): self.OnSave()

  def OnSave(self):
    f = Qw.QFileDialog.getSaveFileName(self, '', cfg.get_folder(), '*.dat')
    folder = os.path.dirname(f[0])

    if f[0]:
      data = np.array([self.x, self.y])
      np.savetxt(f[0], data.transpose())
      cfg.set_folder(folder)
      if self.figure.isChecked():
        fp = os.path.splitext(f[0])
        print(fp[0])
        plt.savefig(f'{fp[0]}.png')


if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = Yokogawa_AQ6370D()
  window.show()
  sys.exit(app.exec_())

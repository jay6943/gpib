import os
import cfg
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtCore as Qc
import PyQt5.QtWidgets as Qw

def QMessage(self, text):
  Qw.QMessageBox.about(self, 'Receiver', text)

def Qlabel(self, text, x, y, size):
  label = Qw.QLabel(self)
  label.resize(size, 30)
  label.move(x + 20, y + 30)
  label.setText(text)
  label.setFont(Qg.QFont('Calibri'))

def Qbutton(self, event, text, x, y, size):
  button = Qw.QPushButton(text, self)
  button.clicked.connect(event)
  button.resize(size, 30)
  button.move(x + 20, y + 20)
  button.setFont(Qg.QFont('Calibri'))

def Qedit(self, text, x, y, size):
  edit = Qw.QLineEdit(self)
  edit.resize(size, 30)
  edit.move(x + 20, y + 20)
  edit.setText(text)
  edit.setAlignment(Qc.Qt.AlignCenter)
  edit.setFont(Qg.QFont('Consolas'))

  return edit

def Qcheck(self, text, x, y, size):
  check = Qw.QCheckBox(text, self)
  check.resize(size, 30)
  check.move(x + 20, y + 20)
  check.setFont(Qg.QFont('Calibri'))

  return check

def Qcombo(self, x, y, size):
  combo = Qw.QComboBox(self)
  combo.resize(size, 30)
  combo.move(x + 20, y + 20)
  combo.setFont(Qg.QFont('Calibri'))

  return combo

def get_folder():
  fp = open(cfg.temps)
  data = fp.read()
  data = data.replace('\n','')
  fp.close()

  return data

def set_folder(folder):
  fp = open(cfg.temps, 'w')
  fp.write(folder)
  fp.close()

def arange(xmin, xmax, step):
  return np.arange(xmin, xmax + step * 0.5, step)

if __name__ == '__main__':
  print(os.listdir(get_folder()))
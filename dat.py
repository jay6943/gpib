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
  label.setAlignment(Qc.Qt.AlignCenter)
  label.setFont(Qg.QFont('Calibri'))


def Qbutton(self, event, text, x, y, size):
  button = Qw.QPushButton(text, self)
  button.clicked.connect(event)
  button.resize(size, 30)
  button.move(x + 20, y + 20)
  button.setFont(Qg.QFont('Calibri'))


def QbuttonBig(self, event, text, x, y, size):
  button = Qw.QPushButton(text, self)
  button.clicked.connect(event)
  button.resize(size, 50)
  button.move(x + 20, y + 20)
  button.setFont(Qg.QFont('', 14))


def Qedit(self, text, x, y, size):
  edit = Qw.QLineEdit(self)
  edit.resize(size, 30)
  edit.move(x + 20, y + 20)
  edit.setText(text)
  edit.setAlignment(Qc.Qt.AlignCenter)
  edit.setFont(Qg.QFont('Consolas'))

  return edit


def Qeditbig(self, text, x, y, size):
  edit = Qw.QLineEdit(self)
  edit.resize(size, 50)
  edit.move(x + 20, y + 20)
  edit.setText(text)
  edit.setAlignment(Qc.Qt.AlignCenter)
  edit.setFont(Qg.QFont('Consolas', 24))

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

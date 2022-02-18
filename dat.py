import sys
import os.path
import numpy as np
import PyQt5.QtGui as Qg
import PyQt5.QtCore as Qc
import PyQt5.QtWidgets as Qw
import matplotlib.pyplot as plt

config = 'dat.txt'

def Qlabel(self, text, x, y):

    label = Qw.QLabel(self)
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
    edit.setAlignment(Qc.Qt.AlignLeft)
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

def getfolder():

    fp = open(config, 'r')
    data = fp.read().split('\n')
    fp.close()

    return data[0]

def setfolder(foldername):

    fp = open(config, 'r')
    data = fp.read().split('\n')
    fp.close()

    data[0] = foldername + '/'

    fp = open(config, 'w')
    for i in range(len(data)-1): fp.write(data[i] + '\n')
    fp.close()

def titles():

    fp = open(config, 'r')
    data = fp.read().split('\n')
    fp.close()

    i = data.index('Y')

    return data[2:i], data[i+1:len(data)-1]

def title(i):

    fp = open(config, 'r')
    data = fp.read().split('\n')
    fp.close()

    return data[i]

def getdata(filename):

    fp = open(filename, 'r')
    data = fp.read().split('\n')
    data = data[:len(data)-1]
    fp.close()

    x, y = [], []

    for i in range(len(data)):
        var = data[i].split('\t')
        x.append(float(var[0]))
        y.append(float(var[1]))

    return x, y

def save(filename, x, y):

    fp = open(filename, 'w')
    
    for i in range(len(x)):
        fp.write(str(x[i]) + '\t')
        fp.write(str(y[i]) + '\n')
    
    fp.close()

def aranges(start, stop, step):

    m = int(round((stop - start) / step, 1)) + 1

    x = [start + step * i for i in range(m)]
    y = [0 for i in range(m)]

    return x, y

def plot(filename, x, y, xtitle, ytitle, xmin, xmax, ymin, ymax, style, on):

    plt.plot(x, y, style)
    plt.xlabel(title(xtitle))
    plt.ylabel(title(ytitle))
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.grid()
    plt.savefig(filename)
    if on: plt.show()
    plt.close()

def tcpn():

    legend = []

    folder = getfolder()

    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 3):
                filename = str(i) + str(j) + str(k) + '-I'
                isfile = os.path.isfile(folder + filename + '.txt')
                if isfile:
                    x, y = getdata(folder + filename + '.txt')
                    plt.plot(x, y)
                    legend.append(filename)

    plt.legend(legend)
    plt.xlabel('Current (mA)')
    plt.ylabel('Voltage (V)')
    plt.xlim(0, 10)
    plt.ylim(1.1, 1.6)
    plt.grid()
    plt.savefig(folder + '/IV.png')
    plt.close()

if __name__ == "__main__": tcpn()
    
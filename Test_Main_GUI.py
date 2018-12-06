import numpy as np
import matplotlib.pyplot as plt

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Plot_Window import plot_window, MyMplCanvas
from Test_ui import Ui_Dialog
from Test_Class import Test

class main_window(QDialog):
    def __init__(self):
        super(main_window,self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.assign_widgets()
        self.test = None
        self.show()
        self.plot = None

    def assign_widgets(self):
        self.ui.pushButton_getFile.clicked.connect(self.getData)
        self.ui.pushButton_RawDataPlot.clicked.connect(self.plotData)

    # Ask the user to select a file to process and process it
    def getData(self):
        filename = QFileDialog.getOpenFileName()[0]
        if len(filename) == 0:
            no_file()
            return
        self.test = Test(filename)
        self.test.readData()
        self.test.processStepData()
    # Plot stuff, mostly for testing purposes
    def plotData(self):
        a = 20000
        b = a + 1024
        self.plot = plot_window(xdata=self.test.tempPts,ydata=self.test.storagePts,plotType=0)
        self.plot.show()
        sc2 = MyMplCanvas(xdata=self.test.data.stepTime[a:b],ydata=self.test.data.strain[a:b],plotType=0)
        sc3 = MyMplCanvas(xdata=self.test.stepResult[1].fspace,ydata=self.test.stepResult[1].sigAmp)
        sc3ntb = NavigationToolbar(sc3,self.plot.main_widget)
        self.plot.l.addWidget(sc2)
        self.plot.l.addWidget(sc3)
        self.plot.l.addWidget(sc3ntb)
        self.plot.show()

def no_file():
    msg = QMessageBox()
    msg.setText('There was no file selected')
    msg.setWindowTitle("No File")
    retval = msg.exec_()
    return None

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())
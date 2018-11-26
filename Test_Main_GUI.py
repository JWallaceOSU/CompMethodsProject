import numpy as np
import matplotlib.pyplot as plt

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

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

    def assign_widgets(self):
        self.ui.pushButton_getFile.clicked.connect(self.getData)
    def getData(self):
        filename = QFileDialog.getOpenFileName()[0]
        if len(filename) == 0:
            no_file()
            return
        self.test = Test(filename)
        self.test.readData()
        self.test.sortData()
        self.test.stepProcess()
        print(self.test.stepIndices[2])
        print(self.test.realTime[self.test.stepIndices[2]])
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
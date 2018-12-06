import sys
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100, title='title',xdata=np.zeros(1),ydata=np.zeros(1),
                 ylabel = "",xlabel="", plotType=0):
        self.title = title
        self.xdata = xdata
        self.ydata = ydata
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.plotType = plotType
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.suptitle(title)

        # We want the axes cleared every time plot() is called
        self.axes.clear()

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        self.axes.clear()
        if self.plotType == 3:
            self.axes.loglog(self.xdata,self.ydata)
        elif self.plotType == 2:
            self.axes.semilogy(self.xdata,self.ydata)
        elif self.plotType == 1:
            self.axes.semilogx(self.xdata,self.ydata)
        else:
            self.axes.plot(self.xdata,self.ydata)
        self.axes.set_ylabel(self.ylabel)
        self.axes.set_xlabel(self.xlabel)
        self.axes.grid(True)
class plot_window(QMainWindow):
    def __init__(self,width=5, height=4, dpi=100, title='title',xdata=np.zeros(1),ydata=np.zeros(1),ylabel="",xlabel="",plotType=0):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("plot")
        self.width = width
        self.height = height
        self.dpi = dpi
        self.xdata = xdata
        self.ydata = ydata
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.title = title
        self.plotType = plotType
        self.main_widget = QWidget(self)
        self.l = QVBoxLayout(self.main_widget)
        sc = MyMplCanvas(self.main_widget,width=self.width,height=self.height,dpi=self.dpi,title=self.title,
                         xdata=self.xdata,ydata=self.ydata,ylabel=self.ylabel,xlabel=self.xlabel,plotType=self.plotType)
        scntb = NavigationToolbar(sc,self.main_widget)
        self.l.addWidget(sc)
        self.l.addWidget(scntb)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 10:28:06 2020

@author: eja26438
"""

import numpy as np
import h5py
from nexus_iterator import KeyFollower
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sys









class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        
        with h5py.File("/home/eja26438/Documents/First_Year_Projects/Unique_Keys/Iterator/tests/hdf5_plotter_tests/complete_1.h5", "r") as f:
            dataset_play = f['keys/complete'][...].sum(axis = 2)
            dataset_play = dataset_play.reshape((dataset_play.shape[0], dataset_play.shape[1]))
        
        sc.axes.imshow(dataset_play)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.show()
        
    def update_plot(self):
        with h5py.File("/home/eja26438/Documents/First_Year_Projects/Unique_Keys/Iterator/tests/hdf5_plotter_tests/complete_1.h5", "r") as f:
            f.refresh()
            dataset_play = f['keys/complete'][...].sum(axis = 2)
            dataset_play = dataset_play.reshape((dataset_play.shape[0], dataset_play.shape[1]))
        
        


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
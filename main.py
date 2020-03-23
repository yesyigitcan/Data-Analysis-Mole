import pandas as pd
import numpy as np
import sys

import matplotlib.pyplot as plt
import seaborn as sns

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMessageBox, QListWidget, QApplication, QLabel, QMainWindow, QPushButton, QListView, QFileDialog, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QTimeLine, QPointF, QPropertyAnimation

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.win = uic.loadUi('main.ui', self)
        self.win.setFixedSize(774, 455)
        self.splitLimit = 100
        self.isSplit = 0

        self.win.loadDatasetButton.clicked.connect(self.loadDataset)
        self.win.plotDistributionButton.clicked.connect(self.plotDistribution)
        self.win.plotBoxButton.clicked.connect(self.plotBox)
        self.win.plotScatterButton.clicked.connect(self.plotScatter)
        self.win.plotHeatMapButton.clicked.connect(self.plotHeatMap)
        self.win.splitDataButton.clicked.connect(self.splitData)
        self.win.clearSplittedSetsButton.clicked.connect(self.clearSplittedSets)
        self.win.checkSplittedSetsButton.clicked.connect(self.checkSplittedSets)

        self.splittedDataset = {}

        self.fpath = None
        self.dataset = None
        self.currentFeature = None
        self.currentFeatureData = None
        self.currentFeatureType = None # 1 Numeric 0 Some Numeric -1 Not Numeric
        self.secondFeature = None

        self.win.loadDatasetButton.setFocus()
        self.win.featureListWidget.currentItemChanged.connect(self.changeCurrentFeature)

    def showWarningDialog(self, text):
        QWarningBox = QMessageBox()
        QWarningBox.setIcon(QMessageBox.Warning)
        QWarningBox.setText(text)
        QWarningBox.setWindowTitle("Mole Says")
        returnValue = QWarningBox.exec()

    # Use all clear methods to reset all information sections
    def clearAllInformation(self):
        self.clearFeatureList()

    # Load new dataset
    def loadDataset(self):
        try:
            self.fpath = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.csv)")[0]
        except Exception as e:
            print(e)
            return
        if not self.fpath:
            return

        self.dataset = pd.read_csv(self.fpath)
        self.clearAllInformation()
        self.splittedDataset.clear()
        self.loadAllInformation()



    # Load all information sections after new data set is loaded
    def loadAllInformation(self):
        self.loadFeatureList()

    def loadFeatureList(self):
        if self.dataset is not None:
            for feature in self.dataset.columns:
                self.win.featureListWidget.addItem(feature)
    def clearFeatureList(self):
        self.win.featureListWidget.clear()

    def changeCurrentFeature(self):
        if self.win.featureListWidget.currentItem() is not None:
            self.currentFeature = self.win.featureListWidget.currentItem().text()
            self.currentFeatureData = self.dataset[self.currentFeature]
            self.changeAllInformation()


    def changeAllInformation(self):
        self.changeSampleData()
        ###################
        self.changeType()
        ###################
        self.changeRowCount()
        self.changeUniqueRowCount()
        ###################
        self.changeMax()
        self.changeMin()
        ###################
        self.changeMean()
        self.changeMedian()
        self.changeStd()
        ###################
        self.changeLowerQuartile()
        self.changeUpperQuartile()

    def changeSampleData(self):
        if self.currentFeatureData[0] is not None:
            self.win.sampleDataLabel.setText("Sample Data: " + str(self.currentFeatureData[0]))

    def changeType(self):
        try:
            if self.currentFeatureData.str.isnumeric().all():
                self.win.typeLabel.setText("Type: Numeric")
                self.currentFeatureType = 1
            elif self.currentFeatureData.str.isnumeric().any():
                self.win.typeLabel.setText("Type: Some Numeric")
                self.currentFeatureType = 0
            else:
                self.win.typeLabel.setText("Type: Not Numeric")
                self.currentFeatureType = -1
        except:
            self.win.typeLabel.setText("Type: Numeric")
            self.currentFeatureType = 1
    def changeRowCount(self):
        self.win.rowCountLabel.setText("Row Count: " + str(self.currentFeatureData.count()))
    def changeUniqueRowCount(self):
        try:
            self.win.uniqueRowCountLabel.setText("Unique Row Count: " + str(len(self.currentFeatureData.unique())))
        except Exception as e:
            print(e)
            self.win.uniqueRowCountLabel.setText("Unique Row Count: Unresolved error")
        
    def changeMean(self):
        try:
            if self.currentFeatureType == 1:
                self.win.meanLabel.setText("Mean: {0:.5f}".format(float(np.mean(self.currentFeatureData))))
            elif self.currentFeatureType == 0:
                self.win.meanLabel.setText("Mean: There is non numeric data")
            elif self.currentFeatureType == -1:
                self.win.meanLabel.setText("Mean: Feature is not numeric")
        except:
            try:
                self.win.meanLabel.setText("Mean: {0:.5f}".format(float(np.mean(self.currentFeatureData))))
            except Exception as e:
                print(e)
                self.win.meanLabel.setText("Mean: Unresolved error")
    def changeMedian(self):
        try:
            if self.currentFeatureType == 1:
                self.win.medianLabel.setText("Median: {0:.5f}".format(float(np.median(self.currentFeatureData))))
            elif self.currentFeatureType == 0:
                self.win.medianLabel.setText("Mean: There is non numeric data")
            elif self.currentFeatureType == -1:
                self.win.medianLabel.setText("Mean: Feature is not numeric")
        except:
            try:
                self.win.medianLabel.setText("Mean: {0:.5f}".format(float(np.median(self.currentFeatureData))))
            except:
                self.win.medianLabel.setText("Mean: Unresolved error")
    def changeStd(self):
        try:
            if self.currentFeatureType == 1:
                self.win.stdLabel.setText("Std: {0:.5f}".format(float(np.std(self.currentFeatureData))))
            elif self.currentFeatureType == 0:
                self.win.stdLabel.setText("Std: There is non numeric data")
            elif self.currentFeatureType == -1:
                self.win.stdLabel.setText("Std: Feature is not numeric")
        except:
            try:
                self.win.stdLabel.setText("Std: {0:.5f}".format(float(np.std(self.currentFeatureData))))
            except:
                self.win.stdLabel.setText("Std: Unresolved error")
    def changeUpperQuartile(self):
        mid = len(self.currentFeatureData) // 2
        try:
            if (len(self.currentFeatureData) % 2 == 0):
                upperQ = float(np.median(self.currentFeatureData[mid:]))
            else:
                upperQ = float(np.median(self.currentFeatureData[mid+1:]))
        except:
            self.win.upperQuartileLabel.setText("Upper Quartile: Feature is not numeric")
        try:
            if self.currentFeatureType == 1:
                self.win.upperQuartileLabel.setText("Upper Quartile: {0:.5f}".format(upperQ))
            elif self.currentFeatureType == 0:
                self.win.upperQuartileLabel.setText("Upper Quartile: There is non numeric data")
            elif self.currentFeatureType == -1:
                self.win.upperQuartileLabel.setText("Upper Quartile: Feature is not numeric")
        except:
            try:
                self.win.upperQuartileLabel.setText("Upper Quartile: {0:.5f}".format(upperQ))
            except:
                self.win.upperQuartileLabel.setText("Upper Quartile: Unresolved error")
    def changeLowerQuartile(self):
        mid = len(self.currentFeatureData) // 2
        try:
            if (len(self.currentFeatureData) % 2 == 0):
                lowerQ = float(np.median(self.currentFeatureData[:mid]))
            else:
                lowerQ = float(np.median(self.currentFeatureData[:mid]))
        except:
            self.win.lowerQuartileLabel.setText("Lower Quartile: Feature is not numeric")
            return
        try:
            if self.currentFeatureType == 1:
                self.win.lowerQuartileLabel.setText("Lower Quartile: {0:.5f}".format(lowerQ))
            elif self.currentFeatureType == 0:
                self.win.lowerQuartileLabel.setText("Lower Quartile: There is non numeric data")
            elif self.currentFeatureType == -1:
                self.win.lowerQuartileLabel.setText("Lower Quartile: Feature is not numeric")
        except:
            try:
                self.win.lowerQuartileLabel.setText("Lower Quartile: {0:.5f}".format(lowerQ))
            except:
                self.win.lowerQuartileLabel.setText("Lower Quartile: Unresolved error")
    def changeMax(self):
        try:
            if self.currentFeatureType == 1:
                self.win.maxLabel.setText("Max: {0}".format(np.max(self.currentFeatureData)))
            elif self.currentFeatureType == 0:
                self.win.maxLabel.setText("Max: There is non numeric data")
            elif self.currentFeatureType == -1:
                self.win.maxLabel.setText("Max: Feature is not numeric")
        except:
            try:
                self.win.maxLabel.setText("Max: {0}".format(np.max(self.currentFeatureData)))
            except:
                self.win.maxLabel.setText("Max: Unresolved error")
    def changeMin(self):
        try:
            if self.currentFeatureType == 1:
                self.win.minLabel.setText("Min: {0}".format(np.min(self.currentFeatureData)))
            elif self.currentFeatureType == 0:
                self.win.minLabel.setText("Min: There is non numeric data")
            elif self.currentFeatureType == -1:
                self.win.minLabel.setText("Min: Feature is not numeric")
        except:
            try:
                self.win.minLabel.setText("Min: {0}".format(np.min(self.currentFeatureData)))
            except:
                self.win.minLabel.setText("Min: Unresolved error")
    def plotDistribution(self):
        if self.dataset is None:
            self.showWarningDialog("Load a Data Set Please ;)")
            return
        if self.currentFeatureData is not None:
            if not self.win.featureListWidget.currentItem():
                self.showWarningDialog("Select a Feature Please ;)")
            if self.currentFeatureType == 1:
                if len(self.splittedDataset) == 0:
                    plt.title("Distribution Plot For Feature " + self.currentFeature)
                    plt.xlabel(self.currentFeature)
                    sns.distplot(self.currentFeatureData)
                    plt.show()
                else:
                    for key in self.splittedDataset.keys():
                        sns.distplot(self.splittedDataset[key][self.currentFeature])
                    
                    plt.legend(title='Distribution Plot', loc='upper left', labels=self.splittedDataset.keys())
                    plt.show()
            else:
                self.showWarningDialog("This Feature is not Numeric ;)")
        else:
            self.showWarningDialog("Select a Feature Please ;)")
                    
    def plotBox(self):
        if self.dataset is None:
            self.showWarningDialog("Load a Data Set Please ;)")
            return
        if self.currentFeatureData is not None:
            if not self.win.featureListWidget.currentItem():
                self.showWarningDialog("Select a Feature Please ;)")
            if self.currentFeatureType == 1:
                if self.isSplit == 1:
                    for key in self.splittedDataset.keys():
                        sns.boxplot(self.splittedDataset[key][self.currentFeature])
                    plt.legend(title='Box Plot', loc='upper left', labels=self.splittedDataset.keys())
                    plt.show()
                else:
                    plt.title("Box Plot For Feature " + self.currentFeature)
                    plt.xlabel(self.currentFeature)
                    sns.boxplot(self.currentFeatureData)
                    plt.show()
            else:
                self.showWarningDialog("This Feature is not Numeric ;)")
        else:
            self.showWarningDialog("Select a Feature Please ;)")
    def plotScatter(self):
        if self.dataset is None:
            self.showWarningDialog("Load a Data Set Please ;)")
            return
        self.secondFeature = None

        if self.currentFeatureData is None:
            self.showWarningDialog("Select a Feature Please ;)")
            return
        
        self.dialog = uic.loadUi("second.ui")
        self.dialog.setFixedSize(400, 234)
        self.dialog.featureListWidget.clear()
        for i in range(self.win.featureListWidget.count()):
            feature = self.win.featureListWidget.item(i).text()
            if self.currentFeature == feature:
                continue
            self.dialog.featureListWidget.addItem(feature)

        self.dialog.featureListWidget.itemClicked.connect(self.secondFeatureSelect)
        self.dialog.exec_()
        if self.currentFeatureType == 1:
            try:
                if self.dataset[self.secondFeature].str.isnumeric().all() != True:
                    self.showWarningDialog("Second Feature is not Numeric ;)")
                    return
            except Exception as e:
                print(e)
            if self.isSplit == 1:  
                for key in self.splittedDataset.keys():
                    sns.scatterplot(self.splittedDataset[key][self.currentFeature], self.splittedDataset[key][self.secondFeature])
                plt.legend(title='Scatter Plot', loc='upper left', labels=self.splittedDataset.keys())
                plt.show()
            else:
                plt.title("Scatter Plot For Feature " + self.currentFeature + " and " + self.secondFeature)
                plt.xlabel(self.currentFeature)
                plt.ylabel(self.secondFeature)
                sns.scatterplot(self.currentFeatureData, self.dataset[self.secondFeature])
                plt.show()
        else:
            self.showWarningDialog("This Feature is not Numeric ;)")
    def secondFeatureSelect(self):
        self.secondFeature = self.dialog.featureListWidget.currentItem().text()
        self.dialog.done(1)
    def plotHeatMap(self):
        if self.dataset is not None:
            plt.title("Heatmap")
            sns.heatmap(self.dataset.corr())
            plt.show()
        else:
            self.showWarningDialog("Load a Data Set Please ;)")

    def splitData(self):
        if self.dataset is None:
            self.showWarningDialog("Load a Data Set Please ;)")
            return
        self.isSplit = 0
        self.splitDialog = uic.loadUi("split.ui")
        self.splitDialog.setFixedSize(500, 234)
        self.splitDialog.countWarningLabel.setText("Count should be less than " + str(self.splitLimit))
        for i in range(self.win.featureListWidget.count()):
            feature = self.win.featureListWidget.item(i).text()
            self.splitDialog.featureListWidget.addItem(feature)
        self.splitDialog.featureListWidget.itemClicked.connect(self.splitDataFeatureClicked)
        self.splitDialog.splitByFeatureButton.clicked.connect(self.splitByFeature)
        self.splitDialog.exec_()
    def splitDataFeatureClicked(self):
        self.splitDialog.uniqueListWidget.clear()
        currentItem = self.splitDialog.featureListWidget.currentItem().text()
        if currentItem == self.currentFeature:
            uniqueItems = self.currentFeatureData.unique()
            self.splitDialog.uniqueCountLabel.setText("Unique Count: " + str(len(uniqueItems)))
        else:
            uniqueItems = self.dataset[currentItem].unique()
            self.splitDialog.uniqueCountLabel.setText("Unique Count: " + str(len(uniqueItems)))
        if len(uniqueItems) <= self.splitLimit:
            self.isSplit = 1
            for data in uniqueItems:
                self.splitDialog.uniqueListWidget.addItem(str(data))
        else:
            self.isSplit = 0
            self.splitDialog.uniqueListWidget.addItem("Unique Number is More Than 100")
            self.splitDialog.uniqueListWidget.addItem("It is bad for performance to show the data here")

    def splitByFeature(self):
        if self.isSplit == 1:
            self.splittedDataset.clear()
            feature = self.splitDialog.featureListWidget.currentItem().text()
            self.splitFeature = feature
            for i in range(self.splitDialog.uniqueListWidget.count()):
                value = self.splitDialog.uniqueListWidget.item(i).text()
                self.splittedDataset.update({value:self.dataset[self.dataset[feature] == value]})
            self.splitDialog.done(1)
    def clearSplittedSets(self):
        if len(self.splittedDataset) == 0:
            self.showWarningDialog("There are no splitted sets yet ;)")
            return
        self.splittedDataset.clear()
    def checkSplittedSets(self):
        if len(self.splittedDataset) > 0:
            self.splittedCheckDialog = uic.loadUi("check.ui")
            self.splittedCheckDialog.setFixedSize(215, 183)
            self.splittedCheckDialog.splitFeatureLabel.setText("feature = " + self.splitFeature)
            for key in self.splittedDataset.keys():
                self.splittedCheckDialog.splittedSetsListWidget.addItem(key)
            self.splittedCheckDialog.exec_()
        else:
            self.showWarningDialog("There are no splitted sets yet ;)")

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()
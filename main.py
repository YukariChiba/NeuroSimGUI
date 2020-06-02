#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup
from main_layout import *
from neurosim import NeuroSim
from PyQt5.QtCore import QProcess
from time import gmtime, strftime

class MainWindow(QMainWindow, Ui_MainWindow):

    arglist_ord = [
        "trfp",
        "trfl",
        "tefp",
        "tefl",
        "MNISTTrainImgs",
        "MNISTTestImgs",
        "TrainImgEpoch",
        "totEpoch",
        "intEpoch",
        "nIn",
        "nHide",
        "nOut",
        "alp1",
        "alp2",
        "maxW",
        "minW",
        "HWTrainFF",
        "HWTrainWU",
        "HWTestFF",
        "nBitInput",
        "nBitPartial",
        "nWBit",
        "BWthres",
        "Hthres",
        "nColMux",
        "nWriteColMux",
        "writeEReport",
        "SimDynPerf",
        "relaxArrCellH",
        "relaxArrCellW",
        "arrWireW",
        "node",
        "clkfq"
    ]

    arglist_dev = [
        "MaxConductance",
        "MinConductance",
        "ReadVoltage",
        "ReadPulseWidth",
        "WriteVoltageLTP",
        "WriteVoltageLTD",
        "WritePulseWidthLTP",
        "WritePulseWidthLTD",
        "WriteEnergy",
        "MaxNumLevelLTP",
        "MaxNumLevelLTD",
        "NumPulse",
        "CMOSAccess",
        "FeFET",
        "GateCapFeFET",
        "ResistanceAccess",
        "NonlinearIV",
        "NonIdenticalPulse",
        "NL",
        "ReadNoise",
        "SigmaReadNoise",
        "ConductanceRangeVar",
        "MaxConductanceVar",
        "MinConductanceVar",
        "NonlinearWrite",
        "VinitLTP",
        "VstepLTP",
        "VinitLTD",
        "VstepLTD",
        "PWinitLTP",
        "PWstepLTP",
        "PWinitLTD",
        "PWstepLTD",
        "WriteVoltageSquareSum",
        "NLLTP",
        "NLLTD",
        "SigmaDtoD",
        "SymLTPandLTD",
        "ReadEnergy",
        "Bit",
        "BitPrev",
        "HeightInFeatureSize",
        "WidthInFeatureSize",
        "WidthSRAMCellNMOS",
        "WidthSRAMCellPMOS",
        "WidthAccessCMOS",
        "MinSenseVoltage",
        "ReadEnergySRAMCell",
        "WriteEnergySRAMCell",
        "ParallelRead"
    ]

    arglist_type = [
        "Ideal",
        "Real",
        "Measured",
        "DigitalNVM",
        "SRAM"
    ]

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.IHDevice = QButtonGroup(self)
        self.IHDevice.addButton(self.IHIdeal, 0)
        self.IHDevice.addButton(self.IHReal, 1)
        self.IHDevice.addButton(self.IHMeasured, 2)
        self.IHDevice.addButton(self.IHDigitalNVM, 3)
        self.IHDevice.addButton(self.IHSRAM, 4)

        self.HODevice = QButtonGroup(self)
        self.HODevice.addButton(self.HOIdeal, 0)
        self.HODevice.addButton(self.HOReal, 1)
        self.HODevice.addButton(self.HOMeasured, 2)
        self.HODevice.addButton(self.HODigitalNVM, 3)
        self.HODevice.addButton(self.HOSRAM, 4)

        self.execute.clicked.connect(self.run_app)
        self.exit.clicked.connect(self.close)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.started.connect(lambda: self.execute.setEnabled(False)) 
        self.process.finished.connect(lambda: self.execute.setEnabled(True)) 
        self.process.readyRead.connect(self.dataReady)

        self.outfile = "log_{}.txt".format(strftime("%Y-%m-%d-%H-%M-%S", gmtime()))

    def dataReady(self):
        cursor = self.output.textCursor() 
        cursor.movePosition(cursor.End) 
        tmp_str = str(self.process.readAll(), encoding = "utf-8")
        cursor.insertText(tmp_str) 
        with open(self.outfile, "w") as f:
            f.write(tmp_str)
        self.output.ensureCursorVisible() 

    def run_app(self):
        ns = NeuroSim(self)
        ns.add_arg("IHDevice", self.arglist_type[self.IHDevice.checkedId()])
        ns.add_arg("HODevice", self.arglist_type[self.HODevice.checkedId()])
        ns.add_arg("opt", self.opt.currentText())
        for arg in self.arglist_ord:
            ns.add_arg(arg)
        for arg in self.arglist_dev:
            ns.add_arg("IHDev"+arg)
            ns.add_arg("HODev"+arg)
        #print(ns.execute())
        self.process.start(ns.execute())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

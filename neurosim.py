import sys
from PyQt5.QtWidgets import QCheckBox

class NeuroSim():
    def __init__(self, window, bin_dir="./neurosim"):
        self.bin = bin_dir
        self.arg = ""
        self.window = window

    def add_arg(self, arg_str, arg_val=None):
        comp = getattr(self.window,arg_str)
        if arg_val != None:
            val = arg_val
        elif isinstance(comp, QCheckBox):
            val = comp.isChecked()
        else:
            val = getattr(self.window,arg_str).text()
        self.arg = self.arg + " --{} {}".format(arg_str, val)

    def execute(self):
        return self.bin + self.arg
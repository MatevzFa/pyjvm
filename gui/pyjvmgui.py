import os
import sys

from PySide2 import QtWidgets
from PySide2.QtCore import QUrl, QStringListModel
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QListWidgetItem

from gui.bytecodemodel import BytecodeModel
from gui.abstractions.ops_to_bytecode import *

from gui.abstractions.bytecode import Bytecode

# DO NOT REMOVE
from gui.abstractions.ops_to_bytecode import *
from pyjvm.ops.ops_names import ops_name
from pyjvm.ops.ops_arrays import *
from pyjvm.ops.ops_calc import *
from pyjvm.ops.ops_cond import *
from pyjvm.ops.ops_convert import *
from pyjvm.ops.ops_fields import *
from pyjvm.ops.ops_invokespecial import *
from pyjvm.ops.ops_invokestatic import *
from pyjvm.ops.ops_invokevirtual import *
from pyjvm.ops.ops_invokeinterface import *
from pyjvm.ops.ops_misc import *
from pyjvm.ops.ops_ret import *
from pyjvm.ops.ops_setget import *
from pyjvm.ops.ops_shift import *


# /DO NOT REMOVE


class PyJvmGui(QQuickView):

    def __init__(self, executor, parent=None):
        super(PyJvmGui, self).__init__(parent)

        self.setResizeMode(QQuickView.SizeViewToRootObject)

        self.executor = executor
        self.show_bytecode()

        self.rootContext().setContextProperty("bytecode", self.bytecode)

        qml_file_path = os.path.join(os.path.dirname(__file__), "qml/BytecodeList.qml")
        self.setSource(QUrl(os.path.abspath(qml_file_path)))

        self.show()

    def set_executor(self, executor):
        self.executor = executor

    def show_bytecode(self):
        code_list = Bytecode.bytecode_list_from_code(self.executor.get_frame_for_thread(1).code)
        self.bytecode = BytecodeModel(bytecodes=code_list)

import os
import pprint
import random

from PySide2.QtCore import QUrl, QSize, Slot
from PySide2.QtQuick import QQuickView

from gui.bytecodemodel import BytecodeModel

from gui.abstractions.bytecode import Bytecode

# DO NOT REMOVE
from gui.abstractions.ops_to_bytecode import *
from gui.opstackmodel import OperandStackModel
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

    def __init__(self, executor, thread_idx, parent=None):
        super(PyJvmGui, self).__init__(parent)

        self.setResizeMode(QQuickView.SizeViewToRootObject)
        self.setMinimumSize(QSize(800, 500))
        self.setTitle("PyJVM - Thread " + str(thread_idx + 1))

        self.thread_idx = thread_idx
        self.executor = executor
        self.show_bytecode()

        self.rootContext().setContextProperty("app", self)

        qml_file_path = os.path.join(os.path.dirname(__file__), "qml/App.qml")
        self.setSource(QUrl(os.path.abspath(qml_file_path)))

        # Step button

        self.show()

    def set_executor(self, executor):
        self.executor = executor

    def show_bytecode(self):
        code_list = Bytecode.bytecode_list_from_code(self.executor.get_frame_for_thread(self.thread_idx).code)
        self.loc_to_idx = {}
        for i, code in enumerate(code_list):
            self.loc_to_idx[code.loc] = i
        # pprint.pprint(self.loc_to_idx)
        self.bytecode = BytecodeModel(bytecodes=code_list)
        self.rootContext().setContextProperty("bytecode", self.bytecode)

        self.frame_info = self.executor.get_frame_for_thread(self.thread_idx).desc
        self.rootContext().setContextProperty("frameInfo", self.frame_info)

        op_stack = self.executor.get_frame_for_thread(self.thread_idx).stack

        self.operand_stack = OperandStackModel(operands=op_stack)
        self.rootContext().setContextProperty("operandStack", self.operand_stack)

    @Slot()
    def stepExecutor(self):
        frame_alive = self.executor.step_thread(self.thread_idx)
        self.show_bytecode()

    @Slot()
    def stepOut(self):
        self.executor.step_thread_until_frame_over(self.thread_idx)
        self.show_bytecode()

    @Slot(result=int)
    def getCurLoc(self):
        return self.loc_to_idx.get(self.executor.get_frame_for_thread(self.thread_idx).pc)

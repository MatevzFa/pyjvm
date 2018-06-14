from pyjvm import bytecode as bytecodeutil
from ops_to_bytecode import *


class Bytecode:

    def __init__(self, loc, opcode, operands):
        """

        :param opcode: numeric representation of this bytecode instruction
        :param operands: array of operands
        """
        self.loc = loc
        self.opcode = opcode
        self.name = bytecodeutil.get_operation(opcode)
        self.operands = operands

    def __str__(self):
        return "{0}: {1} {2}".format(self.loc, self.opcode, str(self.operands))

    @staticmethod
    def bytecode_list_from_code(code):
        """
        Construct a list of Bytecode instances
        :param code: bytes representing a frame's bytecode
        :return: array of Bytecode instances
        """
        bytecodes = []
        cur_loc = 0
        while cur_loc < len(code):
            opcode = hex(ord(code[cur_loc]))
            disasm_oper = bytecodeutil.get_to_bytecode(opcode)
            size, bytecode = disasm_oper(cur_loc, code)
            cur_loc += size
            bytecodes.append(bytecode)
        return bytecodes

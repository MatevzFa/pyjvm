import fileinput

CSV_DELIM = "\t"

out_file = open("pyjvm/operands/ops_operands.py", "w")

out_file.write("""
from pyjvm.bytecode import operands
import logging
import struct

logger = logging.getLogger(__name__)


def unpack_byte(bin_str):
    return struct.unpack(">b", bin_str)[0]

def unpack_short(bin_str):
    return struct.unpack(">h", bin_str)[0]

def unpack_int(bin_str):
    return struct.unpack(">i", bin_str)[0]
""")


def n_operands_normal(op, opcode, nargs, division_arr):
    out_file.write("""
@operands(code=0x{1})
def {0}(frame):
    division_arr = {3} 
    operands = []
    offset = 1
    for op in division_arr:
        cur_op_slice = frame.code[frame.pc + offset : frame.pc + offset + op]
        if op == 1:
            operands.append(unpack_byte(cur_op_slice))
        elif op == 2:
            operands.append(unpack_short(cur_op_slice))
        elif op == 4:
            operands.append(unpack_int(cur_op_slice))
        offset += op
    return operands
""".format(op.strip(), opcode.strip(), nargs.strip(), str(division_arr)))


def n_operands_none(op, opcode):
    out_file.write("""
@operands(code=0x{1})
def {0}(frame):
    return []
""".format(op.strip(), opcode.strip()))


def n_operands_not_supported(op, opcode, nargs):
    out_file.write("""
@operands(code=0x{1})
def {0}(frame):
    logger.warn("{0} operands not supported")
    return []
""".format(op.strip(), opcode.strip(), nargs.strip()))


for line in fileinput.input():
    op, opcode, nargs, division = [x.strip() for x in line.split(CSV_DELIM)]

    if op == "return":
        op = "return_"

    if nargs == "?":
        n_operands_not_supported(op, opcode, nargs)
        continue

    try:
        n = int(nargs)
        if n == 0:
            n_operands_none(op, opcode)
        else:
            division_arr = [int(x) for x in division.split(",")]
            n_operands_normal(op, opcode, nargs, division_arr)
    except ValueError:
        print "cannot parse", nargs
        continue

out_file.close()

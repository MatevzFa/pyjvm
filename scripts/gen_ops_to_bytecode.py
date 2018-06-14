import fileinput

CSV_DELIM = "\t"

out_file = open("gui/abstractions/ops_to_bytecode.py", "w")

out_file.write("""
from pyjvm.bytecode import to_bytecode
from gui.abstractions.bytecode import Bytecode
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


def to_bytecode_normal(op, opcode, nargs, division_arr):
    out_file.write('''
@to_bytecode(code=0x{1})
def {0}(loc, code):
    """
    :return (size, Bytecode)
    """
    division_arr = {3}
    operands = []
    offset = 1
    for op in division_arr:
        cur_op_slice = code[loc + offset : loc + offset + op]
        if op == 1:
            operands.append(unpack_byte(cur_op_slice))
        elif op == 2:
            operands.append(unpack_short(cur_op_slice))
        elif op == 4:
            operands.append(unpack_int(cur_op_slice))
        offset += op
    
    return (1 + {2}, Bytecode(loc, 0x{1}, operands)) 
'''.format(op.strip(), opcode.strip(), nargs.strip(), str(division_arr)))


def to_bytecode_none(op, opcode):
    out_file.write('''
@to_bytecode(code=0x{1})
def {0}(loc, code):
    """
    :return (size, Bytecode)
    """
    return (1, Bytecode(loc, 0x{1}, []))
    '''.format(op.strip(), opcode.strip()))


def to_bytecode_lookupswitch(op, opcode):
    out_file.write('''
@to_bytecode(code=0x{1})
def {0}(loc, code):
    """
    https://cs.au.dk/~mis/dOvs/jvmspec/ref--41.html
    :return:
    """
    loc_offset = loc + 1
    operands = []
    while loc_offset % 4 != 0:
        loc_offset += 1

    default_offset = unpack_int(code[loc_offset: loc_offset + 4])
    loc_offset += 4
    operands.append(default_offset)

    n = unpack_int(code[loc_offset: loc_offset + 4])
    loc_offset += 4
    operands.append(n)

    for i in range(n):
        key = unpack_int(code[loc_offset: loc_offset + 4])
        loc_offset += 4
        operands.append(key)
        offset = unpack_int(code[loc_offset: loc_offset + 4])
        loc_offset += 4
        operands.append(offset)
        
    return (loc_offset - loc, Bytecode(loc, 0x{1}, operands))
'''.format(op.strip(), opcode.strip()))


def to_bytecode_not_supported(op, opcode, nargs):
    out_file.write("""
@to_bytecode(code=0x{1})
def {0}(code):
    logger.warn("{0} operands not supported")
    return []
""".format(op.strip(), opcode.strip(), nargs.strip()))


for line in fileinput.input():
    op, opcode, nargs, division = [x.strip() for x in line.split(CSV_DELIM)]

    if op == "return":
        op = "return_"

    if op == "lookupswitch":
        to_bytecode_lookupswitch(op, opcode)
        continue

    if nargs == "?":
        to_bytecode_not_supported(op, opcode, nargs)
        continue

    try:
        n = int(nargs)
        if n == 0:
            to_bytecode_none(op, opcode)
        else:
            division_arr = [int(x) for x in division.split(",")]
            to_bytecode_normal(op, opcode, nargs, division_arr)
    except ValueError:
        print "cannot parse", nargs
        continue

out_file.close()

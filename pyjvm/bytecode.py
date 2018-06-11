BYTECODE = {}
OPERANDS = {}


def bytecode(code):
    def cl(func):
        BYTECODE[hex(code)] = func
        return func

    return cl


def operands(code):
    def cl(func):
        OPERANDS[hex(code)] = func
        return func

    return cl


def get_operands(code):
    return OPERANDS.get(code)


def get_operation(code):
    return BYTECODE.get(code)


def get_operation_name(code):
    if code in BYTECODE:
        a = BYTECODE[code]
        return a.__name__
    return ""


class Node(object):

    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


class Declarations(Node):
    def __init__(self, declarations=None, declaration=None):
        self.declarations = declarations
        self.declaration = declaration


class Declaration(Node):
    def __init__(self, type, inits=None):
        self.type = type
        self.inits = inits


class Inits(Node):
    def __init__(self, init, inits=None):
        self.init = init
        self.inits = inits


class Init(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class Instructions(Node):
    def __init__(self, instruction, instructions=None):
        self.instructions = instructions
        self.instruction = instruction


class Instruction(Node):
    def __init__(self, instruction):
        self.instruction = instruction


class Print_instr(Node):
    def __init__(self, expression):
        self.expression = expression


class Labeled_instr(Node):
    def __init__(self, id, instruction):
        self.id = id
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class Choice_instr(Node):
    def __init__(self, condition, instruction, elseinstruction = None):
        self.condition = condition
        self.instruction = instruction
        self.elseinstruction = elseinstruction


class While_instr(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class Repeat_instr(Node):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition


class Return_instr(Node):
    def __init__(self, expression):
        self.expression = expression


class Continue_instr(Node):
    pass

class Break_instr(Node):
    pass


class Compound_instr(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions


class Condition(Node):
    def __init__(self, expression):
        self.expression = expression

class Const(Node):
    def __init__(self, const_value):
        self.const_value = const_value


class Expression(Node):
    def __init__(self, expression1, typeexpr, expression2, id_or_const = None):
        self.expression1 = expression1
        self.typeexpr = typeexpr
        self.expression2 = expression2
        self.id_or_const = id_or_const

class Funcall(Node):
    def __init__(self, id, expr_list_or_empty):
        self.id = id
        self.expr_list_or_empty = expr_list_or_empty

class ExprInBrackets(Node):
    def __init__(self, expression):
        self.expression = expression

class Expr_list_or_empty(Node):
    def __init__(self, expr_list = None):
        self.expr_list = expr_list


class Expr_list(Node):
    def __init__(self, expression, expr_list=None):
        self.expr_list = expr_list
        self.expression = expression


class Fundefs(Node):
    def __init__(self, fundef = None, fundefs = None):
        self.fundef = fundef
        self.fundefs = fundefs


class Fundef(Node):
    def __init__(self, type, id, args_list_or_empty, compound_instruction):
        self.type = type
        self.id = id
        self.arg_list = args_list_or_empty
        self.compound_instr = compound_instruction


class Args_list_or_empty(Node):
    def __init__(self, args_list = None):
        self.args_list = args_list

class Args_list(Node):
    def __init__(self, arg, args_list = None):
        self.args_list = args_list
        self.arg = arg

class Arg(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id


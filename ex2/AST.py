
class Node(object):

    def __str__(self):
        return self.printTree()

    def accept(self, visitor):
        classname = self.__class__.__name__
        fun = getattr(visitor, 'visit_' + classname, None)
        if fun:
            return fun(self)
        print "Lack of some visit_function: " + self.__class__.__name__

    def accept2(self, visitor):
        return visitor.visit(self)



class Program(Node):
    def __init__(self, lineno, declarations, fundefs, instructions):
        self.lineno = lineno
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


class Declarations(Node):
    def __init__(self):
        self.declarations = []

class Declaration(Node):
    def __init__(self, lineno, type, inits=None):
        self.type = type
        self.inits = inits
        self.lineno = lineno


class Inits(Node):
    def __init__(self):
        self.inits = []

class Init(Node):
    def __init__(self, lineno, id, expression):
        self.id = id
        self.expression = expression
        self.lineno = lineno

class Instructions(Node):
    def __init__(self):
        self.instructions = []



class Print_instr(Node):
    def __init__(self, lineno, expression):
        self.expression = expression
        self.lineno = lineno

class Labeled_instr(Node):
    def __init__(self, lineno, id, instruction):
        self.id = id
        self.instruction = instruction
        self.lineno = lineno

class Assignment(Node):
    def __init__(self, lineno, id, expression):
        self.id = id
        self.expression = expression
        self.lineno = lineno

class Choice_instr(Node):
    def __init__(self, lineno, condition, instruction, elseinstruction = None):
        self.condition = condition
        self.instruction = instruction
        self.elseinstruction = elseinstruction
        self.lineno = lineno

class While_instr(Node):
    def __init__(self, lineno, condition, instruction):
        self.condition = condition
        self.instruction = instruction
        self.lineno = lineno

class Repeat_instr(Node):
    def __init__(self, lineno, instruction, condition):
        self.instruction = instruction
        self.condition = condition
        self.lineno = lineno

class Return_instr(Node):
    def __init__(self, lineno, expression):
        self.expression = expression
        self.lineno = lineno

class Continue_instr(Node):
    def __init__(self, lineno):
        self.lineno = lineno


class Break_instr(Node):
    def __init__(self, lineno):
        self.lineno = lineno


class Compound_instr(Node):
    def __init__(self, lineno, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions
        self.lineno = lineno

class Integer(Node):
    def __init__(self, lineno, value):
        self.value = value
        self.lineno = lineno

class Float(Node):
    def __init__(self, lineno, value):
        self.value = value
        self.lineno = lineno

class String(Node):
    def __init__(self, lineno, value):
        self.value = value
        self.lineno = lineno

class Variable(Node):
    def __init__(self, lineno, id):
        self.id = id
        self.lineno = lineno

class Expression(Node):
    def __init__(self, lineno, left, oper, right):
        self.left = left
        self.oper = oper
        self.right = right
        self.lineno = lineno

class Funcall(Node):
    def __init__(self, lineno, id, expr_list_or_empty):
        self.id = id
        self.expr_list_or_empty = expr_list_or_empty
        self.lineno = lineno

class Expressions(Node):
    def __init__(self, lineno):
        self.expr_list = []
        self.lineno = lineno


class Fundefs(Node):
    def __init__(self, lineno):
        self.fundefs = []
        self.lineno = lineno


class Fundef(Node):
    def __init__(self, lineno, type, id, args_list_or_empty, compound_instruction):
        self.type = type
        self.id = id
        self.arg_list = args_list_or_empty
        self.compound_instr = compound_instruction
        self.lineno = lineno

class Args_list(Node):
    def __init__(self, lineno):
        self.args_list = []
        self.lineno = lineno

class Arg(Node):
    def __init__(self, lineno, type, id):
        self.type = type
        self.id = id
        self.lineno = lineno


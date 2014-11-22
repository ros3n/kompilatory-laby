#!/usr/bin/python


from SymbolTable import FunctionsTable
from SymbolTable import SymbolTable


class TypeChecker(object):
    ttype = {
        '+': {
            'str': {'str': 'str'},
            'int': {'float': 'float', 'int': 'int'},
            'float': {'float': 'float', 'int': 'float'}},
        '-': {
            'int': {'int': 'int', 'float': 'float'},
            'float': {'float': 'float', 'int': 'float'}},
        '*': {
            'str': {'int': 'str'},
            'int': {'int': 'int', 'float': 'float'},
            'float': {'int': 'float', 'float': 'float'}},
        '/': {
            'int': {'int': 'int', 'float': 'float'},
            'float': {'float': 'float', 'int': 'float'}},
        '!=': {
            'string': {'string': 'int'},
            'int': {'float': 'int', 'int': 'int'},
            'float': {'int': 'int', 'float': 'int'}},
        '<': {
            'string': {'string': 'int'},
            'int': {'float': 'int', 'int': 'int'},
            'float': {'int': 'int', 'float': 'int'}},
        '<=': {
            'string': {'string': 'int'},
            'int': {'float': 'int', 'int': 'int'},
            'float': {'int': 'int', 'float': 'int'}},
        '>': {
            'string': {'string': 'int'},
            'int': {'float': 'int', 'int': 'int'},
            'float': {'int': 'int', 'float': 'int'}},
        '>=': {
            'string': {'string': 'int'},
            'int': {'float': 'int', 'int': 'int'},
            'float': {'int': 'int', 'float': 'int'}},
        '==': {
            'string': {'string': 'int'},
            'int': {'float': 'int', 'int': 'int'},
            'float': {'int': 'int', 'float': 'int'}},
        '%': {
            'int': {'int': 'int'}},
        '^': {
            'int': {'int': 'int', 'float': 'float'},
            'float': {'int': 'float', 'float': 'float'}},
        '&': {
            'int': {'int': 'int'}},
        'AND': {
            'int': {'int': 'int'}},
        'OR': {
            'int': {'int': 'int'}},
        'SHL': {
            'int': {'int': 'int'}},
        'SHR': {
            'int': {'int': 'int'}},
        'EQ': {
            'int': {'int': 'int'}},
        'NEQ': {
            'int': {'int': 'int'}},
        'LE': {
            'int': {'int': 'int'}},
        'GE': {
            'int': {'int': 'int'}}
    }

    errors = []


    def visit_Program(self, node):
        node.Functions = FunctionsTable("ProgramF")
        node.Variables = SymbolTable("ProgramV")

        node.declarations.Functions = node.Functions
        node.declarations.Variables = node.Variables
        node.fundefs.Functions = node.Functions
        node.fundefs.Variables = node.Variables
        node.instructions.Functions = node.Functions
        node.instructions.Variables = node.Variables

        node.declarations.accept(self)
        node.fundefs.accept(self)
        node.instructions.accept(self)
        return self.errors

    def visit_Declarations(self, node):
        for elem in node.declarations:
            elem.Functions = node.Functions
            elem.Variables = node.Variables
            elem.accept(self)


    def visit_Declaration(self, node):
        node.inits.Functions = node.Functions
        node.inits.Variables = node.Variables
        self.visit_Inits(node.inits, node.type)


    def visit_Inits(self, node, type):
       for elem in node.inits:
            elem.Functions = node.Functions
            elem.Variables = node.Variables
            self.visit_Init(elem, type)

    def visit_Init(self, node, type):
        if node.Variables.put(node.id, type) == -1:
            self.errors.append(str(node.lineno) + ": " + node.id + " already initialized")

    def visit_Instructions(self, node):
        for elem in node.instructions:
            elem.Functions = node.Functions
            elem.Variables = node.Variables
            elem.accept(self)


    def visit_Instruction(self, node):
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept(self)

    def visit_Print_instr(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        node.expression.accept(self)

    def visit_Labeled_instr(self, node):
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept(self)

    def visit_Assignment(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        #TODO
        type1 = node.Variables.get(node.id)
        if type1 == -1:
            self.errors.append(str(node.lineno) + ": " + node.id + " undeclared")
            return

        type2 = node.expression.accept(self)
        if type2 == -1:
            self.errors.append(str(node.lineno) + ": wrong expression")
            return

        if type1 != type2:
            self.errors.append(str(node.lineno) + ": Type mismatch: " + str(type2) + " and " + str(type1))

    def visit_Choice_instr(self, node):
        node.condition.Functions = node.Functions
        node.condition.Variables = node.Variables
        node.condition.accept(self)
        node.instruction.Functions = FunctionsTable("Functions", node.Functions)
        node.instruction.Variables = SymbolTable("Variables", node.Variables)
        node.instruction.accept(self)

        if node.elseinstruction:
            node.elseinstruction.Functions = FunctionsTable("Functions", node.Functions)
            node.elseinstruction.Variables = SymbolTable("Variables", node.Variables)
            node.elseinstruction.accept(self)

    def visit_While_instr(self, node):
        node.condition.Functions = node.Functions
        node.condition.Variables = node.Variables
        node.condition.accept(self)
        node.instruction.Functions = FunctionsTable("Functions", node.Functions)
        node.instruction.Variables = SymbolTable("Variables", node.Variables)
        node.instruction.accept(self)

    def visit_Repeat_instr(self, node):
        Functions = FunctionsTable("Functions", node.Functions)
        Variables = SymbolTable("Variables", node.Variables)
        node.instructions.Functions = Functions
        node.instructions.Variables = Variables
        node.instructions.accept(self)
        node.condition.Functions = Functions
        node.condition.Variables = Variables
        node.condition.accept(self)

    def visit_Return_instr(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        node.expression.accept(self)

    def visit_Compound_instr(self, node):
        Functions = FunctionsTable("Functions", node.Functions)
        Variables = SymbolTable("Variables", node.Variables)
        node.declarations.Functions = Functions
        node.declarations.Variables = Variables
        node.declarations.accept(self)
        node.instructions.Functions = Functions
        node.instructions.Variables = Variables
        node.instructions.accept(self)

    def visit_Condition(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        node.expression.accept(self)

    def visit_Expression(self, node):
        node.left.Functions = node.Functions
        node.left.Variables = node.Variables
        type1 = node.left.accept(self)
        node.right.Functions = node.Functions
        node.right.Variables = node.Variables
        type2 = node.right.accept(self)
        if node.oper in self.ttype.keys() and type1 in self.ttype[node.oper].keys() and type2 in \
                self.ttype[node.oper][type1].keys():
            return self.ttype[node.oper][type1][type2]
        else:
            self.errors.append(str(node.right.lineno) + ": Invalid expression")
            return type1

    def visit_ExprNested(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        return node.expression.accept(self)

    def visit_SingleExpression(self, node):
        if node.id.__class__.__name__ in ["Integer", "Float", "String"]:
            node.id.Functions = node.Functions
            node.id.Variables = node.Variables
            return node.id.accept(self)
        if node.Variables.get(node.id)== -1:
           self.errors.append(str(node.lineno) + ": Couldn't find the variable" + node.id)
           return node.type
        return node.Variables.get(node.id)

    def visit_Integer(self, node):
        return "int"

    def visit_Float(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_Funcall(self, node):
        type1 = node.Functions.get(node.id)
        node.expr_list_or_empty.Functions = node.Functions
        node.expr_list_or_empty.Variables = node.Variables
        type2 = node.expr_list_or_empty.accept(self)
        if type1[0] != type2:
            self.errors.append(str(node.lineno) + ": Function args mismatch")
        return type1[1]


    def visit_Expr_list_or_empty(self, node):
        l = []
        for elem in node.expr_list:
            elem.Functions = node.Functions
            elem.Variables = node.Variables
            l.append(elem.accept(self))
        return l



    def visit_Fundefs(self, node):
        for elem in node.fundefs:
            elem.Functions = node.Functions
            elem.Variables = node.Variables
            elem.accept(self)

    def visit_Fundef(self, node):
        node.Functions.putNewFun(node.id, node.type)
        Functions = FunctionsTable("Functions", node.Functions)
        Variables = SymbolTable("Variables", node.Variables)
        node.arg_list.Functions = Functions
        node.arg_list.Variables = Variables
        listOfArguments = node.arg_list.accept(self)
        for element in listOfArguments:
            if element != None:
                node.Functions.put(node.id, element[1])
                if Variables.put(element[0], element[1]) == -1:
                    self.errors.append(
                        "In line " + str(node.lineno) + ": Variable " + element.name + " already initialized")
        node.compound_instr.Functions = Functions
        node.compound_instr.Variables = Variables
        node.compound_instr.accept(self)


    def visit_Args_list(self, node):
        l1 = []
        for elem in node.args_list:
            elem.Functions = node.Functions
            elem.Variables = node.Variables
            l1.append(elem.accept(self))
        return l1

    def visit_Arg(self, node):
        return node.id, node.type
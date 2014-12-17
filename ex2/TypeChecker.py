#!/usr/bin/python


from SymbolTable import FunctionsTable
from SymbolTable import SymbolTable

def tables(parent):
        return FunctionsTable("Smth", parent[0]), SymbolTable("Smth", parent[1])


class TypeChecker(object):
    ttype = {
        '+': {
            'string': {'string': 'string'},
            'int': {'float': 'float', 'int': 'int'},
            'float': {'float': 'float', 'int': 'float'}},
        '-': {
            'int': {'int': 'int', 'float': 'float'},
            'float': {'float': 'float', 'int': 'float'}},
        '*': {
            'string': {'int': 'string'},
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
        self.loop = 0
        self.retfun = 0
        node.Tables = tables((None, None))

        node.declarations.Tables = node.Tables
        node.fundefs.Tables = node.Tables
        node.instructions.Tables = node.Tables

        node.declarations.accept(self)
        node.fundefs.accept(self)
        node.instructions.accept(self)
        return self.errors

    def visit_Declarations(self, node):
        for elem in node.declarations:
            elem.Tables = node.Tables
            elem.accept(self)


    def visit_Declaration(self, node):
        node.inits.Tables = node.Tables
        self.visit_Inits(node.inits, node.type)



    def visit_Inits(self, node, type):
       for elem in node.inits:
            elem.Tables = node.Tables
            self.visit_Init(elem, type)

    def visit_Init(self, node, type):
        node.expression.Tables = node.Tables
        expr_type = node.expression.accept(self)
        if expr_type != type and not (type == "float" and expr_type == "int"):
            self.errors.append(str(node.lineno) + ": " + node.id + " expected " + type + " got " + expr_type)
        if node.Tables[1].put(node.id, type) == -1:
            self.errors.append(str(node.lineno) + ": " + node.id + " already initialized")

    def visit_Instructions(self, node):
        for elem in node.instructions:
            elem.Tables = node.Tables
            elem.accept(self)


    def visit_Instruction(self, node):
        node.instruction.Tables = node.Tables
        node.instruction.accept(self)

    def visit_Print_instr(self, node):
        node.expression.Tables = node.Tables
        node.expression.accept(self)

    def visit_Labeled_instr(self, node):
        node.instruction.Tables = node.Tables
        node.instruction.accept(self)

    def visit_Assignment(self, node):
        node.expression.Tables = node.Tables
        type1 = node.Tables[1].get(node.id)
        if type1 == -1:
            self.errors.append(str(node.lineno) + ": " + node.id + " undeclared")
            return

        type2 = node.expression.accept(self)
        if type2 == -1:
            self.errors.append(str(node.lineno) + ": wrong type")
            return

        if type1 != type2:
            self.errors.append(str(node.lineno) + ": Type mismatch: " + str(type2) + " and " + str(type1))

    def visit_Choice_instr(self, node):
        node.condition.Tables = node.Tables
        node.condition.accept(self)
        node.instruction.Tables = tables(node.Tables)
        node.instruction.accept(self)

        if node.elseinstruction:
            node.elseinstruction.Tables = tables(node.Tables)
            node.elseinstruction.accept(self)

    def visit_While_instr(self, node):
        node.condition.Tables = node.Tables
        node.condition.accept(self)
        node.instruction.Tables = tables(node.Tables)
        self.loop+=1
        node.instruction.accept(self)
        self.loop-=1

    def visit_Repeat_instr(self, node):
        node.instruction.Tables = tables(node.Tables)
        self.loop+=1
        node.instruction.accept(self)
        self.loop-=1
        node.condition.Tables = node.instruction.Tables
        node.condition.accept(self)

    def visit_Return_instr(self, node):
        if self.retfun == 0:
            self.errors.append(str(node.lineno) + ": return outside function")

        node.expression.Tables = node.Tables
        type1 = node.expression.accept(self)
        type2 = self.currtype
        if type1 != type2:
            self.errors.append(str(node.lineno) + ": return type other than function")

    def visit_Break_instr(self, node):
        if self.loop == 0:
            self.errors.append(str(node.lineno) + ": Break outside loop")

    def visit_Continue_instr(self, node):
        if self.loop == 0:
            self.errors.append(str(node.lineno) + ": continue outside loop")

    def visit_Compound_instr(self, node):
        Table = tables(node.Tables)
        node.declarations.Tables = Table
        node.declarations.accept(self)
        node.instructions.Tables = Table
        node.instructions.accept(self)

    def visit_Condition(self, node):
        node.expression.Tables = node.Tables
        node.expression.accept(self)

    def visit_Expression(self, node):
        node.left.Tables = node.Tables
        type1 = node.left.accept(self)
        node.right.Tables = node.Tables
        type2 = node.right.accept(self)
        if node.oper in self.ttype.keys() and type1 in self.ttype[node.oper].keys() and type2 in \
                self.ttype[node.oper][type1].keys():
            return self.ttype[node.oper][type1][type2]
        else:
            self.errors.append(str(node.lineno) + ": Invalid expression in operands of type " + type1 + " and " + type2 + " for operator " + node.oper)
            return type1



    def visit_Variable(self, node):
        if node.id.__class__.__name__ in ["Integer", "Float", "String"]:
            node.id.Tables = node.Tables
            return node.id.accept(self)
        if node.Tables[1].get(node.id)== -1:
            self.errors.append(str(node.lineno) + ": Couldn't find the variable" + node.id)
            return node.type
        return node.Tables[1].get(node.id)

    def visit_Integer(self, node):
        return "int"

    def visit_Float(self, node):
        return "float"

    def visit_String(self, node):
        return "string"

    def visit_Funcall(self, node):
        type1 = node.Tables[0].get(node.id)
        if type1 == -1:
            self.errors.append("Line " + str(node.lineno) + ": Function not found")
            return 'int'
        node.expr_list_or_empty.Tables = node.Tables
        type2 = node.expr_list_or_empty.accept(self)
        if len(type1[0]) != len(type2):
              self.errors.append(str(node.lineno) + ": Wrong number of arguments in function: " + node.id)
              return type1[1]
        for num, type in enumerate(type1[0]):
            if type != type2[num] and (not (type == "float" and type2[num] == "int")):
                self.errors.append(str(node.lineno) + ": Function args mismatch: " + type + " and " + type2[num])
        return type1[1]


    def visit_Expressions(self, node):
        l = []
        for elem in node.expr_list:
            elem.Tables = node.Tables
            l.append(elem.accept(self))
        return l



    def visit_Fundefs(self, node):
        for elem in node.fundefs:
            elem.Tables = node.Tables
            elem.Tables[0].putNewFun(elem.id, elem.type)
            Table = tables(elem.Tables)
            elem.arg_list.Tables = Table
            listOfArguments = elem.arg_list.accept(self)
            for element in listOfArguments:
                if element != None:
                    elem.Tables[0].put(elem.id, element[1])
                    if Table[1].put(element[0], element[1]) == -1:
                        self.errors.append(
                        "In line " + str(node.lineno) + ": Variable " + element.name + " already initialized")
        for elem in node.fundefs:
            elem.accept(self)

    def visit_Fundef(self, node):
        self.retfun += 1
        self.currtype = node.type
        node.compound_instr.Tables = node.arg_list.Tables
        node.compound_instr.accept(self)
        self.retfun -= 1

    def visit_Args_list(self, node):
        l1 = []
        for elem in node.args_list:
            elem.Tables = node.Tables
            l1.append(elem.accept(self))
        return l1

    def visit_Arg(self, node):
        return node.id, node.type
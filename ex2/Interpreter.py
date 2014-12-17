import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *


class Interpreter(object):


    @on('node')
    def visit(self, node):
        pass

    @when(AST.Node)
    def visit(self, node):
        print "Unrecognized node"

    @when(AST.Program)
    def visit(self, node):
        self.functions = {}
        self.memoryStack = MemoryStack(Memory("global"))
        node.declarations.accept2(self)
        node.fundefs.accept2(self)
        node.instructions.accept2(self)


    @when(AST.Declarations)
    def visit(self, node):
        for dec in node.declarations:
            dec.inits.accept2(self)

    @when(AST.Inits)
    def visit(self, node):
        for init in node.inits:
            init.accept2(self)

    @when(AST.Init)
    def visit(self, node):
        self.memoryStack.insert(node.id, node.expression.accept2(self))

    @when(AST.Variable)
    def visit(self, node):
        if isinstance(node.id, str):
            return self.memoryStack.get(node.id)
        return node.id.accept2(self)

    @when(AST.Integer)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Float)
    def visit(self, node):
        return node.value

    @when(AST.Expression)
    def visit(self, node):
        if node.oper == '%':
            return node.left.accept2(self) % node.right.accept2(self)
        if node.oper == '*':
            return node.left.accept2(self) * node.right.accept2(self)
        if node.oper == '/':
            return node.left.accept2(self) / node.right.accept2(self)
        if node.oper == '+':
            return node.left.accept2(self) + node.right.accept2(self)
        if node.oper == '-':
            return node.left.accept2(self) - node.right.accept2(self)
        if node.oper == '==':
            return node.left.accept2(self) == node.right.accept2(self)
        if node.oper == '!=':
            return node.left.accept2(self) != node.right.accept2(self)
        if node.oper == '>=':
            return node.left.accept2(self) >= node.right.accept2(self)
        if node.oper == '<=':
            return node.left.accept2(self) <= node.right.accept2(self)
        if node.oper == '<':
            return node.left.accept2(self) < node.right.accept2(self)
        if node.oper == '>':
            return node.left.accept2(self) > node.right.accept2(self)


    @when(AST.Instructions)
    def visit(self, node):
        for ins in node.instructions:
            ins.accept2(self)

    @when(AST.Print_instr)
    def visit(self, node):
        print node.expression.accept2(self)

    @when(AST.Assignment)
    def visit(self, node):
        self.memoryStack.set(node.id, node.expression.accept2(self))

    @when(AST.Choice_instr)
    def visit(self, node):
        if node.elseinstruction:
            if node.condition.accept2(self):
                node.instruction.accept2(self)
            else:
                node.elseinstruction.accept2(self)
        else:
            if node.condition.accept2(self):
                node.instruction.accept2(self)

    @when(AST.While_instr)
    def visit(self, node):
        while node.condition.accept2(self):
            try:
                node.instruction.accept2(self)
            except ContinueException:
                continue
            except BreakException:
                break


    @when(AST.Repeat_instr)
    def visit(self, node):
        while True:
            try:
                node.instruction.accept2(self)
            except ContinueException:
                continue
            except BreakException:
                break
            if node.condition.accept2(self):
                break

    @when(AST.Return_instr)
    def visit(self, node):
        raise ReturnValueException(node.expression.accept2(self))

    @when(AST.Break_instr)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue_instr)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Compound_instr)
    def visit(self, node):
        self.memoryStack.push(Memory("CompoundMem"))
        node.declarations.accept2(self)
        try:
            node.instructions.accept2(self)
        finally:
            self.memoryStack.pop()

    @when(AST.Fundefs)
    def visit(self, node):
        for fun in node.fundefs:
            fun.accept2(self)

    @when(AST.Fundef)
    def visit(self, node):
        self.functions[node.id] = node.arg_list.accept2(self), node.compound_instr

    @when(AST.Args_list)
    def visit(self, node):
        l = []
        for ar in node.args_list:
            l.append(ar.accept2(self))
        return l
    @when(AST.Arg)
    def visit(self, node):
        return node.id

    @when(AST.Expressions)
    def visit(self, node):
        l = []
        for el in node.expr_list:
            l.append(el.accept2(self))
        return l

    @when(AST.Funcall)
    def visit(self, node):
        result = 0
        vals = node.expr_list_or_empty.accept2(self)
        fun = self.functions[node.id]
        self.memoryStack.push(Memory("FunHeaderStack"))
        for name, val in zip(fun[0], vals):
            self.memoryStack.insert(name, val)
        try:
            fun[1].accept2(self)
        except ReturnValueException, a:
            result = a.value
        except ContinueException:
            pass
        except BreakException:
            pass
        finally:
            self.memoryStack.pop()
            return result
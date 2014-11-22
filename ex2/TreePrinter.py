
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self):
        result = "DECL\n"
        result += self.declarations.printTree("")
        result += "FUNDEF\n"
        result += self.fundefs.printTree("")
        result += "INSTRUCTIONS\n"
        result += self.instructions.printTree("")
        return result

    @addToClass(AST.Declarations)
    def printTree(self, depth):
        result = ""
        for elem in self.declarations:
            result += elem.printTree(depth)
        return result

    @addToClass(AST.Declaration)
    def printTree(self, depth):
        result = ""
        if self.inits:
            result += self.inits.printTree(depth)
        return result

    @addToClass(AST.Inits)
    def printTree(self, depth):
        result = ""
        for elem in self.inits:
            result += elem.printTree(depth + "| ")
        return result

    @addToClass(AST.Init)
    def printTree(self, depth):
        result = depth + "=\n"
        result += depth + "| "
        result += self.id
        result += "\n"
        result += self.expression.printTree(depth + "| ")
        return result

    @addToClass(AST.Instructions)
    def printTree(self, depth):
        result = ""
        for elem in self.instructions:
            result += elem.printTree(depth)
        return result


    @addToClass(AST.Print_instr)
    def printTree(self, depth):
        return depth + "PRINT\n" + self.expression.printTree(depth + "| ")

    @addToClass(AST.Labeled_instr)
    def printTree(self):
        #TODO
        return ""

    @addToClass(AST.Assignment)
    def printTree(self, depth):
        return depth + "=\n" + depth + "| " + self.id + "\n" + self.expression.printTree(depth + "| ")

    @addToClass(AST.Choice_instr)
    def printTree(self, depth):
        result = depth + "IF\n"
        result += self.condition.printTree(depth + "| ")
        result += self.instruction.printTree(depth + "| ")
        if self.elseinstruction:
            result += depth + "ELSE\n"
            result += self.elseinstruction.printTree(depth + "| ")
        return result

    @addToClass(AST.While_instr)
    def printTree(self, depth):
        return depth + "WHILE\n" +  self.condition.printTree(depth + "| ") + self.instruction.printTree(depth + "| ")


    @addToClass(AST.Repeat_instr)
    def printTree(self, depth):
        result = depth + "REPEAT\n"
        result += self.instructions.printTree(depth + "| ")
        result += depth + "| "
        result += "UNTIL\n"
        result += self.condition.printTree(depth + "| ")
        return result

    @addToClass(AST.Return_instr)
    def printTree(self, depth):
        return depth + "RETURN\n" + self.expression.printTree(depth + "| ")

    @addToClass(AST.Continue_instr)
    def printTree(self, depth):
        return depth + "CONTINUE\n"

    @addToClass(AST.Break_instr)
    def printTree(self, depth):
        return depth + "BREAK\n"

    @addToClass(AST.Compound_instr)
    def printTree(self, depth):
        result = ""
        if self.declarations:
            if self.declarations.printTree(depth):
                result += depth +"DECL\n"
                result += self.declarations.printTree(depth)
        result += self.instructions.printTree(depth)
        return result

    @addToClass(AST.Condition)
    def printTree(self, depth):
        return self.expression.printTree(depth)

    @addToClass(AST.Integer)
    def printTree(self, depth):
        return depth + str(self.value) + "\n"

    @addToClass(AST.Float)
    def printTree(self, depth):
        return depth + str(self.value) + "\n"

    @addToClass(AST.String)
    def printTree(self, depth):
        return depth + str(self.value) + "\n"

    @addToClass(AST.Expression)
    def printTree(self, depth):
        result = depth
        result += self.oper + "\n"
        result += self.left.printTree(depth + "| ")
        result += self.right.printTree(depth + "| ")
        return result

    @addToClass(AST.SingleExpression)
    def printTree(self, depth):
        if isinstance(self.id, str):
            return depth + self.id+"\n"
        else:
            return self.id.printTree(depth)


    @addToClass(AST.Funcall)
    def printTree(self, depth):
        result = ""
        result += depth + "FUNCALL\n"
        result += depth + "| " + self.id + "\n"
        result += self.expr_list_or_empty.printTree(depth + "| ")
        return result


    @addToClass(AST.ExprNested)
    def printTree(self, depth):
        return self.expression.printTree(depth)


    @addToClass(AST.Expr_list_or_empty)
    def printTree(self, depth):
        result = ""
        for elem in self.expr_list:
            result += elem.printTree(depth)
        return result


    @addToClass(AST.Fundefs)
    def printTree(self, depth):
        result = ""
        for elem in self.fundefs:
            result += elem.printTree(depth)
        return result

    @addToClass(AST.Fundef)
    def printTree(self, depth):
        result = depth + "| " + self.id +"\n" +  depth + "| "
        result += "RET " + self.type + "\n" + self.arg_list.printTree(depth + "| ")
        result += self.compound_instr.printTree(depth + "| ")
        return result


    @addToClass(AST.Args_list)
    def printTree(self, depth):
        result = ""
        for elem in self.args_list:
            result += elem.printTree(depth)
        return result

    @addToClass(AST.Arg)
    def printTree(self, depth):
        return depth + "ARG " + self.id + "\n"
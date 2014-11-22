#!/usr/bin/python

from scanner import Scanner
import AST


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print('At end of input')

    def p_program(self, p):
        """program : declarations fundefs instructions"""
        p[0] = AST.Program(p.lineno(1), p[1], p[2], p[3])

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if len(p) == 3:
            p[1].declarations.append(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.Declarations()

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        if len(p) == 3:
            p[0] = AST.Declaration(p.lineno(1), p[1])
        else:
            p[0] = AST.Declaration(p.lineno(1), p[1], p[2])

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 2:
            x = AST.Inits()
            x.inits.append(p[1])
            p[0] = x
        else:
            p[1].inits.append(p[3])
            p[0] = p[1]


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = AST.Init(p.lineno(1), p[1], p[3])


    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 2:
            x = AST.Instructions()
            x.instructions.append(p[1])
            p[0] = x
        elif p[1] is None:
            x = AST.Instructions()
            x.instructions.append(p[2])
            p[0] = x
        else:
            p[1].instructions.append(p[2])
            p[0] = p[1]

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""
        p[0] = p[1]


    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'
                       | PRINT error ';' """
        p[0] = AST.Print_instr(p.lineno(1), p[2])


    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.Labeled_instr(p.lineno(1), p[1], p[3])


    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.Assignment(p.lineno(1), p[1], p[3])


    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        if len(p) == 8:
            p[0] = AST.Choice_instr(p.lineno(1), p[3], p[5], p[7])
        else:
            p[0] = AST.Choice_instr(p.lineno(1), p[3], p[5])


    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.While_instr(p.lineno(1), p[3], p[5])


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.Repeat_instr(p.lineno(1), p[2], p[4])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.Return_instr(p.lineno(1), p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.Continue_instr(p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.Break_instr(p.lineno(1))


    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}' """
        p[0] = AST.Compound_instr(p.lineno(1), p[2], p[3])


    def p_condition(self, p):
        """condition : expression"""
        p[0] = AST.Condition(p.lineno(1), p[1])


    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        if isinstance(p[1], int):
            p[0] = AST.Integer(p.lineno(1), p[1])
            return
        if isinstance(p[1], float):
            p[0] = AST.Float(p.lineno(1), p[1])
            return
        p[0] = AST.String(p.lineno(1), p[1])


    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        if len(p) == 2:
            p[0] = AST.SingleExpression(p.lineno(1), p[1])
            return
        if p[1] == '(' and p[3] == ')':
            p[0] = AST.ExprNested(p.lineno(1), p[2])
            return
        if p[2] == '(' and p[4] == ')':
            p[0] = AST.Funcall(p.lineno(1), p[1], p[3])
            return
        p[0] = AST.Expression(p.lineno(1), p[1], p[2], p[3])


    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 1:
            p[0] = AST.Expr_list_or_empty(p.lineno(1))
        else:
            p[0] = p[1]

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) ==4:
            p[1].expr_list.append(p[3])
            p[0] = p[1]
        else:
            x = AST.Expr_list_or_empty(p.lineno(1))
            x.expr_list.append(p[1])
            p[0] = x


    def p_fundefs(self, p):
        """fundefs : fundef fundefs
                   |  """
        if len(p) == 1:
            p[0] = AST.Fundefs(p.lineno(0))
        else:
            p[2].fundefs.append(p[1])
            p[0] = p[2]

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.Fundef(p.lineno(1), p[1], p[2], p[4], p[6])


    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 1:
            p[0] = AST.Args_list(p.lineno(1))
        else:
            p[0] = p[1]

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) == 2:
            x = AST.Args_list(p.lineno(1))
            x.args_list.append(p[1])
            p[0] = x
        else:
            p[1].args_list.append(p[3])
            p[0] = p[1]

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.Arg(p.lineno(1), p[1], p[2])




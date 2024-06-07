from Utils import tokens

class ASTNode:
    pass


class VarDeclNode(ASTNode):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __str__(self):
        if self.var_name == tokens.TT_STRING:
            return
        return f"VarDeclNode(var_name='{self.var_name}', value={self.value})"

class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"PrintNode(expression={self.expression})"

class IfNode(ASTNode):
    def __init__(self, condition, if_body, else_node=None, elif_nodes=None):
        self.condition = condition
        self.if_body = if_body
        self.elif_nodes = elif_nodes
        self.else_node = else_node

    def __str__(self):
        return f"IfNode(condition={self.condition}, if_body={self.if_body}, else_body={self.else_node},  elif_nodes={self.elif_nodes})"

class ElifNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"ElifNode(condition={self.condition}, body={self.body})"
    
class ElseNode(ASTNode):
    def __init__(self, body):
        self.body = body

    def __str__(self):
        return f"ElseNode(body={self.body})"

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"WhileNode(condition={self.condition}, body={self.body})"

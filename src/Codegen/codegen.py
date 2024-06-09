from Parser.astNode import *

class CodeGen:
    def __init__(self, parsed_code) -> None:
        self.parsed_code = parsed_code

    def get_executable_code(self):
        code_lines = [self.generate_code(node, 0) for node in self.parsed_code]
        return "\n".join(code_lines)

    def generate_code(self, node, indent_level):
        if isinstance(node, VarDeclNode):
            return self.generate_var_decl(node, indent_level)
        elif isinstance(node, PrintNode):
            return self.generate_print(node, indent_level)
        elif isinstance(node, IfNode):
            return self.generate_if(node, indent_level)
        elif isinstance(node, ElseNode):
            return self.generate_else(node, indent_level)
        elif isinstance(node, ElifNode):
            return self.generate_elif(node, indent_level)
        elif isinstance(node, WhileNode):
            return self.generate_while(node, indent_level)
        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def indent(self, code, indent_level):
        indentation = " " * 4 * indent_level
        return "\n".join(indentation + line for line in code.split("\n"))

    def generate_var_decl(self, node, indent_level):
        code = f"{node.var_name} = {node.value}"
        return self.indent(code, indent_level)

    def generate_print(self, node, indent_level):
        code = f"print({node.expression})"
        return self.indent(code, indent_level)

    def generate_if(self, node, indent_level):
        condition = node.condition
        if_body = "\n".join(self.generate_code(stmt, indent_level + 1) for stmt in node.if_body)
        elif_nodes = "\n".join(self.generate_code(stmt, indent_level) for stmt in node.elif_nodes)
        else_body = self.generate_code(node.else_node, indent_level) if node.else_node else ""
        
        code = f"if {condition}:\n{if_body}"
        code = self.indent(code, indent_level)
        if elif_nodes:
            code += f"\n{elif_nodes}"
        if else_body:
            code += f"\n{else_body}"

        return code
    
    def generate_elif(self, node, indent_level):
        condition = node.condition
        elif_body = "\n".join(self.generate_code(stmt, indent_level + 1) for stmt in node.body)
        code = f"elif {condition}:\n{elif_body}"
        return self.indent(code, indent_level)
    
    def generate_else(self, node, indent_level):
        else_body = "\n".join(self.generate_code(stmt, indent_level + 1) for stmt in node.body)
        code = f"else:\n{else_body}"
        return self.indent(code, indent_level)
    
    def generate_while(self, node, indent_level):
        condition = node.condition
        while_body = "\n".join(self.generate_code(stmt, indent_level + 1) for stmt in node.body)
        code = f"while {condition}:\n{while_body}"
        return self.indent(code, indent_level)

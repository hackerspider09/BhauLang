
'''
function codeGen(node){
    switch (node.type) {
        case 'Program':
            return node.body.map(codeGen).join('\n');
        case 'Declaration': return `const ${node.name} = ${node.value}`;
        case 'Print' : return `console.log(${node.expression})`;

        default:
            break;
    }
}
'''
from Parser.astNode import *

class CodeGen:
    def __init__(self,parsed_code) -> None:
        self.parsed_code = parsed_code

    def get_executable_code(self):
        code_lines = [self.generate_code(node) for node in self.parsed_code]
        return "\n".join(code_lines)

    def generate_code(self, node):
        if isinstance(node, VarDeclNode):
            return self.generate_var_decl(node)
        elif isinstance(node, PrintNode):
            return self.generate_print(node)
        elif isinstance(node, IfNode):
            return self.generate_if(node)
        elif isinstance(node, ElseNode):
            return self.generate_else(node)
        elif isinstance(node, ElifNode):
            return self.generate_elif(node)
        elif isinstance(node, WhileNode):
            return self.generate_while(node)
        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def generate_var_decl(self, node):
        return f"{node.var_name} = {node.value}"

    def generate_print(self, node):
        return f"print({node.expression})"

    def generate_if(self, node):
        condition = node.condition
        if_body = "\n    ".join(self.generate_code(stmt) for stmt in node.if_body)
        else_body = ""
        elif_nodes = "\n".join(self.generate_code(stmt) for stmt in node.elif_nodes)


        if (node.else_node):
            else_body = self.generate_code(node.else_node) 
        return f"if {condition}:\n    {if_body}\n{elif_nodes}{else_body}"
    
    def generate_elif(self, node):
        condition = node.condition
        elif_body = "\n    ".join(self.generate_code(stmt) for stmt in node.body)
        # print("hello => ",else_body)
        return f"elif {condition}:\n    {elif_body}"
    
    def generate_else(self, node):
        else_body = "\n    ".join(self.generate_code(stmt) for stmt in node.body)
        # print("hello => ",else_body)
        return f"else :\n    {else_body}"
    
    def generate_while(self, node):
        condition = node.condition
        while_body = "\n    ".join(self.generate_code(stmt) for stmt in node.body)
        # print("hello => ",else_body)
        return f"while {condition}:\n    {while_body}"
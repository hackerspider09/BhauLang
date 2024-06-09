from Utils import constants,keywords,tokens
import re
from Parser.astNode import VarDeclNode,PrintNode,IfNode,ElifNode,WhileNode,ElseNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        statements = []
        while self.current_token is not None and self.current_token.TYPE != tokens.TT_EOF:
            statement,error = self.parse_statement()
            if error is not None:
                print("Error in parser => ",error)
            if statement is not None:
                statements.append(statement)
            self.advance()

        return statements

    def parse_statement(self):
        if self.current_token.TYPE == tokens.TT_KEYWORD:
            if self.current_token.VALUE == keywords.KEYWORDS_DICT['declaration']:
                return self.parse_var_decl()  # Parse variable declaration
            elif self.current_token.VALUE == keywords.KEYWORDS_DICT['print']:
                return self.parse_print_statement()  # Parse print statement
            elif self.current_token.VALUE == keywords.KEYWORDS_DICT['if'] :
                return self.parse_if_statement()  # Parse if  statement
            elif self.current_token.VALUE == keywords.KEYWORDS_DICT['else'] :
                return self.parse_else_statement()  # Parse else statement
            elif self.current_token.VALUE == keywords.KEYWORDS_DICT['elif'] :
                return self.parse_elif_statement()  # Parse elif statement
            elif self.current_token.VALUE == keywords.KEYWORDS_DICT['while'] :
                return self.parse_while_statement()  # Parse elif statement
        elif self.current_token.TYPE == tokens.TT_IDENTIFIER:
            return self.parse_iden_statement()
        return None,None

    def parse_iden_statement(self):

        var_name = self.current_token.VALUE

        self.advance()
        if (self.current_token.TYPE == tokens.TT_OPERATOR and self.current_token.VALUE == "=" ):
            self.advance()  
            expression = ""

            while(self.current_token is not None and self.current_token.TYPE != tokens.TT_EOF and self.current_token.TYPE != tokens.TT_NEWLINE):
                # expression += self.current_token.VALUE
                expression += self.get_string_with_quote(self.current_token)
                self.advance()
            return VarDeclNode(var_name,expression),None
        return None," = necessory"

    def parse_var_decl(self):
        self.advance()

        var_name = self.current_token.VALUE

        self.advance()
        if (self.current_token.TYPE == tokens.TT_OPERATOR and self.current_token.VALUE == "=" ):
            self.advance()  
            expression = ""

            while(self.current_token is not None and self.current_token.TYPE != tokens.TT_EOF and self.current_token.TYPE != tokens.TT_NEWLINE):
                # expression += self.current_token.VALUE
                expression += self.get_string_with_quote(self.current_token)
                self.advance()

            return VarDeclNode(var_name,expression),None

        return None," = necessory"

    def parse_print_statement(self):
        expression = ""
        ending_char = [tokens.TT_EOF,tokens.TT_NEWLINE,tokens.TT_COLON]
        self.advance()

        if (self.current_token.TYPE == tokens.TT_LPAREN):
            self.advance()
            right_paran_chance = 1
            while(self.current_token is not None and self.current_token.TYPE not in ending_char ):
                if (right_paran_chance >=1 and self.current_token.TYPE != tokens.TT_RPAREN and self.current_token.TYPE != tokens.TT_LPAREN):
                    expression += self.get_string_with_quote(self.current_token)
                elif(right_paran_chance>1 and self.current_token.TYPE == tokens.TT_RPAREN):
                    expression += self.get_string_with_quote(self.current_token)
                    right_paran_chance -= 1
                elif(self.current_token.TYPE == tokens.TT_LPAREN):
                    expression += self.get_string_with_quote(self.current_token)
                    right_paran_chance += 1
                else:
                    break

                self.advance()

            token =self.current_token
            if(token.TYPE != tokens.TT_RPAREN):
                return None,") necessory"
            
            # self.advance()
            return PrintNode(expression),None

        else:
            return None,"( necessory"
        
    def get_string_with_quote(self,token):
        if(token.TYPE == tokens.TT_STRING):
            return '"'+token.VALUE+'"'
            # return token.VALUE

        # return token.TYPE(token.VALUE)
        return str(token.VALUE)
    
    def parse_if_statement(self):
        self.advance()
        ending_char = [tokens.TT_EOF,tokens.TT_NEWLINE,tokens.TT_COLON]
        if_condition = ""
        if_body = []

        # condition check
        if ( self.current_token.TYPE == tokens.TT_LPAREN):
            self.advance()
            right_paran_chance = 1
            while(self.current_token is not None and self.current_token.TYPE not in ending_char ):
                if (right_paran_chance >=1 and self.current_token.TYPE != tokens.TT_RPAREN and self.current_token.TYPE != tokens.TT_LPAREN):
                    if_condition += self.get_string_with_quote(self.current_token)
                elif(right_paran_chance>1 and self.current_token.TYPE == tokens.TT_RPAREN):
                    if_condition += self.get_string_with_quote(self.current_token)
                    right_paran_chance -= 1
                elif(self.current_token.TYPE == tokens.TT_LPAREN):
                    if_condition += self.get_string_with_quote(self.current_token)
                    right_paran_chance += 1
                else:
                    break

                self.advance()
            
            # if ) is not present error
            if(self.current_token.TYPE != tokens.TT_RPAREN):
                return None,") necessory"
            
            # other wise go below for body generation
            self.advance()
            while(self.current_token.TYPE==tokens.TT_NEWLINE):
                self.advance()
            

            if self.current_token.TYPE == tokens.TT_LBRACE:
                self.advance()
                while self.current_token is not None and self.current_token.TYPE != tokens.TT_RBRACE:
                    statement,error = self.parse_statement()
                    if error is not None:
                        print("Error in parser => ",error)
                    if statement is not None:
                        if_body.append(statement)
                    self.advance()

                
                
                # Check if the closing curly brace is present
                if self.current_token.TYPE != tokens.TT_RBRACE:
                    return None, "} necessary"
                self.advance()

                while(self.current_token.TYPE==tokens.TT_NEWLINE):
                    self.advance()


                # Check for else if block 
                elif_nodes = []
                if(self.current_token.VALUE == keywords.KEYWORDS_DICT['elif']):
                    while(self.current_token.VALUE == keywords.KEYWORDS_DICT['elif'] ):
                        elif_node , elif_node_error = self.parse_statement()
                        
                        if(elif_node_error is None):
                            elif_nodes.append(elif_node)

                            
                

                # Check for else block 
                else_node, else_node_error = None,None
                if(self.current_token.VALUE == keywords.KEYWORDS_DICT['else']):
                    else_node , else_node_error = self.parse_statement()

                    if(else_node_error):
                        else_node = None



                return IfNode(if_condition, if_body, else_node, elif_nodes), None
            else:
                return None, "{ necessary"

        else:
            return None,"( necessory"
        
    def parse_else_statement(self):
        self.advance()
        ending_char = [tokens.TT_EOF,tokens.TT_NEWLINE,tokens.TT_COLON]
        else_body = []

        if self.current_token.TYPE == tokens.TT_LBRACE:
            self.advance()
            while self.current_token is not None and self.current_token.TYPE != tokens.TT_RBRACE:
                statement,error = self.parse_statement()
                if error is not None:
                    print("Error in parser => ",error)
                if statement is not None:
                    else_body.append(statement)
                self.advance()
            
            
            # Check if the closing curly brace is present
            if self.current_token.TYPE != tokens.TT_RBRACE:
                return None, "} necessary"
            self.advance()
            
            return ElseNode(else_body), None
        else:
            return None, "{ necessary"
        
    def parse_elif_statement(self):
        self.advance()
        ending_char = [tokens.TT_EOF,tokens.TT_NEWLINE,tokens.TT_COLON]
        elif_condition = ""
        elif_body = []

        # condition check
        if ( self.current_token.TYPE == tokens.TT_LPAREN):
            self.advance()
            right_paran_chance = 1
            while(self.current_token is not None and self.current_token.TYPE not in ending_char ):
                if (right_paran_chance >=1 and self.current_token.TYPE != tokens.TT_RPAREN and self.current_token.TYPE != tokens.TT_LPAREN):
                    elif_condition += self.get_string_with_quote(self.current_token)
                elif(right_paran_chance>1 and self.current_token.TYPE == tokens.TT_RPAREN):
                    elif_condition += self.get_string_with_quote(self.current_token)
                    right_paran_chance -= 1
                elif(self.current_token.TYPE == tokens.TT_LPAREN):
                    elif_condition += self.get_string_with_quote(self.current_token)
                    right_paran_chance += 1
                else:
                    break

                self.advance()
            
            # if ) is not present error
            if(self.current_token.TYPE != tokens.TT_RPAREN):
                return None,") necessory"
            
            # other wise go below for body generation
            self.advance()

            if self.current_token.TYPE == tokens.TT_LBRACE:
                self.advance()
                while self.current_token is not None and self.current_token.TYPE != tokens.TT_RBRACE:
                    statement,error = self.parse_statement()
                    if error is not None:
                        print("Error in parser => ",error)
                    if statement is not None:
                        elif_body.append(statement)
                    self.advance()

                
                
                # Check if the closing curly brace is present
                if self.current_token.TYPE != tokens.TT_RBRACE:
                    return None, "} necessary"
                self.advance()


                return ElifNode(elif_condition, elif_body), None
            else:
                return None, "{ necessary"

        else:
            return None,"( necessory"


    def parse_while_statement(self):
        self.advance()
        ending_char = [tokens.TT_EOF,tokens.TT_NEWLINE,tokens.TT_COLON]
        while_condition = ""
        while_body = []

        # condition check
        if ( self.current_token.TYPE == tokens.TT_LPAREN):
            self.advance()
            right_paran_chance = 1
            while(self.current_token is not None and self.current_token.TYPE not in ending_char ):
                if (right_paran_chance >=1 and self.current_token.TYPE != tokens.TT_RPAREN and self.current_token.TYPE != tokens.TT_LPAREN):
                    while_condition += self.get_string_with_quote(self.current_token)
                elif(right_paran_chance>1 and self.current_token.TYPE == tokens.TT_RPAREN):
                    while_condition += self.get_string_with_quote(self.current_token)
                    right_paran_chance -= 1
                elif(self.current_token.TYPE == tokens.TT_LPAREN):
                    while_condition += self.get_string_with_quote(self.current_token)
                    right_paran_chance += 1
                else:
                    break

                self.advance()
            
            # if ) is not present error
            if(self.current_token.TYPE != tokens.TT_RPAREN):
                return None,") necessory"
            
            # other wise go below for body generation
            self.advance()

            if self.current_token.TYPE == tokens.TT_LBRACE:
                self.advance()
                while self.current_token is not None and self.current_token.TYPE != tokens.TT_RBRACE:
                    statement,error = self.parse_statement()
                    if error is not None:
                        print("Error in parser => ",error)
                    if statement is not None:
                        while_body.append(statement)
                    self.advance()

                
                
                # Check if the closing curly brace is present
                if self.current_token.TYPE != tokens.TT_RBRACE:
                    return None, "} necessary"
                self.advance()
                
                return WhileNode(while_condition, while_body), None
            else:
                return None, "{ necessary"

        else:
            return None,"( necessory"

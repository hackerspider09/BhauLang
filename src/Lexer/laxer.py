from Utils import constants,keywords,tokens
import re
from Lexer.token import Token


class Laxer:
    def __init__(self,code) -> None:
        self.tokens = []
        self.cursor = -1
        self.current_char = None
        self.user_code = code
        self.keywords = sorted(keywords.KEYWORDS, key=len, reverse=True)  # Sort keywords by length in descending order to ensure longer key check 1st
        self.cursor_advance()

    def cursor_advance(self,increment=1):
        self.cursor += increment
        self.current_char = self.user_code[self.cursor] if self.cursor < len(self.user_code) else None
    
    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.cursor_advance()
        self.cursor_advance()

    def create_token(self):
        # print("create token")
        while(self.current_char != None):

            if(self.current_char == "\n"):
                self.tokens.append(Token(tokens.TT_NEWLINE))
                self.cursor_advance()
                continue

            # Ignore white space
            if(self.current_char.isspace()):
                self.cursor_advance()
                continue
            # Ignore comment
            if(self.current_char == '#'):
                self.skip_comment()
                continue

            # Check for keyword 
            char_token = self.match_keywords()
            if char_token:
                self.tokens.append(char_token)
                continue

            # Remaining checks
            char_token = self.get_token()

            if char_token is None:
                # breack nanter
                continue

            self.tokens.append(char_token)

        self.tokens.append(Token(tokens.TT_EOF))
        return self.tokens

    def check_digit(self):
        pass

    def check_alpha(self,char):
        return re.match(r'[a-zA-Z]', char) is not None
    
    def check_alpha_num(self,char):
        return re.match(r'[a-zA-Z0-9]', char) is not None
    
    def check_number(self,num):
        return re.match(r'[0-9]', num) is not None
    
    def match_keywords(self):
        for keyword in self.keywords:
            length = len(keyword)
            if self.user_code[self.cursor:self.cursor+length] == keyword:
                self.cursor_advance(length)

                return Token(tokens.TT_KEYWORD, keyword)
        return None
    
    def get_operator(self):

        if (self.current_char in constants.ARITHMETIC_OPERATORS ):
            return tokens.TT_OPERATOR , self.current_char
        
        # 2nd param is None but for parser i have change this
        if (self.current_char == "(" ):
            # return tokens.TT_LPAREN ,None
            return tokens.TT_LPAREN ,self.current_char
        if (self.current_char == ")" ):
            return tokens.TT_RPAREN , self.current_char
        if (self.current_char == "{" ):
            # return tokens.TT_LPAREN ,None
            return tokens.TT_LBRACE ,self.current_char
        if (self.current_char == "}" ):
            return tokens.TT_RBRACE , self.current_char
        if (self.current_char == ":" ):
            return tokens.TT_COLON , self.current_char
        if (self.current_char == "=" ):
            return tokens.TT_OPERATOR , self.current_char
        
        
        
        
        return None, None
        

    

    def get_token(self):

        token_type,token_char = self.get_operator()
        if token_type:
            self.cursor_advance()
            return Token(token_type, token_char if token_type is not None else token_char)
        

        # Check for identifier
        if(self.check_alpha(self.current_char)):
            word = ""

            while self.current_char is not None and self.check_alpha_num(self.current_char):
                word += self.current_char
                self.cursor_advance()
            

            if word in constants.BOOLEAN_VALUE:
                return Token(tokens.TT_BOOL, word)
                
            return Token(tokens.TT_IDENTIFIER, word)
            
        # Check for number
        if(self.check_number(self.current_char)):
            number = ""
            isFloat = False

            while self.current_char != None and self.current_char  in constants.DIGITS + ".":
                if (self.current_char == "."):
                    if isFloat:
                        break
                    isFloat = True
                
                number += self.current_char
                self.cursor_advance()

            # self.cursor_advance()

            if isFloat:
                return Token(tokens.TT_FLOAT, float(number))
            else:
                return Token(tokens.TT_INT, number)
            
        # Check for string
        if (self.current_char == '"'):
            word = ""

            self.cursor_advance()
            while self.current_char is not None and self.current_char !=  '"':
                word += self.current_char
                self.cursor_advance()
            
            self.cursor_advance()

            return Token(tokens.TT_STRING, word)
        
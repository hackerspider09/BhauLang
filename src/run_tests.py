import os
import sys
from Lexer import Laxer
from Parser import Parser
from Codegen import CodeGen

def run_custom_lang(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

        # Split the code into lines and filter out blank lines
        lines = [line.strip() for line in code.splitlines() if line.strip()]
        # Join the non-blank lines back together
        code = '\n'.join(lines)
        
        lexer = Laxer(code)
        tokens = lexer.create_token()

        parser = Parser(tokens)
        ast = parser.parse()
        
        codegen = CodeGen(ast)
        
        executable_code = codegen.get_executable_code()
        
        return executable_code


def main(DEBUG=False):
    print("************Running Tests***************")
    test_folder = './Tests'
    for test_file in os.listdir(test_folder):
        if test_file.endswith('.bhau'):
            print("######################################")
            print(f"\nRunning test: {test_file}")
            
            file_path = os.path.join(test_folder, test_file)
            executable_code = run_custom_lang(file_path)
            if executable_code:
                if(DEBUG):
                    print("\nGenerated Python code:\n")
                    print(executable_code)
                print("\nExecution Result:\n")
                exec(executable_code)

            print("######################################")

if __name__ == "__main__":
    main(False)

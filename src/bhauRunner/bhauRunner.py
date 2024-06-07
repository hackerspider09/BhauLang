import sys
from Lexer import Laxer
from Parser import Parser
from Codegen import CodeGen

def main():
    if len(sys.argv) != 2:
        print("Usage: bhau file.bhau")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        code = file.read()

    lexer = Laxer(code)
    tokens = lexer.create_token()

    parser = Parser(tokens)
    parsed_code = parser.parse()

    code_generator = CodeGen(parsed_code)
    executable_code = code_generator.get_executable_code()

    exec(executable_code)

if __name__ == "__main__":
    main()

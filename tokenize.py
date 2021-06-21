import re
class Tokenize:
    # GET ALL TOKENS FROM FILE JACK GIVEN 
    regex = re.compile('".*"|[a-zA-Z_]+[a-zA-Z0-9_]*|[0-9]+|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|<|>|=|~|&]')

    indentifier = "[a-zA-Z_]+[a-zA-Z0-9_]*"
    integer = "[0-9]+"
    string = '".*"'
    symbols = "|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|<|>|=|~]"
    keywords = [
        "class", "constructor", "function", "method", "field", "static",
        "var", "int", "char", "boolean", "void", "true", "false", "null",
        "this", "let", "do", "if", "else", "while", "return"
    ]
    operators = [
        '+', '-', '*', '/',
        '&', '|', '<', '>', '='
    ]

    KEYWORD = "keyword"
    IDENTIFIER = "identifier"
    INTEGER = "integerConstant"
    STRING = "stringConstant"
    SYMBOL = "symbol"

    def __init__(self, filePath):
        self.file = open(filePath, "r").read()
        self.tokens = self.regex.findall(self.file)
        self.tokenIndex = 0

    def hasMoreTokens(self):
        #print(self.getToken())
        try:
            return self.tokenIndex <= len(self.tokens) - 1
        except error:
            print("hasMoreTokens exception ", error, " on line ", self.tokenIndex)


    def advance(self):
        if (self.hasMoreTokens()):
            self.tokenIndex += 1

    def getToken(self):
        try:
            return self.replace(self.tokens[self.tokenIndex])
        except error:
            print("getToken exception ", error, " on line ", self.tokenIndex)


    def tokenType(self):
        try:
            token = self.getToken()
            if (re.match(self.indentifier, token)):
                if (token in self.keywords):
                    return self.KEYWORD
                else:
                    return self.IDENTIFIER
            elif (re.match(self.integer, token)):
                return self.INTEGER
            elif (re.match(self.string, token)):
                return self.STRING
            elif (re.match(self.symbols, token)):
                return self.SYMBOL
        except error:
            print("tokenType exception ", error, " on line ", self.tokenIndex)
        
        

    def replace(self, symbol):
        try:
            if (symbol == "<"):
                return "&lt"
            elif (symbol == ">"):
                return "&gt"
            elif (symbol == '"'):
                return "&quot"
            elif (symbol == '&'):
                return "&amp"
            else:
                return symbol
        except error:
            print("replace exception ", error, " on line ", self.tokenIndex)
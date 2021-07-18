import re
class Tokenizer:
    # GET ALL TOKENS FROM FILE JACK GIVEN 
    regex = re.compile('".*"|[a-zA-Z_]+[a-zA-Z0-9_]*|[0-9]+|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|<|>|=|~|&]')

    indentifier = "[a-zA-Z_]+[a-zA-Z0-9_]*"
    integer = "[0-9]+"
    string = '".*"'
    symbols = "|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|<|>|=|~]"
    keywords = [
        "class", "constructor", "function", "method", "field", "static",
        "var", "int", "char", "boolean", "void", "true", "false", "null",
        "this", "let", "do", "if", "else", "while", "return, new"
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
        #print("Tokens")
        print(self.tokens)
        self.tokenIndex = 0
        self.doc = open('tokens.xml', 'w+')

    def hasMoreTokens(self):
        print("has " + str(self.tokenIndex) + " " + str(len(self.tokens) - 1))
        return self.tokenIndex < len(self.tokens) - 1
        

    def advance(self):
        if (self.hasMoreTokens()):
            #print("tokenAdvance ", self.getToken())
            self.tokenIndex += 1

    def getToken(self):
        if(self.tokenIndex <= (len(self.tokens))):
            return self.replace(self.tokens[self.tokenIndex])
       

    def tokenType(self):
        #try:
        token = self.getToken()
        #print("tokentype2 ", token)
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
        #except error:
        #    print("tokenType exception ", error, " on line ", self.tokenIndex)
        

    def replace(self, symbol):
        #try:
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
        #except error:
        #    print("replace exception ", error, " on line ", self.tokenIndex)
    
    def write(self, flag=0, statement=""):
        if(flag == 0):
            token = self.getToken() 
            _type = self.tokenType()
            print("wtoken", token, _type)
            self.doc.writelines("  <{}>{}</{}>\n".format(_type, token,_type))
        if(flag == 1):
            self.doc.writelines("<{}>\n".format(statement))
        if(flag == 2):
            self.doc.writelines("</{}>\n".format(statement))


#a = Tokenizer("main.jack")
#while(a.hasMoreTokens()):
#    print("Token ", a.getToken(), " Type", a.tokenType())
#    a.advance()
from tokenize import Tokenizer
import re

class Parser:
    
    def __init__(self, _file):
        self.tokenizer = Tokenizer(_file)
        self.doc = open('tokens.xml', 'w+')
    
    def compile(self):
        self.compileClass()
    
    def writeStatement(self, statement, flag):
        if(flag):
            self.doc.writelines("<{}>\n".format(statement))
        else:
            self.doc.writelines("</{}>\n".format(statement))

    #Compiles a complete class.
    def compileClass(self):
        self.writeStatement("class", 1)
        print("token class ", self.tokenizer.getToken())
        self.tokenizer.write()
        self.tokenizer.advance() # class name (identifier)
        print("class name ", self.tokenizer.getToken())
        self.tokenizer.write()
        self.tokenizer.advance()#open key
        print("opened key ", self.tokenizer.getToken())
        self.tokenizer.write()

        self.tokenizer.advance()
        while (self.tokenizer.getToken() in ["static", "field"]):
            self.compileClassVarDec()

        while (self.tokenizer.getToken() in ["method", "constructor", "function"]):
            self.compileSubroutineDec()

        self.tokenizer.advance() #closed key
        self.tokenizer.write()
        print("closed key ", self.tokenizer.getToken())
        self.writeStatement("class", 0)

    #Compiles a static declaration or a field declaration.
    def compileClassVarDec(self):
        #self.writeStatement("varStatement", 1)
        self.tokenizer.advance() #static or field
        self.tokenizer.write()
        #print("after static or field ", self.tokenizer.getToken())
        self.tokenizer.advance() #type
        #print("type in class var dec ", self.tokenizer.getToken())
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("1: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))

        self.tokenizer.advance() #type
        self.tokenizer.write()

        while self.tokenizer.getToken() != ";":
            self.tokenizer.advance()
            self.tokenizer.write()
            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception("2: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
            self.tokenizer.advance()
            self.tokenizer.write()
        
        self.tokenizer.advance()
        self.tokenizer.write()
        #self.writeStatement("varStatement", 0)

    #Compiles a complete method, function, or constructor.
    def compileSubroutineDec(self):
        #self.writeStatement("compileSubroutineDec", 1)
        self.tokenizer.advance() #method, constructor, function
        self.tokenizer.write()
        self.tokenizer.advance() #type
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("3: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
    
        self.tokenizer.advance()  # identifier
        self.tokenizer.write()

        self.tokenizer.advance()  # (
        self.tokenizer.write()

        self.compileParameterList()

        self.tokenizer.advance()  # )
        self.tokenizer.write()

        self.tokenizer.advance()  # {
        self.tokenizer.write()

        while self.tokenizer.getToken() == "var":
            self.compileVarDec()

        self.compileStatements()

        self.tokenizer.advance()  # }
        self.tokenizer.write()
        #self.writeStatement("compileSubroutineDec", 0)
    
    #Compiles a (possibly empty) parameter list, not including the enclosing "()" .
    def compileParameterList(self):
        #self.writeStatement("compileParameterList", 1)

        if(self.tokenizer.getToken() == ")"):
            return

        self.tokenizer.advance()  # type
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("3: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
        
        self.tokenizer.advance()  # identifier
        self.tokenizer.write()

        #VERIFICAR A LOGICA DESSE WHILE, TA ESTRANHO    
        while self.tokenizer.getToken() != ")":
            self.tokenizer.advance()  # ,
            self.tokenizer.write()
            self.tokenizer.advance()  #
            self.tokenizer.write()
            self.tokenizer.advance()  #
            self.tokenizer.write()
    
        #self.writeStatement("compileParameterList", 0)
    
    #Compiles a var declaration.
    def compileVarDec(self):
        #self.writeStatement("compileVarDec", 1)
        self.tokenizer.advance()  #var
        self.tokenizer.write()
        self.tokenizer.advance()  # type
        self.tokenizer.write()
        
        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("3: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
        
        self.tokenizer.advance()  # identifier
        self.tokenizer.write()

        while self.tokenizer.getToken() != ";":
            self.tokenizer.advance()  # t,
            self.tokenizer.write()
            if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception("4: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
            self.tokenizer.advance()  #
            self.tokenizer.write()    
        self.tokenizer.advance()  #
        self.tokenizer.write()
        #self.writeStatement("compileVarDec", 0)
    
    #Compiles a sequence of statements, not including the enclosing ‘‘{}’’.
    def compileStatements(self):
        #self.writeStatement("compileStatements", 1)
        while self.tokenizer.getToken() in ["return", "let", "do", "if", "while"]:
            if(self.tokenizer.getToken() == "if"):
                self.compileIf()
            elif (self.tokenizer.getToken() == "while"):
                self.compileWhile()
            elif (self.tokenizer.getToken() == "let"):
                self.compileLet()
            elif (self.tokenizer.getToken() == "do"):
                self.compileDo()
            elif (self.tokenizer.getToken() == "return"):
                self.compileReturn()
        #self.writeStatement("compileStatements", 0)

    #Compiles an if statement, possibly with a trailing else clause.
    def compileIf(self):
        self.writeStatement("ifStatement", 1)

        self.tokenizer.advance()  # if
        self.tokenizer.write()
        self.tokenizer.advance()  # (
        self.tokenizer.write()
        self.compileExpression()

        self.tokenizer.advance()  # )
        self.tokenizer.write()
        self.tokenizer.advance()  # {
        self.tokenizer.write()
        self.compileStatements()

        self.tokenizer.advance()  # }
        self.tokenizer.write()

        if(self.tokenizer.getToken() == "else"):
            self.tokenizer.advance() # else
            self.tokenizer.write()
            self.tokenizer.advance() # {
            self.tokenizer.write()
            self.compileStatements()
            self.tokenizer.advance() # }
            self.tokenizer.write()

        self.writeStatement("ifStatement", 0)

    def compileWhile(self):
        self.writeStatement("whileStatement", 1)
        self.tokenizer.advance()  # while
        self.tokenizer.write()
        self.tokenizer.advance()  # (
        self.tokenizer.write()
        self.compileExpression()
        self.tokenizer.advance()  # )
        self.tokenizer.write()
        self.tokenizer.advance()  # {
        self.tokenizer.write()
        self.compileStatements()
        self.tokenizer.advance()  # }
        self.tokenizer.write()
        self.writeStatement("whileStatement", 0)

    def compileLet(self):
        self.writeStatement("letStatement", 1)
        self.tokenizer.advance()  # let
        self.tokenizer.write()
        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("5: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
        
        self.tokenizer.advance()  # identifier
        self.tokenizer.write()
        if(self.tokenizer.getToken() == "["):
            self.tokenizer.advance() # [
            self.tokenizer.write()
            self.compileExpression()
            self.tokenizer.advance()  # ]
            self.tokenizer.write()
            self.tokenizer.advance()  # =
            self.tokenizer.write()
            self.compileExpression()
        else:
            self.tokenizer.advance()  # =
            self.tokenizer.write()
            self.compileExpression()

        self.tokenizer.advance()  # ;
        self.tokenizer.write()
        self.writeStatement("letStatement", 0)
        return True
   
    def compileReturn(self):
        #self.writeStatement("returnStatement", 1)
        self.tokenizer.advance()  # return
        self.tokenizer.write()
        if(self.tokenizer.getToken() != ";"):
            self.compileExpression()
        self.tokenizer.advance()  # ;
        self.tokenizer.write()
        #self.writeStatement("returnStatement", 0)
    
    def compileDo(self):
        #self.writeStatement("doStatement", 1)
        self.tokenizer.advance()  # do
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("5: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))

        self.tokenizer.advance()  # identifier
        self.tokenizer.write()
        self.tokenizer.advance()  # ;
        self.tokenizer.write()
        #self.writeStatement("doStatement", 0)

    def compileExpression(self):
        self.writeStatement("expression", 1)
        self.compileTerm()
        #print("operator {}".format(self.tokenizer.getToken()))

        while (self.tokenizer.getToken() in ['+', '-' , '&amp', '|', '&lt', '&gt', '=' ]):
            self.tokenizer.advance()  # ,
            self.tokenizer.write()
            self.compileTerm()
        
        self.writeStatement("expression", 0)
        return True


    def compileExpressionList(self):
        #self.writeStatement("compileExpressionList", 1)
        len_args = 0
        if(self.tokenizer.getToken() == ")"):
            return len_args

        self.compileExpression()
        len_args = len_args + 1

        while (self.tokenizer.getToken() != ")"):

            self.tokenizer.advance()  #,
            self.tokenizer.write()
            self.compileExpression()
            len_args = len_args + 1

        #self.writeStatement("compileExpressionList", 0)
        return len_args
    
    def compileSubroutineCall(self):
        #self.writeStatement("compileSubroutineCall", 1)

        if(self.tokenizer.getToken() == "."):
            self.tokenizer.advance()  # .
            self.tokenizer.write()
            self.tokenizer.advance()  # identifier
            self.tokenizer.write()

        self.tokenizer.advance()  # (
        self.tokenizer.write()
        self.compileExpressionList()
        self.tokenizer.advance() 
        self.tokenizer.write()

        #self.writeStatement("compileSubroutineCall", 1)


    def compileString(self):
        self.writeStatement("stringStatement", 1)
        self.tokenizer.advance()
        self.tokenizer.write()
        self.writeStatement("stringStatement", 0)
    
    def compileTerm(self):
        #self.writeStatement("compileTerm", 1)

        if(self.tokenizer.tokenType() == self.tokenizer.STRING):
            self.compileString()
        elif(self.tokenizer.tokenType() == self.tokenizer.INTEGER):
            self.tokenizer.advance()  # int
        elif(self.tokenizer.getToken() in ["false", "null", "true"]):
            self.tokenizer.advance()  # keyword
        elif(self.tokenizer.getToken() == "this"):
            self.tokenizer.advance()  # this
        elif(self.tokenizer.getToken() in ["-", "~"]):
            self.tokenizer.advance()  
            self.compileTerm()
        elif(self.tokenizer.getToken() == "("):
            self.tokenizer.advance()  # (
            self.compileExpression()
            self.tokenizer.advance()  # )
        else:
            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception("5: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
            
            self.tokenizer.advance()  # identifier
            self.tokenizer.write()
            if(self.tokenizer.getToken() == "["):
                self.tokenizer.advance()  # [
                self.tokenizer.write()
                self.compileExpression()
                self.tokenizer.advance()  # ]
                self.tokenizer.write()


            elif(self.tokenizer.getToken() in [".", "("]):
                self.compileSubroutineCall()

        #self.writeStatement("compileTerm", 0)



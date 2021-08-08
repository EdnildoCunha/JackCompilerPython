from tokenize import Tokenizer
from symbleTable import SymbleTable
from codeWriter import CodeWriter
import re

class Parser:
    
    def __init__(self, _file):
        self.tokenizer = Tokenizer(_file)
        self.doc = open('tokens.xml', 'w+')
        self.symbolTable = SymbleTable()
        self.className = None

        self.codeWriter = CodeWriter(_file)

        self.if_counter = 0
        self.while_counter = 0

        self.kind_myd = {
            "FIELD" : "THIS",
            "ARG" : "ARG",
            "STATIC" : "STATIC",
            "VAR" : "LOCAL"
        }
        self.operator_myd = {
            '+' : 'ADD',
            '-' : 'SUB',
            '&amp' : 'AND',
            '|' : 'OR',
            '&lt' : 'LT',
            '&gt' : 'GT',
            '=' : 'EQ'
        }
    
    def compile(self):
        self.compileClass()
    
    def writeStatement(self, statement, flag):
        if(flag==1):
            self.doc.writelines("<{}>\n".format(statement))
        else:
            self.doc.writelines("</{}>\n".format(statement))

    #Compiles a complete class.
    def compileClass(self):
        
        flag = True
        if(self.tokenizer.getToken() != "class"):
                print("Esperava class aqui")
                return
        
        self.tokenizer.write(1, "class")
        self.tokenizer.write()#class

        while(self.tokenizer.hasMoreTokens()):
            #self.tokenizer.write()
            self.tokenizer.advance()
            if flag:
                self.className = self.tokenizer.getToken()
                flag = False
            self.tokenizer.write()


            #self.tokenizer.advance()

            while(self.tokenizer.getToken() in ["static", "field"]):
                self.compileClassVarDec()

            while(self.tokenizer.getToken() in ["method", "constructor", "function"]):
                self.compileSubroutineDec()

            #self.tokenizer.advance() #closed key
            #self.tokenizer.write()
            #print("closed key ", self.tokenizer.getToken())
        self.tokenizer.write(2, "class")
        self.codeWriter.close()

    #Compiles a static declaration or a field declaration.
    def compileClassVarDec(self):

        #self.writeStatement("varStatement", 1)
        kind = self.tokenizer.getToken().upper()
        self.tokenizer.write(1, "varStatement")

        self.tokenizer.advance() #static or field
        tipo = self.tokenizer.getToken()
        self.tokenizer.write()

        #print("after static or field ", self.tokenizer.getToken())
        
        self.tokenizer.advance() #type
        #print("type in class var dec ", self.tokenizer.getToken())
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("1: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))

        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)

        self.tokenizer.advance() #type
        self.tokenizer.write()

        while self.tokenizer.getToken() != ";":
            self.tokenizer.advance()
            self.tokenizer.write()

            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception("2: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.tokenizer.advance()
            self.tokenizer.write()
        
        self.tokenizer.advance()
        self.tokenizer.write()
        #self.writeStatement("varStatement", 0)
        self.tokenizer.write(2, "varStatement")

    #Compiles a complete method, function, or constructor.
    def compileSubroutineDec(self):
        self.tokenizer.write(1, "compileSubroutineDec")

        self.symbolTable.clear()
        subRoutineType = self.tokenizer.getToken()

        if(subRoutineType == "method"):
            self.symbolTable.addElement("this", self.className, "ARG")

        self.tokenizer.advance() #method, constructor, function
        self.tokenizer.write()

        self.tokenizer.advance() #type
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("3: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
            
        method_name = "{}.{}".format(self.className, self.tokenizer.getToken())
            
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

        args_counter = self.symbolTable.getCount("VAR")
        self.codeWriter.writeFunction(method_name, args_counter)

        if(subRoutineType == "method"):
            self.codeWriter.push("ARG", 0)
            self.codeWriter.pop("POINTER", 0)
        elif(subRoutineType == "constructor"):
            field_counter = self.symbolTable.getCount("FIELD")
            self.codeWriter.push("CONST", field_counter)
            self.codeWriter.writeCall("Memory.alloc", 1)
            self.codeWriter.pop("POINTER", 0)

        self.compileStatements()

        self.tokenizer.advance()  # }
        self.tokenizer.write()

        self.tokenizer.write(2, "compileSubroutineDec")
    
    #Compiles a (possibly empty) parameter list, not including the enclosing "()" .
    def compileParameterList(self):
        #self.writeStatement("compileParameterList", 1)
        kind = "ARG"

        if(self.tokenizer.getToken() == ")"):
            print("retornou no parameterList")
            return
        
        tipo = self.tokenizer.getToken()
        self.tokenizer.advance()  # type
        self.tokenizer.write(1, "compileParameterList")
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("3: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
        
        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
        
        self.tokenizer.advance()  # identifier
        self.tokenizer.write()

        #VERIFICAR A LOGICA DESSE WHILE, TA ESTRANHO    
        while self.tokenizer.getToken() != ")":
            self.tokenizer.advance()  # ,
            tipo = self.tokenizer.getToken()

            self.tokenizer.write()
            self.tokenizer.advance()  #

            self.tokenizer.write()
            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception("FALHA CPL WHILE")
            
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.tokenizer.advance()  #
            self.tokenizer.write()
    
        #self.writeStatement("compileParameterList", 0)
        self.tokenizer.write(2, "compileParameterList")
    
    #Compiles a var declaration.
    def compileVarDec(self):
        #self.writeStatement("compileVarDec", 1)
        self.tokenizer.write(1, "classVarDec")

        self.tokenizer.advance()  #var
        kind = "VAR"
        tipo = self.tokenizer.getToken()

        self.tokenizer.write()

        self.tokenizer.advance()  # type
        self.tokenizer.write()
        
        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("3: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
        
        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
        self.tokenizer.advance()  # identifier
        self.tokenizer.write()

        while self.tokenizer.getToken() != ";":
            self.tokenizer.advance()  # t,
            self.tokenizer.write()
            if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception("4: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.tokenizer.advance()  #
            self.tokenizer.write()

        self.tokenizer.advance()  #
        self.tokenizer.write()
        #self.writeStatement("compileVarDec", 0)
        self.tokenizer.write(2, "classVarDec")
    
    #Compiles a sequence of statements, not including the enclosing ‘‘{}’’.
    def compileStatements(self):
        #self.writeStatement("compileStatements", 1)
        #self.tokenizer.write(1, "compileStatements")
        flag = 0
        if (self.tokenizer.getToken() in ["return", "let", "do", "if", "while"]):
             self.tokenizer.write(1, "compileStatements")
             flag = 1

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
        if (flag == 1):
            self.tokenizer.write(2, "compileStatements")

    #Compiles an if statement, possibly with a trailing else clause.
    def compileIf(self):
        #self.writeStatement("ifStatement", 1)
        self.tokenizer.write(1, "ifStatement")

        self.tokenizer.advance()  # if
        self.tokenizer.write()

        self.tokenizer.advance()  # (
        self.tokenizer.write()

        self.compileExpression()

        self.tokenizer.advance()  # )
        self.tokenizer.write()

        label_1 = "IF_TRUE{}".format(self.if_counter)
        label_2 = "IF_FALSE{}".format(self.if_counter)
        label_3 = "IF_END{}".format(self.if_counter)

        self.codeWriter.writeIfGoto(label_1)
        self.codeWriter.writeGoto(label_2)
        self.codeWriter.writeLabel(label_1)
        self.if_counter += 1

        self.tokenizer.advance()  # {
        self.tokenizer.write()

        self.compileStatements()

        self.codeWriter.writeGoto(label_3)

        self.tokenizer.advance()  # }
        self.tokenizer.write()
        self.codeWriter.writeLabel(label_2)

        if(self.tokenizer.getToken() == "else"):
            self.tokenizer.advance() # else
            self.tokenizer.write()
            self.tokenizer.advance() # {
            self.tokenizer.write()

            self.compileStatements()

            self.tokenizer.advance() # }
            self.tokenizer.write()

        #self.writeStatement("ifStatement", 0)
        self.codeWriter.writeLabel(label_3)
        self.tokenizer.write(2, "ifStatement")

    def compileWhile(self):
        #self.writeStatement("whileStatement", 1)
        self.tokenizer.write(1, "whileStatement")

        self.tokenizer.advance()  # while
        self.tokenizer.write()
        label_1 = "WHILE_EXP{}".format(self.while_counter)
        label_2 = "WHILE_END{}".format(self.while_counter)
        self.while_counter += 1
        self.codeWriter.writeLabel(label_1)

        self.tokenizer.advance()  # (
        self.tokenizer.write()

        self.compileExpression()
        self.codeWriter.writeExpression("NOT")

        self.tokenizer.advance()  # )        
        self.tokenizer.write()

        self.tokenizer.advance()  # {
        self.tokenizer.write()

        self.codeWriter.writeIfGoto(label_2)

        self.compileStatements()

        self.codeWriter.writeGoto(label_1)
        self.codeWriter.writeLabel(label_2)

        self.tokenizer.advance()  # }
        self.tokenizer.write()

        #self.writeStatement("whileStatement", 0)
        self.tokenizer.write(2, "whileStatement")

    def compileLet(self):
        #self.writeStatement("letStatement", 1)
        self.tokenizer.write(1, "letStatement")
        self.tokenizer.advance()  # let
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("5: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
            
        tipo, categ, pos = self.symbolTable.get(self.tokenizer.getToken())
        # print(categ)
        categoria = self.kind_myd[categ]

        self.tokenizer.advance()  # identifier
        self.tokenizer.write()

        if(self.tokenizer.getToken() == "["):
            self.tokenizer.advance() # [
            self.tokenizer.write()

            self.compileExpression()

            self.tokenizer.advance()  # ]

            self.codeWriter.push(categoria, pos)
            self.codeWriter.writeExpression("ADD")
            self.codeWriter.pop("TEMP", 0)


            self.tokenizer.write()
            self.tokenizer.advance()  # =
            self.tokenizer.write()
            self.compileExpression()

            self.codeWriter.push("TEMP", 0)
            self.codeWriter.pop("POINTER", 1)
            self.codeWriter.pop("THAT", 0)

        else:
            self.tokenizer.advance()  # =
            self.tokenizer.write()
            self.compileExpression()
            self.codeWriter.pop(categoria, pos)

        self.tokenizer.advance()  # ;
        self.tokenizer.write()
        #self.writeStatement("letStatement", 0)
        self.tokenizer.write(2, "letStatement")
        #return True
   
    def compileReturn(self):
        #self.writeStatement("returnStatement", 1)
        self.tokenizer.write(1, "returnStatement")
        self.tokenizer.advance()  # return
        self.tokenizer.write()

        if(self.tokenizer.getToken() != ";"):
            self.compileExpression()
        else:
            self.codeWriter.push("CONST", 0)

        self.codeWriter.writeReturn()  
        self.tokenizer.advance()  # ;
        self.tokenizer.write()
        #self.writeStatement("returnStatement", 0)
        self.tokenizer.write(2, "returnStatement")
    
    def compileDo(self):
        #self.writeStatement("doStatement", 1)
        self.tokenizer.write(1, "doStatement")
        self.tokenizer.advance()  # do
        self.tokenizer.write()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("5: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
        
        variable_name = self.tokenizer.getToken()

        self.tokenizer.advance()  # identifier

        self.codeWriter.pop("TEMP", 0)

        self.tokenizer.write()

        self.tokenizer.advance()  # ;

        self.tokenizer.write()

        #self.writeStatement("doStatement", 0)

        self.tokenizer.write(2, "doStatement")

    def compileExpression(self):
        #self.writeStatement("expression", 1)
        self.tokenizer.write(1, "expression")

        self.compileTerm()
        print("operator {}".format(self.tokenizer.getToken()))

        while (self.tokenizer.getToken() in ['+', '-' , '&amp', '|', '&lt', '&gt', '=']):
            operation = self.tokenizer.getToken()
            self.tokenizer.advance()  # ,

            self.tokenizer.write()
            self.compileTerm()
            if(operation in self.operator_myd):
                self.codeWriter.writeExpression(self.operator_myd.get(operation))
            elif (operation == "*"):
                self.codeWriter.writeCall("Math.multiply", 2)
            elif (operation == "/"):
                self.codeWriter.writeCall("Math.divide", 2)
            else:
                raise Exception
        
        #self.writeStatement("expression", 0)
        self.tokenizer.write(2, "expression")
        
        return True

    def compileExpressionList(self):
        #self.writeStatement("compileExpressionList", 1)
        self.tokenizer.write(1, "compileExpressionList")

        len_args = 0

        if(self.tokenizer.getToken() == ")"):
            return len_args

        self.compileExpression()
        len_args = len_args + 1

        while (self.tokenizer.getToken() != ")"):

            self.tokenizer.advance()  #,
            subroutineName = self.tokenizer.getToken()

            self.tokenizer.write()
            self.compileExpression()
            len_args = len_args + 1

        #self.writeStatement("compileExpressionList", 0)
        self.tokenizer.write(2, "compileExpressionList")
        return len_args
    
    def compileSubroutineCall(self):
        #self.writeStatement("compileSubroutineCall", 1)
        self.tokenizer.write(1, "compileSubroutineCall")
        functionName = variable_name
        args_counter = 0

        if(self.tokenizer.getToken() == "."):
            self.tokenizer.advance()  # .
            subroutineName = self.tokenizer.getToken()
            self.tokenizer.write()
            self.tokenizer.advance()  # identifier
            tipo, categ, pos = self.symbolTable.get(variable_name)
            self.tokenizer.write()

            if(tipo != None):
                categoria = self.kind_myd[categ]

                self.codeWriter.push(categoria, pos)
                functionName = "{}.{}".format(tipo, subroutineName)
                args_counter += 1
            else:
                functionName = "{}.{}".format(variable_name, subroutineName)

        elif (self.tokenizer.getToken() == "("):
            subroutineName = variable_name
            functionName = "{}.{}".format(self.className, subroutineName)
            args_counter += 1
            self.codeWriter.push("POINTER", 0)


        self.tokenizer.advance()  # (
        self.tokenizer.write()
        args_counter += self.compileExpressionList()

        self.compileExpressionList()

        self.tokenizer.advance() 
        self.tokenizer.write()
        self.codeWriter.writeCall(functionName, args_counter)

        #self.writeStatement("compileSubroutineCall", 1)
        self.tokenizer.write(2, "compileSubroutineCall")

    def compileString(self):
        #self.writeStatement("stringStatement", 1)
        self.tokenizer.write(1, "stringStatement")
        string = self.tokenizer.getToken[1:]

        self.codeWriter.push("CONST", len(string))
        self.codeWriter.writeCall("String.new", 1)

        for i in string:
            self.codeWriter.push("CONST", ord(i))
            self.codeWriter.writeCall("String.appendChar", 2)

        self.tokenizer.advance()
        self.tokenizer.write()
        #self.writeStatement("stringStatement", 0)
        self.tokenizer.write(2, "stringStatement")
    
    def compileTerm(self):
        #self.writeStatement("compileTerm", 1)
        self.tokenizer.write(1, "compileTerm")

        if(self.tokenizer.tokenType() == self.tokenizer.STRING):
            self.compileString()
        elif(self.tokenizer.tokenType() == self.tokenizer.INTEGER):
            self.codeWriter.push("CONST", int(self.tokenizer.getToken()))
            self.tokenizer.advance()  # int
        elif(self.tokenizer.getToken() in ["false", "null", "true"]):
            self.codeWriter.push("CONST", 0)
            if(self.tokenizer.getToken() == "true"):
                self.codeWriter.writeExpression("NOT")
            self.tokenizer.advance()  # keyword
        elif(self.tokenizer.getToken() == "this"):
            self.codeWriter.push("POINTER", 0)
            self.tokenizer.advance()  # this
        elif(self.tokenizer.getToken() in ["-", "~"]):
            op = self.tokenizer.getToken()
            self.tokenizer.advance()  
            self.compileTerm()
            if(op == "-"):
                self.codeWriter.writeExpression("NEG")
            else:
                self.codeWriter.writeExpression("NOT")
        #CHECAR ESSE ELIF
        elif(self.tokenizer.getToken() == "("):
            self.tokenizer.advance()  # (
            self.compileExpression()
            self.tokenizer.advance()  # )
        else:
            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception("5: Waiting for a identifier, but a {} given".format(self.tokenizer.tokenType()))
            
            varName = self.tokenizer.getToken()
            self.tokenizer.advance()  # identifier
            self.tokenizer.write()
            #CHECAR ESSE IF
            if(self.tokenizer.getToken() == "["):
                self.tokenizer.advance()  # [
                self.tokenizer.write()
                self.compileExpression()

                self.tokenizer.advance()  # ]
                self.tokenizer.write()

                tipo, categ, pos = self.symbolTable.get(varName)
                category = self.kind_myd[categ]
                self.codeWriter.push(category, pos)
                self.codeWriter.writeExpression("ADD")
                self.codeWriter.pop("POINTER", 1)
                self.codeWriter.push("THAT", 0)


            elif(self.tokenizer.getToken() in [".", "("]):
                self.compileSubroutineCall()
            else:
                tipo, categ, pos = self.symbolTable.get(varName)
                category = self.kind_myd[categ]
                self.codeWriter.push(category, pos)

        #self.writeStatement("compileTerm", 0)
        self.tokenizer.write(2, "compileTerm")



class CodeWriter:

    def __init__(self, file):
        self.file = file
        self.output = open(file.split(".")[0] + ".vm", "w")

        self.helperDict = {
            "POINTER": "pointer",
            "LOCAL":"local",
            "THAT":"that",
            "THIS":"this",
            "TEMP":"temp",
            "STATIC":"static",
            "ARG":"argument",
            "CONST":"constant",
            "FIELD":"this"
        }

    def pop(self, segment, index):
        replaced = self.helperDict.get(segment)

        if(replaced == None):
            print("Erro 1")
            raise Exception("Error 1")
        
        print("pop {} {}".format(replaced, index), file=self.output)
    
    def push(self, segment, index):

        replaced = self.helperDict.get(segment)

        if(replaced == None):
            print("Error 2")
            return Exception
        
        print("push {} {} ".format(replaced, index), file=self.output)
        
    def writeReturn(self):
        print("return", file=self.output)
    
    def writeGoto(self, label):
        print("goto {}".format(label), file=self.output)

    def writeIfGoto(self, label):
        print("if-goto {}".format(label), file=self.output)
    
    def writeLabel(self, label):
        print("label {}".format(label), file = self.output)
    
    def writeCall(self, name, len_args):
        print("call {} {}".format(name, len_args), file=self.output)

    def writeFunction(self, name, len_local):
        print("function {} {}".format(name, len_local), file=self.output)
    
    def writeExpression(self, command):
        if(command not in ["ADD", "SUB", "NEG", "EQ", "GT", "LT", "AND", "OR", "NOT"]):
            print("Error 3")
            raise Exception
        
        localCase = command.lower()
        
        print(localCase, file=self.output)
    
    def close(self):
        print("close ", self.output)
        self.output


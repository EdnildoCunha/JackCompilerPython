from tokenize import Tokenize 

token = Tokenize('main.jack')
while(token.hasMoreTokens()):
    token.advance()

class Token:
    '''
    A class that represents a token.
    '''
    def __init__(self, token):
        '''
        Initializes a token with a string value.
        '''
        self.token = token

    def __str__(self):
        '''
        Returns the string value of the token.
        '''
        return self.token
    
    def __eq__(self, t):
        '''
        Compares the string value of the token with another token.
        '''
        return self.token == str(t)
    
    def __ne__(self, t):
        '''
        Compares the string value of the token with another token.
        '''
        return self.token != str(t)

class SyntaxAnalyzer:
    '''
    A class that performs lexical analysis on a given input string.
    '''
    TOKEN_NUMBER = Token('N')
    TOKEN_PLUS_OP = Token('+')
    TOKEN_MINUS_OP = Token('-')
    TOKEN_MULT_OP = Token('*')
    TOKEN_DIV_OP = Token('/')
    TOKEN_EOF = Token('$')
    TOKEN_UNDEFINED = Token('?')

    EOF_STR = '$'

    def __init__(self):
        '''
        Initializes the SyntaxAnalyzer class.
        '''
        self.read_count = 0
        self.user_input = ''
        self.next_char = None
        self.next_token = self.TOKEN_EOF
        self.lexeme = ''
        self.lexemes = []
        self.tokens = []

    def read_char(self):
        '''
        Reads the next character in the input string.
        If the end of the input string is reached, sets next_char to None.
        '''
        if self.read_count < len(self.user_input):
            self.next_char = self.user_input[self.read_count]
            self.read_count += 1
        else:
            self.next_char = None
    
    def add_lexeme(self):
        '''
        Adds the next character to the current lexeme.
        '''
        if self.next_char is None: self.lexeme += self.EOF_STR
        else: self.lexeme += self.next_char

    def commit_lexeme(self):
        '''
        Commits the current lexeme to the lexemes list and the current token to the tokens list.
        '''
        self.lexemes.append(self.lexeme)
        self.tokens.append(str(self.next_token))

    def clear_lexeme(self):
        '''
        Clears the current lexeme.
        '''
        self.lexeme = ''

    def remove_whitespace(self):
        '''
        Removes whitespace characters from the input string.
        '''
        while self.next_char is not None and self.next_char.isspace(): self.read_char()

    def lex(self):
        '''
        Performs lexical analysis on the input string.
        '''
        self.clear_lexeme()
        self.remove_whitespace()

        if self.next_char is None: # EOF
            self.add_lexeme()
            self.next_token = self.TOKEN_EOF
            self.commit_lexeme()
            self.clear_lexeme()
            return
        
        if self.next_char.isdigit(): # Number
            self.next_token = self.TOKEN_NUMBER
            while self.next_char is not None and self.next_char.isdigit():
                self.add_lexeme()
                self.read_char()
            self.commit_lexeme()
            self.clear_lexeme()
        else: # Operator
            self.add_lexeme()
            if self.next_char == '+': self.next_token = self.TOKEN_PLUS_OP
            elif self.next_char == '-': self.next_token = self.TOKEN_MINUS_OP
            elif self.next_char == '*': self.next_token = self.TOKEN_MULT_OP
            elif self.next_char == '/': self.next_token = self.TOKEN_DIV_OP
            else: self.next_token = self.TOKEN_UNDEFINED
            self.commit_lexeme()
            self.clear_lexeme()
            self.read_char()

    def lexer(self, user_input):
        '''
        Tokenizes the input string.
        '''
        self.read_count = 0
        self.user_input = user_input
        self.lexemes = []
        self.tokens = []

        self.read_char()

        while True: # Lexical Analysis Loop Before EOF
            self.lex()
            if self.next_token == self.TOKEN_EOF: break

        return self.lexemes, self.tokens

def main():
    S = SyntaxAnalyzer()
    lexemes, tokens = S.lexer("100-12/12")
    print ("Lexemes:" + str(lexemes))
    print ("Tokens:" + str(tokens))

if __name__ == '__main__': main()
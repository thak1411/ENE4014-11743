
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
    
    def parser(self, lexemes, tokens):
        '''
        LR Parses the input string.
        Using Shift-Reduce Algorithms.
        '''
        if len(lexemes) != len(tokens):
            raise BaseException('Error: Lexemes and Tokens do not match.')
        
        # (0) E' -> E
        # (1) E  -> E + T
        # (2) E  -> E - T
        # (3) E  -> T
        # (4) T  -> T * N
        # (5) T  -> T / N
        # (6) T  -> N

        print('Tracing Start!!')
        print('+------+--------------+---------------+-----------------+------------------------+')
        print('|      |            STACK             |      INPUT      |         ACTION         |')
        print('+------+--------------+---------------+-----------------+------------------------+')
        # LR Parsing Table
        table = {
            0: { 'N': (0, 3), },
            1: { '+': (0, 4), '-': (0, 5), '$': (2, 0), },
            2: { '+': (1, 3), '-': (1, 3), '*': (0, 6), '/': (0, 7), '$': (1, 3), },
            3: { '+': (1, 6), '-': (1, 6), '*': (1, 6), '/': (1, 6), '$': (1, 6), },
            4: { 'N': (0, 3), },
            5: { 'N': (0, 3), },
            6: { 'N': (0, 10), },
            7: { 'N': (0, 11), },
            8: { '+': (1, 1), '-': (1, 1), '*': (0, 6), '/': (0, 7), '$': (1, 1), },
            9: { '+': (1, 2), '-': (1, 2), '*': (0, 6), '/': (0, 7), '$': (1, 2), },
            10: { '+': (1, 4), '-': (1, 4), '*': (1, 4), '/': (1, 4), '$': (1, 4), },
            11: { '+': (1, 5), '-': (1, 5), '*': (1, 5), '/': (1, 5), '$': (1, 5), },
        }
        # LR Goto Table
        goto_table = {
            0: { 'E': 1, 'T': 2, },
            4: { 'T': 8, },
            5: { 'T': 9, },
        }
        step = 0
        stack = [0]
        vstack = []
        success = False
        result = 0
        def print_step(stack, lexemes, action):
            '''
            Print the current step of the LR Parsing Algorithm.
            '''
            nonlocal step
            print('| ({:0>2}) | {:<29}|{:>16} |{:>23} |'.format(f'{step}', ' '.join(list(map(lambda x : str(x), stack))), ''.join(lexemes), action))
            step += 1

        while True: # Shift-Reduce Algorithm Loop
            state = stack[-1]
            if len(tokens) < 1: # If there are no more tokens, break the loop - Fail Case
                break
            user_input = tokens[0]
            lex = lexemes[0]
            # Read Table & Perform Action
            # If State or Token is not in the table, break the loop - Fail Case
            if state not in table or user_input not in table[state]: break
            t, n = table[state][user_input]

            if t == 0: # Shift
                print_step(stack, tokens, f'Shift {n}')
                stack.append(user_input)
                stack.append(n)
                if user_input == 'N': vstack.append(int(lex))
                lexemes.pop(0)
                tokens.pop(0)
            elif t == 1: # Reduce
                prev_stack = stack.copy() # Save the previous stack for printing

                # Perform Reduction & Calculate Result
                if n == 1: # E -> E + T
                    v2 = vstack.pop()
                    v1 = vstack.pop()
                    vstack.append(v1 + v2)
                    reduc_count = 6
                    reduc_symbol = 'E'
                elif n == 2: # E -> E - T
                    v2 = vstack.pop()
                    v1 = vstack.pop()
                    vstack.append(v1 - v2)
                    reduc_count = 6
                    reduc_symbol = 'E'
                elif n == 3: # E -> T
                    reduc_count = 2
                    reduc_symbol = 'E'
                elif n == 4: # T -> T * N
                    v2 = vstack.pop()
                    v1 = vstack.pop()
                    vstack.append(v1 * v2)
                    reduc_count = 6
                    reduc_symbol = 'T'
                elif n == 5: # T -> T / N
                    v2 = vstack.pop()
                    v1 = vstack.pop()
                    if v2 == 0: break # Division by Zero - Fail Case
                    vstack.append(v1 / v2)
                    reduc_count = 6
                    reduc_symbol = 'T'
                elif n == 6: # T -> N
                    reduc_count = 2
                    reduc_symbol = 'T'
                else: break

                for _ in range(reduc_count): stack.pop() # Pop the stack for the number of symbols reduced

                reduce_state = stack[-1]
                reduce_token = reduc_symbol
                # If State or Token is not in the Goto Table, break the loop - Fail Case
                if reduce_state not in goto_table or reduce_token not in goto_table[reduce_state]: break
                # Push the reduced symbol to the stack
                stack.append(reduce_token)
                stack.append(goto_table[reduce_state][reduce_token])
                print_step(prev_stack, tokens, f'Reduce {n} (Goto[{reduce_state}, {reduce_token}])')
            elif t == 2: # Accept
                print_step(stack, tokens, 'Accept')
                success = True
                result = vstack.pop()
                break
            else: break # Undefined State - Fail Case

        if success == False: return None # Fail Case Return None
        return result # Success Case Return Result

def main():
    S = SyntaxAnalyzer()
    user_input = '100-12/12'
    lexemes, tokens = S.lexer(user_input)
    print ("Lexemes:" + str(lexemes))
    print ("Tokens:" + str(tokens))
    result = S.parser(lexemes, tokens)
    print('result:' + str(result))
    print('real result:' + str(eval(user_input)))

import sys
import io

class BufferedPrint:
    '''
    A class that change the standard output to a buffer.

    Usage:
    with BufferedPrint(buffer):
        print('blabla')
    '''
    def __init__(self, buf):
        self.buf = buf
        self._original_stdout = None

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = self.buf

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout

def test(result, answer):
    '''
    Tests if the result is equal to the answer.
    '''
    EPS = 1e-6
    try:
        if answer is None: return result is None
        return abs(answer - result) < EPS
    except: return False
    
def check_test(test_name, user_input, result, answer, debug_message):
    '''
    Checks if the test passed or failed.

    If the test failed, print for debugging message & raise an exception.
    '''
    if test(result, answer): print(f'[Test "{test_name}" Passed]')
    else:
        print(f'\n[Test "{test_name}" Failed]\n\nuser input: {user_input}\nactual result: {result}\nexpected result: {answer}\n\nuser prints:\n{debug_message}\n')
        raise BaseException('Test Failed')

def rn_test():
    '''
    Rn's Test Cases
    '''
    S = SyntaxAnalyzer()
    debug_message = None

    def get_result(user_input):
        '''
        Get the result of the Syntax Analyzer from user_input
        '''
        nonlocal debug_message
        buffer = io.StringIO()
        with BufferedPrint(buffer):
            lexemes, tokens = S.lexer(user_input)
            result = S.parser(lexemes, tokens)
        debug_message = buffer.getvalue()
        buffer.close()
        return result

    
    try:
        # Test 1 [Just Number]
        user_input = '123456'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Just Number', user_input, rs, an, debug_message)

        # # Test 2 [Just Addition]
        user_input = '123000+456'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Just Addition', user_input, rs, an, debug_message)

        # Test 3 [Just Subtraction]
        user_input = '123456-456'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Just Subtraction', user_input, rs, an, debug_message)

        # Test 4 [Just Multiplication]
        user_input = '123*456'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Just Multiplication', user_input, rs, an, debug_message)

        # Test 5 [Just Division]
        user_input = '123456/456'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Just Division', user_input, rs, an, debug_message)

        # Test 6 [Many Additions]
        user_input = '123+456+789+123+456+789'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Many Additions', user_input, rs, an, debug_message)

        # Test 7 [Many Subtractions]
        user_input = '123-456-789-123-456-789'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Many Subtractions', user_input, rs, an, debug_message)

        # Test 8 [Many Multiplications]
        user_input = '123*456*789*123*456*789'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Many Multiplications', user_input, rs, an, debug_message)

        # Test 9 [Many Divisions]
        user_input = '123/456/789/123/456/789'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Many Divisions', user_input, rs, an, debug_message)

        # Test 10 [Mixed Operations]
        user_input = '123+456-789*123/456/123+456-789-123+456+789*123*456/789/123'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Mixed Operations', user_input, rs, an, debug_message)

        # Test 11 [Mixed Operations with Blanks]
        user_input = '123+ 456 -789  *123   /    456/123+456       -789-     123 + 456 + 789 * 123 * 456 / 789 / 123'
        rs, an = get_result(user_input), eval(user_input)
        check_test('Mixed Operations with Blanks', user_input, rs, an, debug_message)

        # Test 12 [Compilation Error - Invalid Token 1]
        user_input = '123+456-789*123/456/123+456-789-123+456+789*123*456/789/123+'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Invalid Token 1', user_input, rs, an, debug_message)

        # Test 13 [Compilation Error - Invalid Token 2]
        user_input = '123+456-789*123/456/123+456-789--123+456+789*123*456/789/123'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Invalid Token 2', user_input, rs, an, debug_message)

        # Test 14 [Compilation Error - Invalid Token 3]
        user_input = '123+456-789*123/456/123+456-789-123+456+789*123**456/789/123'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Invalid Token 3', user_input, rs, an, debug_message)

        # Test 14 [Compilation Error - Invalid Token 4]
        user_input = '+123+456-789*123/456/123+456-789-123+456+789*123*456/789/123'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Invalid Token 4', user_input, rs, an, debug_message)

        # Test 15 [Compilation Error - Invalid Token 5]
        user_input = '123+456-789*123/456/123+456-789-123+456+789*123*456//789/123'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Invalid Token 5', user_input, rs, an, debug_message)

        # Test 16 [Compilation Error - Invalid Token 6]
        user_input = '123+456-789*123/456/123++456-789-123+456+789*123*456/789/123'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Invalid Token 6', user_input, rs, an, debug_message)

        # Test 17 [Compilation Error - Undefined Token 1]
        user_input = '123+456-789*123/456/123+456-789?123+456+789*123*456/789/123'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Undefined Token 1', user_input, rs, an, debug_message)

        # Test 18 [Compilation Error - Undefined Token 2]
        user_input = '123+456-789*123/456/123+456-789-123s456+789*123*456/789/123'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Undefined Token 2', user_input, rs, an, debug_message)

        # Test 19 [Compilation Error - Undefined Token 3]
        user_input = '123+456-789*123/456/123+456-789-123456@+789*123*456/789/123'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Undefined Token 3', user_input, rs, an, debug_message)

        # Test 20 [Compilation Error - Undefined Token 4]
        user_input = '123$'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Undefined Token 4', user_input, rs, an, debug_message)

        # Test 21 [Compilation Error - Undefined Token 5]
        user_input = '123$+456'
        rs, an = get_result(user_input), None
        check_test('Compilation Error - Undefined Token 5', user_input, rs, an, debug_message)

        # Test 22 [Division by Zero]
        user_input = '123/0'
        rs, an = get_result(user_input), None
        check_test('Division by Zero', user_input, rs, an, debug_message)

        print('All Tests Passed!')

    except BaseException as e:
        print(e)
        return False
    return True

if __name__ == '__main__': main()
# if __name__ == '__main__': rn_test()
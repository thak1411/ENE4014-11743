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

        print('All Tests Passed!')

    except BaseException as e:
        print(e)
        return False
    return True

# if __name__ == '__main__': main()
if __name__ == '__main__': rn_test()
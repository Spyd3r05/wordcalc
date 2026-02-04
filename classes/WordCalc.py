from classes.Parser import Parser
from classes.Lexer import Lexer
from classes.WordCalcError import  WordCalcError
from classes.Interpreter import Interpreter

class WordCalc:
    """
    Main WordCalc class - Coordinates lexer, parser, and interpreter
    """
    
    def __init__(self):
        pass
    
    def evaluate(self, expression):
        """
        Evaluate a WordCalc expression
        
        Args:
            expression (str): The expression to evaluate (e.g., "add three and five")
        
        Returns:
            str: The result in word form (e.g., "eight")
        """
        try:
            # Step 1: Tokenize
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            
            # Step 2: Parse
            parser = Parser(tokens)
            operation, num1, num2 = parser.parse()
            
            # Step 3: Interpret
            interpreter = Interpreter(operation, num1, num2)
            result = interpreter.interpret()
            
            return result
            
        except WordCalcError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
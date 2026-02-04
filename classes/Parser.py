from classes.WordCalcError import WordCalcError

class Parser:
    """
    Parser - Validates syntax according to BNF grammar
    """
    
    # Word to number mappings
    WORD_TO_NUM = {
        # Digits (0-9)
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        # Teens (10-19)
        'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
        # Tens (20, 30, 40, ...)
        'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
        'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }
    
    OPERATIONS = {'add', 'subtract', 'multiply', 'divide'}
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.operation = None
        self.num1 = None
        self.num2 = None
    
    def current_token(self):
        """Get current token without consuming it"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def consume_token(self):
        """Get current token and move to next"""
        token = self.current_token()
        self.position += 1
        return token
    
    def parse_operation(self):
        """Parse the operation token"""
        token = self.consume_token()
        if token not in self.OPERATIONS:
            raise WordCalcError(f"Invalid operation: '{token}'. Expected: add, subtract, multiply, or divide")
        self.operation = token
    
    def parse_number(self):
        """Parse a number (can be single word or compound)"""
        token = self.consume_token()
        
        if token is None:
            raise WordCalcError("Expected a number but reached end of input")
        
        # Check if it's a simple number (digit, teen, or tens)
        if token in self.WORD_TO_NUM:
            base_value = self.WORD_TO_NUM[token]
            
            # Check for compound number (e.g., "twenty three")
            # Only tens can form compounds
            if token in ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']:
                next_token = self.current_token()
                if next_token and next_token in self.WORD_TO_NUM and self.WORD_TO_NUM[next_token] < 10:
                    # It's a compound number
                    self.consume_token()
                    return base_value + self.WORD_TO_NUM[next_token]
            
            return base_value
        else:
            raise WordCalcError(f"Unknown number word: '{token}'")
    
    def parse(self):
        """Parse the entire expression according to BNF grammar"""
        # <expression> ::= <operation> <number> "and" <number>
        
        # Parse operation
        self.parse_operation()
        
        # Parse first number
        self.num1 = self.parse_number()
        
        # Expect "and"
        and_token = self.consume_token()
        if and_token != 'and':
            raise WordCalcError(f"Expected 'and' but got '{and_token}'")
        
        # Parse second number
        self.num2 = self.parse_number()
        
        # Check for extra tokens
        if self.position < len(self.tokens):
            extra = ' '.join(self.tokens[self.position:])
            raise WordCalcError(f"Unexpected tokens at end: '{extra}'")
        
        return self.operation, self.num1, self.num2
"""
Parser Module - Enhanced with Hundreds and Thousands Support
Validates syntax according to BNF grammar and converts words to numbers (0-9999)
"""

from classes.WordCalcError import WordCalcError

class Parser:
    
    # Word to number mappings for basic numbers (0-99)
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
    
    # Multiplier keywords
    MULTIPLIERS = {
        'hundred': 100,
        'thousand': 1000
    }
    
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
    
    def peek_token(self, offset=1):
        """Look ahead at token without consuming"""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def count_remaining_ands(self):
        """Count how many 'and' tokens remain from current position"""
        count = 0
        for i in range(self.position, len(self.tokens)):
            if self.tokens[i] == 'and':
                count += 1
        return count
    
    def parse_operation(self):
        """Parse the operation token"""
        token = self.consume_token()
        if token not in self.OPERATIONS:
            raise WordCalcError(f"Invalid operation: '{token}'. Expected: add, subtract, multiply, or divide")
        self.operation = token
    
    def parse_basic_number(self):
        """
        Parse a basic number (0-99)
        Handles: digit, teen, tens, compound
        """
        token = self.current_token()
        
        if token is None or token not in self.WORD_TO_NUM:
            return None
        
        # Consume the token
        self.consume_token()
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
    
    def parse_number(self, is_first_number=True):
        """
        Parse a complete number (0-9999)
        
        Grammar:
        <number> ::= <large_number> | <hundreds> | <basic_number>
        <large_number> ::= <thousands> [<hundreds>] [<basic_number>]
        <thousands> ::= <basic_number> "thousand"
        <hundreds> ::= <basic_number> "hundred"
        <basic_number> ::= <digit> | <teen> | <tens> | <compound>
        
        Note: Handles optional "and" within numbers
        Uses 'and' counting: if 2+ 'and's remain, one can be used within number
        
        Args:
            is_first_number: True if parsing first operand, False if second
        """
        total = 0
        
        # Try to parse basic number first (might be part of thousands/hundreds)
        base = self.parse_basic_number()
        
        if base is None:
            raise WordCalcError(f"Expected a number but got '{self.current_token()}'")
        
        # Check if next token is a multiplier (thousand or hundred)
        next_token = self.current_token()
        
        # Handle THOUSANDS
        if next_token == 'thousand':
            if base == 0:
                raise WordCalcError("Cannot have 'zero thousand'")
            if base > 9:
                raise WordCalcError(f"Invalid thousands value: '{base}'. Must be 1-9")
            
            self.consume_token()  # consume 'thousand'
            total = base * 1000
            
            # Check for optional "and" - use helper to determine if it's within number
            if self.current_token() == 'and' and self._is_and_within_number(is_first_number):
                self.consume_token()
            
            # Try to parse hundreds part
            hundreds_part = self.parse_hundreds_part()
            total += hundreds_part
            
            # Check for optional "and" again before tens/ones
            if self.current_token() == 'and' and self._is_and_within_number(is_first_number):
                self.consume_token()
            
            # Try to parse basic number (tens/ones)
            basic_part = self.parse_basic_number()
            if basic_part is not None:
                total += basic_part
        
        # Handle HUNDREDS (without thousands)
        elif next_token == 'hundred':
            if base == 0:
                raise WordCalcError("Cannot have 'zero hundred'")
            if base > 9:
                raise WordCalcError(f"Invalid hundreds value: '{base}'. Must be 1-9")
            
            self.consume_token()  # consume 'hundred'
            total = base * 100
            
            # Check for optional "and" - use helper to determine if it's within number
            if self.current_token() == 'and' and self._is_and_within_number(is_first_number):
                self.consume_token()
            
            # Try to parse basic number (tens/ones)
            basic_part = self.parse_basic_number()
            if basic_part is not None:
                total += basic_part
        
        # Just a basic number (0-99)
        else:
            total = base
        
        # Validate range
        if total > 9999:
            raise WordCalcError(f"Number too large: {total}. Maximum is 9999")
        
        return total
    
    def _is_and_within_number(self, is_first_number=True):
        """
        Helper: Determine if current "and" is within a number or is expression separator
        
        KEY LOGIC: Count remaining 'and' tokens
        - If parsing FIRST number:
          - Need at least 2 'and's (one for number, one for separator)
          - If only 1 'and' remains: must be expression separator
        - If parsing SECOND number:
          - Any 'and' can be within the number (no separator needed after)
        
        Returns True if "and" should be consumed as part of current number
        Returns False if "and" is the expression separator
        
        Args:
            is_first_number: True if parsing first operand, False if second
        """
        # Count how many 'and' tokens remain from current position
        remaining_ands = self.count_remaining_ands()
        
        # If parsing SECOND number, we don't need to reserve an 'and' for separator
        # So any 'and' we encounter can be consumed as part of the number
        if not is_first_number:
            # Still check if it looks like a valid internal 'and'
            next_token = self.peek_token(1)
            if next_token is None or next_token not in self.WORD_TO_NUM:
                return False
            
            # Check if pattern indicates new number (shouldn't happen in second number)
            following_token = self.peek_token(2)
            if following_token in ['hundred', 'thousand']:
                return False
            
            # Otherwise, consume it as part of the number
            return True
        
        # If parsing FIRST number and only 1 'and' remains,
        # it MUST be the expression separator
        if remaining_ands <= 1:
            return False
        
        # If 2+ 'and's remain, check if this one should be within the number
        # Look at what comes after "and"
        next_token = self.peek_token(1)
        
        if next_token is None or next_token not in self.WORD_TO_NUM:
            # Nothing valid after "and", so it's not within our number
            return False
        
        # Check if the pattern is "and [number] [hundred|thousand]"
        # This would indicate a NEW number component (even with multiple 'and's)
        following_token = self.peek_token(2)
        
        if following_token in ['hundred', 'thousand']:
            # Pattern: "and five hundred" or "and two thousand"
            # This "and" starts a new number, NOT part of current number
            return False
        
        # Check for compound numbers: "and twenty three" where "twenty" is at peek(1)
        if next_token in ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']:
            # Could be compound, check if followed by single digit
            if following_token in self.WORD_TO_NUM and self.WORD_TO_NUM.get(following_token, 100) < 10:
                # It's a compound within our number: "and twenty three"
                return True
            # Just tens: "and twenty" (not followed by digit)
            # Check if there's a third token that could be hundred/thousand
            third_token = self.peek_token(3)
            if third_token in ['hundred', 'thousand']:
                # "and twenty hundred" would be invalid, but let's be safe
                return False
        
        # Default: if it's just a basic number word and we have 2+ 'and's,
        # this one is within our number
        # Examples: "and five", "and thirty", "and twelve"
        return True
    
    def parse_hundreds_part(self):
        """
        Parse the hundreds component (if present)
        Returns 0 if no hundreds found
        """
        base = self.parse_basic_number()
        
        if base is None:
            return 0
        
        if self.current_token() == 'hundred':
            if base == 0:
                raise WordCalcError("Cannot have 'zero hundred'")
            if base > 9:
                raise WordCalcError(f"Invalid hundreds value: '{base}'. Must be 1-9")
            
            self.consume_token()  # consume 'hundred'
            return base * 100
        else:
            # Put the number back - it's not a hundreds component
            # We need to backtrack
            # Since we consumed tokens, we decrement position
            if base < 10:
                self.position -= 1
            else:
                # Compound number (e.g., "twenty three")
                self.position -= 2
            return 0
    
    def parse(self):
        """
        Parse the entire expression according to BNF grammar
        
        FIXED: Now handles "and" ambiguity by counting remaining 'and' tokens
        
        Examples:
        - "add one hundred and thirty and twenty"
          → 2 'and's: first for number (130), second for separator
          → Result: 130 + 20
        
        - "multiply two thousand five hundred and three"
          → 1 'and': must be expression separator
          → Result: 2500 * 3 (not 2503!)
        
        - "add fifty and one hundred and five"
          → 2 'and's: first is separator, second within second number
          → Result: 50 + 105
        """
        # <expression> ::= <operation> <number> "and" <number>
        
        # Parse operation
        self.parse_operation()
        
        # Parse first number (may consume internal "and" tokens if 2+ exist)
        self.num1 = self.parse_number(is_first_number=True)
        
        # Now expect "and" as the expression separator
        # This is the "and" between the two operands
        and_token = self.consume_token()
        if and_token != 'and':
            raise WordCalcError(f"Expected 'and' between numbers but got '{and_token}'")
        
        # Parse second number (can consume any "and" tokens within it)
        self.num2 = self.parse_number(is_first_number=False)
        
        # Check for extra tokens
        if self.position < len(self.tokens):
            extra = ' '.join(self.tokens[self.position:])
            raise WordCalcError(f"Unexpected tokens at end: '{extra}'")
        
        return self.operation, self.num1, self.num2
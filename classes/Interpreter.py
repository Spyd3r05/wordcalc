"""
Interpreter Module - Enhanced with Hundreds and Thousands Support
Executes operations and converts results to words (0-9999)
"""

from classes.WordCalcError import WordCalcError


class Interpreter:
    """
    Interpreter - Executes the parsed expression and returns result
    Now supports number-to-word conversion for 0-9,999
    """
    
    # Number to word mappings (for output)
    NUM_TO_WORD = {
        0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
        5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
        10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
        15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
        20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty',
        60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety'
    }
    
    def __init__(self, operation, num1, num2):
        self.operation = operation
        self.num1 = num1
        self.num2 = num2
    
    def execute(self):
        """Execute the operation and return numeric result"""
        if self.operation == 'add':
            return self.num1 + self.num2
        elif self.operation == 'subtract':
            return self.num1 - self.num2
        elif self.operation == 'multiply':
            return self.num1 * self.num2
        elif self.operation == 'divide':
            if self.num2 == 0:
                raise WordCalcError("Cannot divide by zero")
            # Integer division
            return self.num1 // self.num2
        else:
            raise WordCalcError(f"Unknown operation: {self.operation}")
    
    def number_to_words(self, num):
        """
        Convert a number (0-9999) to its word representation
        
        Algorithm:
        - Handle negative numbers
        - Break down into: thousands, hundreds, tens, ones
        - Convert each component and combine
        """
        # Handle negative numbers
        if num < 0:
            return f"negative {self.number_to_words(abs(num))}"
        
        # Handle zero
        if num == 0:
            return 'zero'
        
        # For numbers beyond our range, return as digits
        if num > 9999:
            return str(num)
        
        # Build the word representation
        parts = []
        
        # THOUSANDS place (1000-9000)
        if num >= 1000:
            thousands_digit = num // 1000
            parts.append(self.NUM_TO_WORD[thousands_digit])
            parts.append('thousand')
            num = num % 1000  # Remove thousands
        
        # HUNDREDS place (100-900)
        if num >= 100:
            hundreds_digit = num // 100
            parts.append(self.NUM_TO_WORD[hundreds_digit])
            parts.append('hundred')
            num = num % 100  # Remove hundreds
        
        # TENS and ONES place (0-99)
        if num > 0:
            parts.append(self._convert_below_hundred(num))
        
        return ' '.join(parts)
    
    def _convert_below_hundred(self, num):
        """
        Convert numbers 1-99 to words
        Helper method for number_to_words
        
        Args:
            num: Integer between 1 and 99
        
        Returns:
            String representation of the number
        """
        # Direct lookup for 0-20 and multiples of 10
        if num in self.NUM_TO_WORD:
            return self.NUM_TO_WORD[num]
        
        # Compound numbers (21-99)
        if 20 < num < 100:
            tens_place = (num // 10) * 10
            ones_place = num % 10
            
            tens_word = self.NUM_TO_WORD[tens_place]
            ones_word = self.NUM_TO_WORD[ones_place]
            
            return f"{tens_word} {ones_word}"
        
        # Shouldn't reach here if num is 1-99
        return str(num)
    
    def interpret(self):
        """Execute and return result as words"""
        result = self.execute()
        return self.number_to_words(result)
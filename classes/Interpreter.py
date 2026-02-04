from classes.WordCalcError import WordCalcError

class Interpreter:
    """
    Interpreter - Executes the parsed expression and returns result
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
        """Convert a number to its word representation"""
        if num < 0:
            return f"negative {self.number_to_words(abs(num))}"
        
        if num in self.NUM_TO_WORD:
            return self.NUM_TO_WORD[num]
        
        # Handle compound numbers (21-99)
        if 20 < num < 100:
            tens = (num // 10) * 10
            ones = num % 10
            if ones == 0:
                return self.NUM_TO_WORD[tens]
            else:
                return f"{self.NUM_TO_WORD[tens]} {self.NUM_TO_WORD[ones]}"
        
        # For numbers >= 100, just return as digits (extension)
        if num >= 100:
            return str(num)
        
        return str(num)
    
    def interpret(self):
        """Execute and return result as words"""
        result = self.execute()
        return self.number_to_words(result)
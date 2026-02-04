from classes.WordCalcError import WordCalcError
class Lexer:
    """
    Lexer/Tokenizer - Breaks down input string into tokens
    """
    
    def __init__(self, text):
        self.text = text.lower().strip()
        self.tokens = []
    
    def tokenize(self):
        """Split input into individual tokens"""
        if not self.text:
            raise WordCalcError("Empty input")
        
        # Split by whitespace
        self.tokens = self.text.split()
        return self.tokens
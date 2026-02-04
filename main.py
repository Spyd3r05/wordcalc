"""
WordCalc - A Simple Natural Language Calculator
Parses and executes arithmetic expressions in natural language
Example: "add four and five" -> "nine"
"""

from classes.WordCalc import WordCalc

def main():
    """
    Main function with test examples
    """
    print("=" * 60)
    print("WordCalc - Natural Language Calculator")
    print("=" * 60)
    print()
    
    calc = WordCalc()
    
    # Test cases
    test_cases = [
        "add four and five",
        "subtract ten and three",
        "multiply two and four",
        "divide twenty and five",
        "multiply thirty two and seventeen",
        "multiply seven and eight",
        "subtract fifty and twenty five",
        "divide ninety and ninety",
        # Edge cases
        "add zero and five",
        "subtract five and five",
        # Error cases
        "add five",  # Missing second number
        "five and three",  # Missing operation
        "plus three and five",  # Invalid operation
        "divide ten and zero",  # Division by zero
    ]
    
    for expression in test_cases:
        result = calc.evaluate(expression)
        print(f"Input:  '{expression}'")
        print(f"Output: {result}")
        print("-" * 60)
    
    print()
    print("=" * 60)
    print("Interactive Mode - Enter 'quit' to exit")
    print("=" * 60)
    print()
    
    # Interactive mode
    while True:
        try:
            user_input = input("WordCalc> ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            if user_input:
                result = calc.evaluate(user_input)
                print(f"Result: {result}")
                print()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
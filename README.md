# WordCalc - Natural Language Calculator

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

A simple programming language interpreter that executes arithmetic operations using natural language expressions.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Grammar Specification](#grammar-specification)
- [Architecture](#architecture)
- [Module Documentation](#module-documentation)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Extending WordCalc](#extending-wordcalc)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**WordCalc** is a domain-specific programming language (DSL) designed for performing basic arithmetic operations using natural language syntax. Instead of writing `4 + 5`, users can write `add four and five`.

### Why WordCalc?

- **Educational**: Perfect for learning about language interpreters, lexical analysis, parsing and execution
- **Natural**: Uses intuitive English words instead of symbols
- **Simple**: Clean architecture demonstrating compiler design principles
- **Extensible**: Modular design makes it easy to add new features

---

## ✨ Features

### Core Capabilities

- ✅ **Natural Language Parsing**: Understands arithmetic expressions in plain English
- ✅ **Four Operations**: Addition, subtraction, multiplication, and division
- ✅ **Number Support**: Handles numbers from 0-99 in word form
- ✅ **Compound Numbers**: Supports multi-word numbers (e.g., "twenty three")
- ✅ **Word Output**: Returns results as English words
- ✅ **Error Handling**: Comprehensive error messages for invalid input
- ✅ **Interactive Mode**: Real-time expression evaluation
- ✅ **Modular Design**: Clean separation of concerns across multiple modules

### Supported Operations

| Operation | Syntax | Example |
|-----------|--------|---------|
| Addition | `add <num> and <num>` | `add three and five` → `eight` |
| Subtraction | `subtract <num> and <num>` | `subtract ten and four` → `six` |
| Multiplication | `multiply <num> and <num>` | `multiply seven and eight` → `fifty six` |
| Division | `divide <num> and <num>` | `divide twenty and five` → `four` |

---

## 📁 Project Structure

```
WORDCALC/
│
├── classes/                    # Core module package
│   ├── __init__.py            # Package initializer
│   ├── WordCalcError.py       # Custom exception class
│   ├── Lexer.py               # Tokenization module
│   ├── Parser.py              # Syntax validation module
│   ├── Interpreter.py         # Execution engine module
│   └── WordCalc.py            # Main controller module
│
├── main.py                     # Entry point with CLI and tests
└── README.md                   # This file
```

### Directory Details

#### `classes/` Package
Contains all core WordCalc components as separate, reusable modules.

#### `main.py`
The application entry point that:
- Imports and uses WordCalc classes
- Provides interactive REPL mode
- Runs automated test cases
- Demonstrates usage examples

---

## 🚀 Installation

### Prerequisites

- **Python 3.7 or higher**
- No external dependencies required (pure Python standard library)

### Setup Steps

1. **Clone or Download the Project**
   ```bash
   git clone https://github.com/Spyd3r05/wordcalc.git
   cd wordcalc
   ```

2. **Verify Python Installation**
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Run WordCalc**
   ```bash
   python main.py
   # or
   python3 main.py
   ```
---

## 💻 Usage

### Interactive Mode

Run the program to enter interactive mode:

```bash
$ python main.py
```

You'll see:
```
============================================================
WordCalc - Natural Language Calculator
============================================================

[Test cases run automatically...]

============================================================
Interactive Mode - Enter 'quit' to exit
============================================================

WordCalc> add five and seven
Result: twelve

WordCalc> multiply nine and nine
Result: eighty one

WordCalc> quit
Goodbye!
```

### Programmatic Usage

You can also use WordCalc in your own Python scripts:

```python
from classes.WordCalc import WordCalc

# Create calculator instance
calc = WordCalc()

# Evaluate expressions
result = calc.evaluate("add ten and twenty")
print(result)  # Output: thirty

result = calc.evaluate("multiply three and seven")
print(result)  # Output: twenty one
```

### Command-Line One-Liners

```bash
# Evaluate a single expression
echo "add fifteen and twenty" | python main.py

# Process multiple expressions
cat expressions.txt | python main.py
```

---

## 📖 Grammar Specification

WordCalc follows a formal BNF (Backus-Naur Form) grammar:

```bnf
<expression> ::= <operation> <number> "and" <number>

<operation> ::= "add" | "subtract" | "multiply" | "divide"

<number> ::= <digit> | <teen> | <tens> | <compound>

<digit> ::= "zero" | "one" | "two" | "three" | "four" | "five" | 
            "six" | "seven" | "eight" | "nine"

<teen> ::= "ten" | "eleven" | "twelve" | "thirteen" | "fourteen" | 
           "fifteen" | "sixteen" | "seventeen" | "eighteen" | "nineteen"

<tens> ::= "twenty" | "thirty" | "forty" | "fifty" | 
           "sixty" | "seventy" | "eighty" | "ninety"

<compound> ::= <tens> <digit>
```

### Grammar Rules Explained

1. **Expression**: Must start with an operation, followed by two numbers connected with "and"
2. **Operation**: One of four keywords: add, subtract, multiply, divide
3. **Number**: Can be a single digit (0-9), teen (10-19), tens (20, 30, ..., 90), or compound (21-99)
4. **Compound**: Combination of tens + digit (e.g., "twenty three" = 23)

---

## 🏗️ Architecture

WordCalc implements a classic **three-stage interpreter pipeline**:

```
Input String
     ↓
┌─────────────┐
│   LEXER     │  → Tokenization
└─────────────┘
     ↓
   Tokens
     ↓
┌─────────────┐
│   PARSER    │  → Syntax Validation
└─────────────┘
     ↓
   AST/Data
     ↓
┌─────────────┐
│ INTERPRETER │  → Execution
└─────────────┘
     ↓
   Result
```

### Design Patterns

- **Modular Architecture**: Each component is a separate class with single responsibility
- **Exception Handling**: Custom `WordCalcError` for domain-specific errors
- **Facade Pattern**: `WordCalc` class provides simple interface to complex subsystems
- **Pipeline Pattern**: Data flows through Lexer → Parser → Interpreter stages

---

## 📚 Module Documentation

### 1. `WordCalcError.py`

**Purpose**: Custom exception class for all WordCalc errors

```python
class WordCalcError(Exception):
    """Raised when WordCalc encounters invalid input or execution errors"""
    pass
```

**Usage**:
```python
raise WordCalcError("Cannot divide by zero")
```

---

### 2. `Lexer.py`

**Purpose**: Breaks input strings into tokens (words)

**Key Methods**:

| Method | Description | Input | Output |
|--------|-------------|-------|--------|
| `__init__(text)` | Initialize with input string | `str` | - |
| `tokenize()` | Split text into tokens | - | `list[str]` |

**Example**:
```python
from classes.Lexer import Lexer

lexer = Lexer("add four and five")
tokens = lexer.tokenize()
# Result: ['add', 'four', 'and', 'five']
```

**Features**:
- Converts input to lowercase (case-insensitive)
- Strips whitespace
- Splits by spaces
- Validates non-empty input

---

### 3. `Parser.py`

**Purpose**: Validates token syntax and converts words to numbers

**Key Attributes**:

```python
WORD_TO_NUM = {
    'zero': 0, 'one': 1, ..., 'ninety': 90
}

OPERATIONS = {'add', 'subtract', 'multiply', 'divide'}
```

**Key Methods**:

| Method | Description | Returns |
|--------|-------------|---------|
| `parse()` | Main parsing function | `(operation, num1, num2)` |
| `parse_operation()` | Extract and validate operation | `str` |
| `parse_number()` | Convert word to integer | `int` |

**Example**:
```python
from classes.Parser import Parser

tokens = ['add', 'four', 'and', 'five']
parser = Parser(tokens)
operation, num1, num2 = parser.parse()
# Result: ('add', 4, 5)
```

**Features**:
- Validates BNF grammar compliance
- Handles compound numbers ("twenty three" → 23)
- Provides detailed error messages
- Consumes tokens sequentially

---

### 4. `Interpreter.py`

**Purpose**: Executes operations and converts results to words

**Key Attributes**:

```python
NUM_TO_WORD = {
    0: 'zero', 1: 'one', ..., 90: 'ninety'
}
```

**Key Methods**:

| Method | Description | Returns |
|--------|-------------|---------|
| `execute()` | Perform arithmetic operation | `int` |
| `number_to_words(num)` | Convert integer to words | `str` |
| `interpret()` | Execute and convert to words | `str` |

**Example**:
```python
from classes.Interpreter import Interpreter

interp = Interpreter('add', 4, 5)
result = interp.interpret()
# Result: 'nine'
```

**Features**:
- Handles four operations: +, -, *, //
- Converts results back to English
- Supports negative numbers
- Division by zero protection

---

### 5. `WordCalc.py`

**Purpose**: Main controller coordinating all components

**Key Methods**:

| Method | Description | Input | Output |
|--------|-------------|-------|--------|
| `evaluate(expression)` | Evaluate complete expression | `str` | `str` |

**Example**:
```python
from classes.WordCalc import WordCalc

calc = WordCalc()
result = calc.evaluate("multiply three and seven")
# Result: 'twenty one'
```

**Workflow**:
1. Creates `Lexer` and tokenizes input
2. Creates `Parser` and validates syntax
3. Creates `Interpreter` and executes
4. Returns result or error message

---

## 🎯 Examples

### Basic Arithmetic

```python
calc = WordCalc()

# Addition
calc.evaluate("add one and one")          # → "two"
calc.evaluate("add fifteen and twenty")   # → "thirty five"

# Subtraction
calc.evaluate("subtract ten and three")   # → "seven"
calc.evaluate("subtract five and five")   # → "zero"

# Multiplication
calc.evaluate("multiply six and seven")   # → "forty two"
calc.evaluate("multiply nine and nine")   # → "eighty one"

# Division
calc.evaluate("divide twenty and four")   # → "five"
calc.evaluate("divide fifty and ten")     # → "five"
```

### Compound Numbers

```python
# Using compound numbers (20+)
calc.evaluate("add twenty three and seventeen")    # → "forty"
calc.evaluate("multiply thirty two and two")       # → "sixty four"
calc.evaluate("subtract ninety nine and fifty")    # → "forty nine"
```

### Edge Cases

```python
# Zero handling
calc.evaluate("add zero and five")        # → "five"
calc.evaluate("subtract eight and eight") # → "zero"
calc.evaluate("multiply zero and ten")    # → "zero"

# Negative results
calc.evaluate("subtract five and ten")    # → "negative five"
```

---

## ⚠️ Error Handling

WordCalc provides clear, specific error messages for common mistakes:

### Syntax Errors

| Input | Error | Reason |
|-------|-------|--------|
| `add five` | `Expected 'and' but got 'None'` | Missing second operand |
| `five and three` | `Invalid operation: 'five'` | Missing operation keyword |
| `add five three` | `Expected 'and' but got 'three'` | Missing connector |
| `add five and` | `Expected a number but reached end` | Incomplete expression |

### Invalid Operations

| Input | Error |
|-------|-------|
| `plus three and five` | `Invalid operation: 'plus'` |
| `sum three and five` | `Invalid operation: 'sum'` |

### Invalid Numbers

| Input | Error |
|-------|-------|
| `add hundred and five` | `Unknown number word: 'hundred'` |
| `add 3 and 5` | `Unknown number word: '3'` |

### Mathematical Errors

| Input | Error |
|-------|-------|
| `divide ten and zero` | `Cannot divide by zero` |

### Handling Errors in Code

```python
from classes.WordCalc import WordCalc

calc = WordCalc()

result = calc.evaluate("divide ten and zero")
if result.startswith("Error:"):
    print("Invalid expression!")
else:
    print(f"Result: {result}")
```

---

## 🔧 Extending WordCalc

### Adding New Operations

**1. Update `Parser.py`:**
```python
OPERATIONS = {'add', 'subtract', 'multiply', 'divide', 'power'}  # Add 'power'
```

**2. Update `Interpreter.py`:**
```python
def execute(self):
    if self.operation == 'power':
        return self.num1 ** self.num2
    # ... existing code
```

### Adding Larger Numbers

**1. Update `Parser.py` to include hundreds:**
```python
WORD_TO_NUM = {
    # ... existing mappings
    'hundred': 100,
    'thousand': 1000
}
```

**2. Update parsing logic to handle compound hundreds:**
```python
def parse_number(self):
    # Add logic for "five hundred twenty three"
    pass
```

### Adding Variables

Create a new `VariableStore` class:

```python
class VariableStore:
    def __init__(self):
        self.variables = {}
    
    def set(self, name, value):
        self.variables[name] = value
    
    def get(self, name):
        return self.variables.get(name)
```

Extend grammar:
```bnf
<statement> ::= <assignment> | <expression>
<assignment> ::= "let" <name> "be" <number>
```

---

## 🧪 Testing

### Running Automated Tests

The `main.py` file includes comprehensive test cases:

```bash
python main.py
```

### Test Coverage

**Valid Expressions** (10 tests):
- Basic operations with single-digit numbers
- Operations with teen numbers
- Operations with tens numbers
- Operations with compound numbers
- Zero handling

**Error Cases** (4 tests):
- Missing operand
- Missing operation
- Invalid operation keyword
- Division by zero

### Writing Custom Tests

```python
from classes.WordCalc import WordCalc

def test_custom():
    calc = WordCalc()
    
    # Test case 1
    assert calc.evaluate("add two and two") == "four"
    
    # Test case 2
    assert calc.evaluate("multiply five and five") == "twenty five"
    
    print("All tests passed!")

test_custom()
```

### Unit Testing Each Module

```python
import unittest
from classes.Lexer import Lexer
from classes.Parser import Parser
from classes.Interpreter import Interpreter

class TestLexer(unittest.TestCase):
    def test_tokenization(self):
        lexer = Lexer("add three and five")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, ['add', 'three', 'and', 'five'])

class TestParser(unittest.TestCase):
    def test_parsing(self):
        parser = Parser(['add', 'three', 'and', 'five'])
        op, n1, n2 = parser.parse()
        self.assertEqual((op, n1, n2), ('add', 3, 5))

if __name__ == '__main__':
    unittest.main()
```

---

## 🎓 Learning Outcomes

Building WordCalc teaches fundamental concepts:

### Compiler/Interpreter Design
- **Lexical Analysis**: Breaking text into meaningful tokens
- **Syntax Analysis**: Validating structure against formal grammar
- **Semantic Analysis**: Executing operations and generating output

### Software Engineering
- **Modularity**: Separation of concerns across classes
- **Error Handling**: Comprehensive exception management
- **API Design**: Clean public interfaces

### Language Design
- **Grammar Definition**: Using BNF notation
- **Token Design**: Choosing keywords and syntax
- **Extensibility**: Planning for future features

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/awesome-feature
   ```
3. **Make Your Changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update README if needed
4. **Test Thoroughly**
5. **Submit a Pull Request**

### Contribution Ideas

- [ ] Add modulo operation (`mod`)
- [ ] Support decimal numbers
- [ ] Add parentheses for order of operations
- [ ] Implement variables (`let x be five`)
- [ ] Create web interface
- [ ] Build VSCode syntax highlighting extension

---

## 📝 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024 WordCalc Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- **BNF Grammar Notation**: Based on formal language theory
- **Interpreter Design**: Inspired by classic compiler construction techniques
- **Educational Purpose**: Created as a learning project for understanding programming language implementation

---

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Questions**: Open a discussion in GitHub Discussions
- **Email**: support@wordcalc.example.com (if applicable)

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Basic arithmetic operations
- ✅ Numbers 0-99
- ✅ Interactive mode
- ✅ Error handling

### Version 1.1 (Planned)
- [ ] Support for numbers 100-999
- [ ] Floating-point division
- [ ] More operations (power, modulo)

### Version 2.0 (Future)
- [ ] Variable assignment
- [ ] Multiple operations per line
- [ ] Functions/procedures
- [ ] File execution mode

---

## 📊 Project Statistics

- **Lines of Code**: ~350
- **Modules**: 5 classes
- **Test Cases**: 14
- **Supported Numbers**: 0-99
- **Operations**: 4
- **Python Version**: 3.7+

---

## 🔍 FAQs

### Q: Can I use numbers in digit form (e.g., "add 3 and 5")?
**A**: No, WordCalc only accepts word form. This is by design to demonstrate natural language processing.

### Q: What happens with large results like 100+?
**A**: Currently, results ≥100 are returned as digit strings (e.g., "120"). A future version will support word conversion.

### Q: Does it support negative numbers as input?
**A**: Not currently, but negative results are supported (e.g., "subtract ten and twenty" → "negative ten").

### Q: Is it case-sensitive?
**A**: No! You can use "ADD", "Add", or "add" - all work the same.

### Q: Can I chain operations?
**A**: Not yet. Each expression is currently limited to one operation.

---

**Made with ❤️ for learning programming language design**

---

*Last Updated: February 2026*
*Version: 1.0.0*#
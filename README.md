# Calculator

This project implements a `Calculator` class in Python that can evaluate algebraic expressions and perform continuous evaluations. The calculator supports basic arithmetic operations and follows the principles of Object-Oriented Programming (OOP).

## Features

- **Evaluate Algebraic Expressions**: Enter and evaluate algebraic expressions.
- **Continuous Evaluation**: Continue evaluating expressions by entering operators and values.

## Classes

### `Operator`

Represents an arithmetic operator with its properties.

#### Attributes

- `name`: The name of the operator.
- `symbol`: The symbol of the operator.
- `function`: The function that performs the operation.
- `precedence`: The precedence of the operator.
- `associativity`: The associativity of the operator (left or right).

### `Calculator`

Main class that handles the evaluation of expressions.

#### Attributes

- `operations`: Dictionary of supported operators.
- `SUPPORTED_OPERATORS`: String of supported operator symbols.
- `SIGN`: String of sign symbols.
- `PARENTHESES`: String of parentheses symbols.
- `MODE_OPTIONS`: String of mode options.
- `EXIT_COMMAND`: Command to exit the current mode.

#### Methods

- `main()`: Main method to start the calculator.
- `_menu_mode()`: Displays the menu and sets the mode.
- `_evaluate_algebraic_expression(single: bool = False)`: Evaluates an algebraic expression.
- `_continuous_evaluation()`: Performs continuous evaluation.
- `_get_expression(prompt: str)`: Gets an expression from the user.
- `_validate_expression()`: Validates the entered expression.
- `_validate_for_continuous_evaluation()`: Validates the expression for continuous evaluation.
- `_evaluate_algebraic_expression_preprocessor(start_index: int = 0)`: Preprocesses the expression for evaluation.
- `_continuous_evaluation_preprocessor()`: Preprocesses the expression for continuous evaluation.
- `_infix_to_postfix()`: Converts infix expression to postfix notation.
- `_evaluate_postfix()`: Evaluates the postfix expression.

## Usage

1. Run the `main()` method from the `Calculator` class.
2. Choose a mode:
   - `1`: Evaluate an algebraic expression.
   - `2`: Continuous evaluation.
3. Follow the prompts to enter expressions or operators and values.

## Example

```python
Calculator().main()
```

## Requirements

- Python 3.x

## License

This project is licensed under the MIT License.

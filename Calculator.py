class Operator:
    def __init__(self, name, symbol, function, precedence, associativity):
        self.name = name
        self.symbol = symbol
        self.function = function
        self.precedence = precedence
        self.associativity = associativity


def _is_number(test_string):
    try:
        float(test_string)
        return True
    except ValueError:
        return False


class Calculator:
    operations = {
        '+': Operator("addition", '+', lambda n1, n2: n1 + n2, 2, "left"),
        '-': Operator("subtraction", '-', lambda n1, n2: n1 - n2, 2, "left"),
        '*': Operator("multiplication", '*', lambda n1, n2: n1 * n2, 3, "left"),
        '/': Operator("division", '/', lambda n1, n2: n1 / n2 if n2 != 0 else ZeroDivisionError, 3, "left"),
        '^': Operator("power", '^', lambda n1, n2: n1 ** n2, 4, "right")
    }

    _supported_operators = "+-*/^"
    _sign = "+-"
    _parentheses = "()"

    def __init__(self):
        self.__expression = None

    # TODO: create menu, add continuous evaluation
    # TODO: add keyboard actions, esc for "back" arrows to browse expression history

    def evaluate_algebraic_expression(self):
        while True:
            isvalid = {"value": False, "msg": None}
            while not isvalid["value"]:
                if isvalid["msg"] is not None:
                    print(isvalid["msg"])
                print("Enter an algebraic expression to evaluate:")
                self.get_expression()
                if self.__expression == "back":
                    return
                isvalid = self.validate()
            self.expression_preprocessor()
            self.infix_to_postfix()
            print(self.evaluate_postfix())

    def get_expression(self):
        self.__expression = input()

    def validate(self):
        if self.__expression == '':
            return {"value": False, "msg": "Expression is empty\n"}
        if self.__expression[-1] in self._supported_operators or self.__expression[-1] == 'e':
            return {"value": False, "msg": "Expression cannot end with an operator\n"}
        parentheses_counter = 0

        for i in range(len(self.__expression)):
            current = self.__expression[i]
            number: bool = _is_number(current)
            operator: bool = current in self._supported_operators
            parentheses: bool = current in self._parentheses

            if current == 'e' and i < len(self.__expression) - 1:
                before = self.__expression[i - 1]
                after = self.__expression[i + 1]
                if not _is_number(before) or not _is_number(after):
                    return {"value": False, "msg": f"Invalid characters in the entered expression: {current}"}
            elif not (number or operator or parentheses or current == '.'):
                return {"value": False, "msg": f"Invalid characters in the entered expression: {current}"}
            if current == '(':
                parentheses_counter += 1
            elif current == ')':
                parentheses_counter -= 1

        if parentheses_counter != 0:
            return {"value": False, "msg": "Mismatched parentheses"}

        return {"value": True, "msg": "Validation successful"}

    def expression_preprocessor(self):
        preprocessed_expression = ''
        for i in range(len(self.__expression)):
            current = self.__expression[i]
            if i == 0:  # First character
                if (first := self.__expression[0]) == '(':
                    preprocessed_expression += self.__expression[0] + ' '
                elif _is_number(first) or first in Calculator._sign:
                    preprocessed_expression += current
                elif (first in Calculator._supported_operators) and first not in Calculator._sign:
                    return Exception("Expression cannot start with an operator")
            else:  # Middle elements
                if (current in Calculator._supported_operators + Calculator._parentheses) and (current not in Calculator._sign):
                    preprocessed_expression += f" {current} "

                elif current in Calculator._sign and _is_number(self.__expression[i - 1]) and _is_number(self.__expression[i + 1]):
                    preprocessed_expression += f" {current} "

                elif current in Calculator._sign and (self.__expression[i - 1] == ')' or self.__expression[i + 1] == '('):
                    preprocessed_expression += f" {current} "
                else:
                    preprocessed_expression += self.__expression[i]

        self.__expression = preprocessed_expression.split()

    def infix_to_postfix(self):
        expression_in_postfix: list = []
        operator_stack = []
        for elem in self.__expression:
            if _is_number(elem):
                expression_in_postfix.append(elem)
            if elem in Calculator.operations.keys():
                while len(operator_stack) > 0 and operator_stack[-1] != '(' and (Calculator.operations[operator_stack[-1]].precedence > Calculator.operations[elem].precedence or (
                        Calculator.operations[operator_stack[-1]].precedence == Calculator.operations[elem].precedence) and (Calculator.operations[elem].associativity == "left")):
                    expression_in_postfix.append(operator_stack.pop())
                operator_stack.append(elem)
            if elem == '(':
                operator_stack.append(elem)
            if elem == ')':
                assert len(operator_stack) != 0, "Operator stack is empty"
                while operator_stack[-1] != '(':
                    expression_in_postfix.append(operator_stack.pop())
                assert operator_stack[-1] == "(", "Mismatched parentheses"
                del operator_stack[-1]
        while len(operator_stack) != 0:
            assert operator_stack[-1] != '(', "Mismatched parentheses"
            expression_in_postfix.append(operator_stack.pop())

        self.__expression = expression_in_postfix

    def evaluate_postfix(self) -> float:
        print(self.__expression)
        calculation_stack = []
        for elem in self.__expression:
            if _is_number(elem):
                calculation_stack.append(float(elem))
            else:
                n1 = float(calculation_stack.pop())
                n2 = float(calculation_stack.pop())
                calculation_stack.append(Calculator.operations[elem].function(n2, n1))

        return calculation_stack[0]


c = Calculator()
c.evaluate_algebraic_expression()

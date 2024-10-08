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
        '/': Operator("division", '/', lambda n1, n2: n1 / n2 if n2 != 0 else float('inf'), 3, "left"),
        '^': Operator("power", '^', lambda n1, n2: n1 ** n2, 4, "right")
    }

    SUPPORTED_OPERATORS = ''.join(operations.keys())
    SIGN = "+-"
    PARENTHESES = "()"
    MODE_OPTIONS = "12back"

    def __init__(self):
        self.__mode = None
        self.__expression = None

    def main(self):
        while True:
            self.menu_mode()
            match self.__mode:
                case "1":
                    self.evaluate_algebraic_expression()
                case "2":
                    self.continuous_evaluation()
                case "back":
                    print("Exiting")
                    return

    def menu_mode(self):
        mode = "None"
        while mode not in self.MODE_OPTIONS:
            mode = input("Choose a mode from the list below (1):\n"
                         "1) Evaluate an algebraic expression\n"
                         "2) Continuous evaluation\n")
        self.__mode = mode

    def evaluate_algebraic_expression(self, single: bool = False):
        print("Type 'back' to return to the main menu")
        while True:
            self.get_expression("Enter an algebraic expression to evaluate:\n")
            if self.__expression == "back":
                return
            self.validate_expression()
            try:
                self.evaluate_algebraic_expression_preprocessor()
            except Exception as e:
                print(e)
                continue
            self.evaluate_algebraic_expression_preprocessor()
            self.infix_to_postfix()
            self.evaluate_postfix()
            print(self.__expression)
            if single:
                return

    def continuous_evaluation(self):
        self.evaluate_algebraic_expression(single=True)
        result = self.__expression
        while True:
            self.get_expression("Enter an operator and a value to continue evaluation:\n")
            if self.__expression == "back":
                return
            try:
                self.validate_for_continuous_evaluation()
            except Exception as e:
                print(e)
                continue
            self.continuous_evaluation_preprocessor()
            self.__expression.insert(0, result)
            self.infix_to_postfix()
            self.evaluate_postfix()
            print(self.__expression)
            result = self.__expression

    def get_expression(self, prompt: str):
        isvalid = {"value": False, "msg": None}
        while not isvalid["value"]:
            if isvalid["msg"] is not None:
                print(isvalid["msg"])
            self.__expression = input(prompt)
            isvalid = {"value": True, "msg": "Exiting"} if self.__expression == "back" else self.validate_expression()

    def validate_expression(self):
        if self.__expression == '':
            return {"value": False, "msg": "Expression is empty\n"}
        if self.__expression[-1] in self.SUPPORTED_OPERATORS or self.__expression[-1] == 'e':
            return {"value": False, "msg": "Expression cannot end with an operator\n"}
        parentheses_counter = 0

        for i in range(len(self.__expression)):
            current = self.__expression[i]
            number: bool = _is_number(current)
            operator: bool = current in self.SUPPORTED_OPERATORS
            parentheses: bool = current in self.PARENTHESES

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

    def validate_for_continuous_evaluation(self):
        if self.__expression[0] not in self.SUPPORTED_OPERATORS:
            raise Exception("First element must be an operator")

    def evaluate_algebraic_expression_preprocessor(self, start_index: int = 0):
        preprocessed_expression = ''
        for i in range(start_index, len(self.__expression)):
            current = self.__expression[i]
            if i == 0:  # First character
                if (first := self.__expression[0]) == '(':
                    preprocessed_expression += self.__expression[0] + ' '
                elif _is_number(first) or first in Calculator.SIGN:
                    preprocessed_expression += current
                elif (first in Calculator.SUPPORTED_OPERATORS) and first not in Calculator.SIGN:
                    raise Exception("Expression cannot start with an operator")
            else:  # Middle elements
                if (current in Calculator.SUPPORTED_OPERATORS + Calculator.PARENTHESES) and (current not in Calculator.SIGN):
                    preprocessed_expression += f" {current} "

                elif current in Calculator.SIGN and _is_number(self.__expression[i - 1]) and _is_number(self.__expression[i + 1]):
                    preprocessed_expression += f" {current} "

                elif current in Calculator.SIGN and (self.__expression[i - 1] == ')' or self.__expression[i + 1] == '('):
                    preprocessed_expression += f" {current} "
                else:
                    preprocessed_expression += self.__expression[i]

        self.__expression = preprocessed_expression.split()

    def continuous_evaluation_preprocessor(self):
        operator, self.__expression = [self.__expression[0]], self.__expression[1:]
        self.evaluate_algebraic_expression_preprocessor()
        self.__expression = operator + self.__expression

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

    def evaluate_postfix(self):
        print(self.__expression)
        calculation_stack = []
        for elem in self.__expression:
            if _is_number(elem):
                calculation_stack.append(float(elem))
            else:
                n1 = float(calculation_stack.pop())
                n2 = float(calculation_stack.pop())
                calculation_stack.append(Calculator.operations[elem].function(n2, n1))

        self.__expression = calculation_stack[0]


if __name__ == "__main__":
    Calculator().main()

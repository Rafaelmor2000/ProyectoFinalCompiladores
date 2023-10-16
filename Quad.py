class Quad:
    def __init__(self, operator, operand1, operand2, temp) -> None:
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.temp = temp

    def fill(self, temp) -> None:
        self.temp = temp

    def __str__(self):
        return f"[{self.operator}, {self.operand1.get('id')}, {self.operand2.get('id')}, {self.temp}]"

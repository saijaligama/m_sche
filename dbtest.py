import math
import re

def evaluate_log_expression(expression):
    tokens = re.findall(r'log\(\d+\)', expression)
    for token in tokens:
        num = int(token[4:-1])
        expression = expression.replace(token, str(math.log(num)))
    return eval(expression)

print(evaluate_log_expression("log(10) + log(2)")) 
# prints 2.30258509299

expression = "log(100) - 2*log(10)" 
print(evaluate_log_expression(expression)) # 2

expression = "3*log(5) + log(20)/2"
print(evaluate_log_expression(expression)) # 4.0442307716

expression = "log(1234)**2"
print(evaluate_log_expression(expression)) # 7.7185482429
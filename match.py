def find_mismatched_brackets(string):
    stack = []
    mismatched_positions = []
    
    for i, char in enumerate(string):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                mismatched_positions.append(i)
    
    for i in stack:
        mismatched_positions.append(i)

    # 不匹配位置按顺序排列
    mismatched_positions.sort()
    
    return mismatched_positions

def generate_output(string, mismatched_positions):
    output = ''
    for i, char in enumerate(string):
        if i in mismatched_positions:
            if char == '(':
                output += 'x'
            elif char == ')':
                output += '?'
        else:
            output += ' '
    return output

if __name__ == '__main__':

    # 测试用例
    test_cases = [
        "bge)))))))))",
        "((IIII))))))",
        "()()()()(uuu",
        "))))UUUU((()"
    ]

    for test_case in test_cases:
        mismatched_positions = find_mismatched_brackets(test_case)
        print(test_case)
        print(generate_output(test_case, mismatched_positions))


import re

"""
Rules:
The function will return the correct conversion if the supplied problems are properly formatted, otherwise, it will return a string that describes an error that is meaningful to the user.

Situations that will return an error:
If there are too many problems supplied to the function. The limit is five, anything more will return:
Error: Too many problems.
The appropriate operators the function will accept are addition and subtraction. Multiplication and division will return an error. Other operators not mentioned in this bullet point will not need to be tested. The error returned will be:
Error: Operator must be '+' or '-'.
Each number (operand) should only contain digits. Otherwise, the function will return:
Error: Numbers must only contain digits.
Each operand (aka number on each side of the operator) has a max of four digits in width. Otherwise, the error string returned will be:
Error: Numbers cannot be more than four digits.

Display:
If the user supplied the correct format of problems, the conversion you return will follow these rules:
    There should be a single space between the operator and the longest of the two operands, 
    the operator will be on the same line as the second operand, both operands will be in the 
    same order as provided (the first will be the top one and the second will be the bottom.
Numbers should be right-aligned.
There should be four spaces between each problem.
There should be dashes at the bottom of each problem. 
The dashes should run along the entire length of each problem individually. (The example above shows what this should look like.)

  32         1      9999      523
+  8    - 3801    + 9999    -  49
----    ------    ------    -----
  40     -3800     19998      474

"""

def arithmetic_arranger(problems, drive_result=False):
    arranged_problems = ""
    validation = validate_problem(problems)

    if validation == None:
        prob_dict_lst = parse_and_get_problems(problems, drive_result)
        # print(prob_dict_lst)
        first_line = ""
        second_line = ""
        third_line = ""
        fourth_line = ""

        operandA = "Operand0"
        operandB = "Operand1"
        spaces_bt_two_problems = 4

        for each_prob in prob_dict_lst:
            max_op_size = get_max_operand_size(each_prob)
            is_max_opA = is_max_size_op(operandA, max_op_size, each_prob)

            # First Line.
            # Space for operator and 1 extra space between op and large operand.
            first_line = first_line + spaces(2)
            if is_max_opA == False:
                extra_spaces = max_op_size - each_prob[operandA+"Length"]
                first_line = first_line + spaces(extra_spaces)
            first_line = first_line + str(each_prob[operandA])
            # Spaces between two problems.
            first_line = first_line + spaces(spaces_bt_two_problems)

            # Second Line.
            second_line = second_line + each_prob["Operator"]
            second_line = second_line + spaces(1)
            if is_max_opA == True:
                extra_spaces = max_op_size - each_prob[operandB+"Length"]
                second_line = second_line + spaces(extra_spaces)
            second_line = second_line + str(each_prob[operandB])
            # Spaces between two problems.
            second_line = second_line + spaces(spaces_bt_two_problems)

            # Third Line.
            third_line = third_line + dashes(max_op_size + 2)
            # Spaces between two problems.
            third_line = third_line + spaces(spaces_bt_two_problems)

            # Fourth Line.
            if drive_result == True:
                result = str(each_prob["Result"])
                extra_spaces = max_op_size + 2 - len(result)
                fourth_line = fourth_line + spaces(extra_spaces)
                fourth_line = fourth_line + result
                # Spaces between two problems.
                fourth_line = fourth_line + spaces(spaces_bt_two_problems)

        # Final result string.
        arranged_problems = first_line.rstrip() + "\n" + second_line.rstrip() + \
            "\n" + third_line.rstrip()
        if drive_result == True:
            arranged_problems = arranged_problems + "\n" + fourth_line.rstrip()
    else:
        return validation

    return arranged_problems


def dashes(n):
    return "-"*n


def spaces(n):
    return " "*n


def is_max_size_op(op_key, max_size, prob_dict):
    op_len = prob_dict[op_key+"Length"]
    if op_len == max_size:
        return True
    else:
        return False


def get_max_operand_size(prob_dict):
    operand_size = prob_dict["NumberOfOperands"]
    max_size = 0
    for op_index in range(0, operand_size):
        op_key = get_operand_key(op_index)
        op_len = prob_dict[op_key+"Length"]
        if max_size < op_len:
            max_size = op_len
    return max_size


"""
    Input - ["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]
    Arrange in the following data structure for better handling.
    List of dictionaires. Each dictionary represents one problem.
    [
        {
            "Operand0":25,
            "Operand0Length":2,
            "Operand1":23,
            "Operand1Length":2,
            "Operator":"+",
            "NumberOfOperands": 2,
            "Result":48
        }
    ]
"""


def parse_and_get_problems(problems, drive_result):
    problems_list = list()
    for problem in problems:
        problem_dict = dict()
        problem = problem.strip()
        prob_details = problem.split(" ")
        op_position = 0
        for each_elm in prob_details:
            each_elm = each_elm.strip()
            if each_elm.isdigit():
                op_key = get_operand_key(op_position)
                problem_dict[op_key+"Length"] = len(each_elm)
                problem_dict[op_key] = int(each_elm)
                op_position = op_position + 1
            else:
                problem_dict["Operator"] = each_elm

        problem_dict["NumberOfOperands"] = op_position
        if drive_result == True:
            calculate_result(problem_dict)
        problems_list.append(problem_dict)

    return problems_list


def calculate_result(prob_dict):
    operator = prob_dict["Operator"]
    operand_size = prob_dict["NumberOfOperands"]

    result = 0
    if operator == "+":
        addition_result = 0
        for op_index in range(0, operand_size):
            addition_result = addition_result + \
                prob_dict[get_operand_key(op_index)]
        result = addition_result
    elif operator == "-":

        sub_result = prob_dict[get_operand_key(0)]

        for op_index in range(1, operand_size):
            sub_result = sub_result - prob_dict[get_operand_key(op_index)]

        result = sub_result
    elif operator == "*":
        mul_result = 1
        for op_index in range(0, operand_size):
            mul_result = mul_result * prob_dict[get_operand_key(op_index)]
        result = mul_result
    else:
        raise "Unexpected operator found."

    prob_dict["Result"] = result


def get_operand_key(op_index):
    return "Operand{}".format(op_index)

# Performs all the validations before preparing the problem display.


def validate_problem(problems):
    validation_result = None

    if len(problems) == 0:
        return "Error: No problem is provided."

    # Rule 1: Number of problems should not be more than 5.
    if len(problems) > 5:
        validation_result = "Error: Too many problems."
        return validation_result

    for problem in problems:

        # Rule 2: Allows only '+' and '-' operators
        if is_contains_valid_operators(problem) == False:
            validation_result = "Error: Operator must be '+' or '-'."
            break

        # Rule 3: Verify each problem should contains only digits.
        if is_all_digits(problem) == False:
            validation_result = "Error: Numbers must only contain digits."
            break

        # Rule 4: Each operand (aka number on each side of the operator) has a max of four digits in width.
        if is_valid_operand_size(problem) == False:
            validation_result = "Error: Numbers cannot be more than four digits."
            break

    return validation_result

# Verify each operand size.
# Passed the problem string not an list


def is_valid_operand_size(problem):
    searchregix = "\S+[0-9]*\S+"
    found = re.findall(searchregix, problem)
    for operand in found:
        if len(operand) > 4:
            return False
    return True

# Each number (operand) should only contain digits.


def is_all_digits(problem):
    searchregix = "[a-zA-Z]+"
    found = re.findall(searchregix, problem)
    if len(found) > 0:
        return False
    else:
        return True


# It allows only + and - operators. Verfiy in each
# problem, do we have an valid operators. If we have multiplication and division then
# return false.
#"32 + 8"
def is_contains_valid_operators(problem):
    searchregix = "[*/%]"
    found = re.findall(searchregix, problem)
    if len(found) > 0:
        return False
    else:
        # Check if it contains + or - atleast once.
        searchregix = "[+,-]+?"
        found = re.findall(searchregix, problem)
        if len(found) != 1:
            return False
        return True


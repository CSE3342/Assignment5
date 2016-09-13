#Assignment 5 - Interpreter
#Preston Tighe
#CSE 3342
#9-12-16

from keyword import iskeyword
import json

print("REPL: enter statement | expression | bye | mem")
var_dict = {}


def is_valid_variable_name(name):
    return name.isidentifier() and not iskeyword(name)


def is_int(s):
    try:
        temp = int(s)
        return True
    except:
        return False


def is_valid_var(s):
 return s in var_dict


def eval_statement(instr):
    tokens = instr.split('=')
    tokens = [tok.strip() for tok in tokens]

    # Parse RHS
    if len(tokens) == 2:  # assignment
        # Check valid variable name
        if is_valid_variable_name(tokens[0]):
            # Assigns value in dict
            var_dict[tokens[0]] = parse_rhs(tokens[1])
            return var_dict[tokens[0]]
        else:
            raise Exception('Invalid variable name: `' + tokens[0] + '`')
    elif len(tokens) == 1:  # inline arithmetic
        if tokens[0]:
            return parse_rhs(tokens[0])
        else:
            raise Exception('Empty statement.')
    else:
        raise Exception('Invalid statement `' + instr + '`')


def parse_rhs(rhs):
    final_val = None
    tokens = rhs.split('+')
    tokens = [tok.strip() for tok in tokens]

    for token in tokens:
        token = token.strip()
        if token:
            if final_val is None:
                final_val = 0

            if is_int(token):
                final_val += int(token)
            elif is_valid_variable_name(token):
                if token in var_dict and var_dict[token]:
                    final_val += var_dict[token]
                else:
                    raise Exception('`' + token + '` not declared or defined.')
            else:
                raise Exception('Invalid statement: `' + rhs + '`')
        else:
            raise Exception('Right hand side of assignment is empty.')

    if final_val is None:
        raise Exception('Invalid statement: `' + rhs + '`')
    else:
        return final_val


def memory_json():
    return json.dumps(var_dict)

while True:
    try:
        instr = input('%')
        if instr == 'bye':
            print('The program will exit now.')
            break
        elif instr == 'mem':
            print(memory_json())
        else:
            print(eval_statement(instr))
    except Exception as error:
        print('Error: ' + str(error))


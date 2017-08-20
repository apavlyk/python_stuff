#! /usr/bin/python

"""
Script to check if brackets in the string are closed
"""

def check_brackets_closed(expression):
    brackets = {")": "(", "]": "[", "}": "{"}
    found_brackets = []
    for ch in expression:
        # append to list open bracket
        if ch in brackets.values():
            found_brackets.append(ch)
        # if there are no opened bracket anymore and get closed bracket
        elif ch in brackets and not found_brackets:
            return False
        elif ch in brackets and found_brackets:
            # if there are opened brackets check if last one corresponds to closed bracket
            if found_brackets[-1] == brackets[ch]:
                found_brackets.pop()
            else:
                return False

    return not len(found_brackets)

if __name__ == '__main__':
    assert check_brackets_closed("((5+3)*2+1)") == True, "Simple"
    assert check_brackets_closed("{[(3+1)+2]+}") == True, "Different types"
    assert check_brackets_closed("(3+{1-1)}") == False, ") is alone inside {}"
    assert check_brackets_closed("[1+1]+(2*2)-{3/3}") == True, "Different operators"
    assert check_brackets_closed("(({[(((1)-2)+3)-3]/3}-3)") == False, "One is redundant"
    assert check_brackets_closed("2+3") == True, "No brackets, no problem"

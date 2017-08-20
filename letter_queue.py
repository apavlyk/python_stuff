#! /usr/bin/python

"""
Script to emulate queue process using string containing "POP", "PUSH" commands
"""

from collections import deque


def letter_queue(commands):
    queue = deque()

    for command in commands:
        if "PUSH" in command.upper():
            queue.append(command.split()[-1])
        elif command.upper() == "POP" and queue:
            queue.popleft()

    return "".join(queue)

if __name__ == '__main__':
    assert letter_queue(["PUSH A", "POP", "POP", "PUSH Z", "PUSH D", "PUSH O", "POP", "PUSH T"]) == "DOT", "dot example"
    assert letter_queue(["POP", "POP"]) == "", "Pop, Pop, empty"
    assert letter_queue(["PUSH H", "PUSH I"]) == "HI", "Hi!"
    assert letter_queue([]) == "", "Nothing"

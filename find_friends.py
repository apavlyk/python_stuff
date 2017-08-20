#! /usr/bin/python

"""
Script to find if users are connected between each other
"""

found_users = set()


def find_connection(network, users):
    rel_users = set()
    global found_users
    found_users.update(users)
    if users:
        for connection in network:
            for user in users:
                if user in connection:
                    rel_users.add(connection.split('-')[0] if connection.split('-')[0] != user else connection.split('-')[1])

        find_connection(network, rel_users - found_users)

    return rel_users


def check_connection(network, first, second):

    global found_users
    found_users = set()

    find_connection(network, [first])

    return second in found_users


if __name__ == '__main__':
    assert check_connection(
        ("dr101-mr99", "mr99-out00", "dr101-out00", "scout1-scout2",
         "scout3-scout1", "scout1-scout4", "scout4-sscout", "sscout-super"),
        "scout2", "scout3") == True, "Scout Brotherhood"
    assert check_connection(
        ("dr101-mr99", "mr99-out00", "dr101-out00", "scout1-scout2",
         "scout3-scout1", "scout1-scout4", "scout4-sscout", "sscout-super"),
        "super", "scout2") == True, "Super Scout"
    assert check_connection(
        ("dr101-mr99", "mr99-out00", "dr101-out00", "scout1-scout2",
         "scout3-scout1", "scout1-scout4", "scout4-sscout", "sscout-super"),
        "dr101", "sscout") == False, "I don't know any scouts."

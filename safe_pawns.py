#! /usr/bin/python

"""
Script to check how many pawns are safe (defended by other pawns)
"""

def safe_pawns(pawns):
    safe_pawns = 0
    pawns = [pawn.lower() for pawn in pawns]
    for pawn in pawns:
        column = ord(pawn[0])
        row = str(int(pawn[1])-1)
        if (chr(column-1) + row in pawns) or (chr(column+1) + row in pawns):
            safe_pawns += 1

    return safe_pawns

if __name__ == '__main__':
    assert safe_pawns({"b4", "d4", "f4", "c3", "e3", "g5", "d2"}) == 6
    assert safe_pawns({"b4", "c4", "d4", "e4", "f4", "g4", "e5"}) == 1

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
AOnlyOne = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))) # A is either a Knight or a Knave

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
BOnlyOne = And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))) # B is either a Knight or a Knave

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
COnlyOne = And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))) # C is either a Knight or a Knave


def Says(knight, knave, saying):
    knowledge = And(
        Or(
            Not(knight),
            saying
        ), 
        Or(
            Not(knave),
            Not(saying)
        )
    )
    return knowledge


# Puzzle 0
# A says "I am both a knight and a knave."
P0_Asaying = And(AKnight, AKnave)
knowledge0 = And(AOnlyOne, Says(AKnight, AKnave, P0_Asaying))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
P1_Asaying = And(AKnave, BKnave)
P1_OnlyOne = And(AOnlyOne, BOnlyOne)
knowledge1 = And(P1_OnlyOne, Says(AKnight, AKnave, P1_Asaying))

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# A says "We are the same kind."
P2_Asaying = Or(
    And(
        AKnight,
        BKnight
    ), And(
        AKnave,
        BKnave
    )
)

# B says "We are of different kinds."
P2_Bsaying = Not(P2_Asaying)

P2_OnlyOne = And(AOnlyOne, BOnlyOne)

knowledge2 = And(
    P2_OnlyOne,
    Says(AKnight, AKnave, P2_Asaying),
    Says(BKnight, BKnave, P2_Bsaying)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# A says either "I am a knight." or "I am a knave.", but you don't know which.
P3_Asaying1 = AKnight
P3_Asaying2 = AKnave
P3_Asaying = And(Or(P3_Asaying1, P3_Asaying2), Not(And(P3_Asaying1, P3_Asaying2)))

# B says "A said 'I am a knave'."
P3_Bsaying1 = Says(AKnight, AKnave, AKnight)
# B says "C is a knave."
P3_Bsaying2 = CKnave
P3_Bsaying = And(P3_Bsaying1, P3_Bsaying2)

# C says "A is a knight."
P3_Csaying = AKnight

P3_OnlyOne = And(AOnlyOne, BOnlyOne, COnlyOne)

knowledge3 = And(
    P3_OnlyOne,
    # A says
    Says(AKnight, AKnave, P3_Asaying),
    # B says
    Says(BKnight, BKnave, P3_Bsaying),
    # C says
    Says(CKnight, CKnave, P3_Csaying)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

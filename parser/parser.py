import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | AdjP | Det N | Det AdjP | NP P NP | NP Conj NP
AdjP -> Adj N | Adj AdjP
VP -> V | VP NP | VP Adv | Adv VP | VP Conj VP | VP P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    word_list = nltk.word_tokenize(sentence)  # tokenize word from sentence and store in list
    ret_list = []  # returning list
    for word in word_list:
        word = word.lower()
        # if the word is all alphabets, append to ret_list
        if word.isalpha():
            ret_list.append(word)
        # else, check if there is any alphabet. If so, append to ret_list. If not, skip.
        else:
            check = False
            for char in word:
                if char.isalpha():
                    check = True
                    ret_list.append(word)
                    break
    return ret_list
                        

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    tree_list = []  # returning list
    # iterate through each subtree of tree
    for s in tree.subtrees():
        # if the subtree has a lebel of 'NP' and height of 2 (i.e. a leaf), add it to tree_list
        if s.label() == 'NP':
            if s.height() == 2:
                tree_list.append(s)
            # else, iterate through children and apply recursion if child is 'NP' 
            else:
                check = False
                for child in s:
                    if child.label() == 'NP':
                        check = True
                        np_chunk(child)
                if check == False:
                    tree_list.append(s)
        # if subtree is not NP, iterate through children and apply recursion if child is NP
        else:
            if s.height() == 2:
                continue
            for child in s:
                if child.label() == 'NP':
                    check = True
                    np_chunk(child)
    return tree_list               


if __name__ == "__main__":
    main()

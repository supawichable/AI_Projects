import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


def unique(list1):
    unique_list = []
    for item in list1:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        # List of cells available to move
        self.availables = []
        for i in range(width):
            for j in range(height):
                self.availables.append((i, j))

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as a move that has been made
        self.moves_made.add(cell)
        # mark the cell as safe
        self.mark_safe(cell)
        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        # 1. making logical sentence from surrounding cells
        cells = set()
        for i in [-1, 0, 1]:
            if (cell[0] + i >= 0) and (cell[0] + i <= self.width - 1):
                for j in [-1, 0, 1]:
                    if (cell[1] + j >= 0) and (cell[1] + j <= self.height - 1):
                        new_cell = (cell[0] + i, cell[1] + j)
                        if not (new_cell in self.moves_made):
                            cells.add(new_cell)
        new_sentence = Sentence(cells, count)
        # 2. check if new sentence is a subset of any sentence in knowledge (or vice versa), if so add just the difference to knowledge
        check = 0
        adding_sentence_list = []
        removing_sentence_list = []
        if len(self.knowledge) != 0:
            for sentence in self.knowledge:
                if sentence.cells == new_sentence.cells:
                    check = 1
                else:
                    if sentence.cells.issubset(new_sentence.cells): # sentence in knowledge is a subset of new sentence
                        adding_sentence_cells = new_sentence.cells.difference(sentence.cells)
                        adding_sentence_count = new_sentence.count - sentence.count
                        adding_sentence = Sentence(adding_sentence_cells, adding_sentence_count)
                        adding_sentence_list.append(adding_sentence)
                        check = 1
                    elif new_sentence.cells.issubset(sentence.cells): # new sentence is a subset of sentence in knowledge 
                        adding_sentence_cells = sentence.cells.difference(new_sentence.cells)
                        adding_sentence_count = sentence.count - new_sentence.count
                        adding_sentence = Sentence(adding_sentence_cells, adding_sentence_count)
                        adding_sentence_list.append(adding_sentence)
                        check = 1
            self.knowledge += adding_sentence_list
            self.knowledge = unique(self.knowledge) # remove the redundants
            if check == 0:
                    self.knowledge.append(new_sentence)
        else:
            self.knowledge.append(new_sentence)
        # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:
            if sentence.cells == None:
                self.knowledge.remove(sentence)
            new_safes = sentence.known_safes().difference(self.safes)
            new_mines = sentence.known_mines().difference(self.mines)
            if len(new_safes) != 0:
                for new_safe in new_safes:
                    self.mark_safe(new_safe)
            if len(new_mines) != 0:
                for new_mine in new_mines:
                    self.mark_mine(new_mine)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) != 0:
            for safe in self.safes:
                if not (safe in self.moves_made):
                    self.availables.remove(safe)
                    return safe


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        number_len = len(self.availables)
        if number_len == 0: # if there's no available left, return None 
            return None
        random_number = random.randint(0, number_len-1) # index for random_cell in self.availables
        random_cell = self.availables[random_number] # choose one cell of all available cells
        self.availables.remove(random_cell)
        if (random_cell not in self.moves_made) and (random_cell not in self.mines):
            return random_cell
        else:
            self.make_random_move()

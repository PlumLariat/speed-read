class WordList:
    """A sequential word list used to step through words one at a time during a speed-reading session.

    Attributes:
        l (list[str]): The list of words loaded from a source file.
        cur_index (int): Index of the current word.
        remaining (int): Number of words left after the current position.
        complete (bool): True once the last word has been consumed.
    """

    def __init__(self) -> None:
        """Initializes an empty WordList with no words loaded."""
        self.l = []
        self.cur_index = 0
        self.remaining = 0
        self.complete = False

    def init_from_txt_file(self, txt_file_path: str) -> None:
        """Loads words from a plain-text file, splitting on whitespace.

        Args:
            txt_file_path (str): Path to the text file to load.
        """
        self.l = self.__txt_file_to_list(txt_file_path)
        self.remaining = len(self.l) - 1

    def reset(self) -> None:
        """Resets the list back to the first word and clears the complete flag."""
        self.cur_index = 0
        self.remaining = len(self.l) - 1
        self.complete = False

    def get_current_word(self) -> str:
        """Returns the word at the current position.

        Returns:
            The current word string.
        """
        return self.l[self.cur_index]

    def next(self) -> None:
        """Advances to the next word.

        Sets `complete` to True when the last word is reached.
        Does nothing if the list is already exhausted.
        """
        if self.remaining <= 0:
            if self.remaining == 0:
                self.complete = True
            return

        self.cur_index += 1
        self.remaining -= 1

    def prev(self) -> None:
        """Moves back to the previous word."""
        if self.remaining >= 0:
            return

        self.cur_index -= 1
        self.remaining += 1

    def __txt_file_to_list(self, filepath: str) -> list[str]:
        """Reads a UTF-8 text file and splits it into a list of whitespace-delimited tokens.

        Args:
            filepath: Path to the text file.

        Returns:
            A list of word strings.
        """
        with open(filepath, encoding="utf-8") as file:
            f_str = file.read()
            token_list = f_str.split()

        return token_list

    def __repr__(self) -> str:
        return (
            __name__
            + f"({self.cur_index=},{self.remaining=},{self.get_current_word()=})"
        )

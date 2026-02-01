class WordList:
    def __init__(self) -> None:
        self.l = []
        self.cur_index = 0
        self.remaining = 0
        self.complete = False

    def init_from_txt_file(self, txt_file_path) -> None:
        self.l = self.__txt_file_to_list(txt_file_path)
        self.remaining = len(self.l) - 1
        #print(self.l)

    def reset(self) -> None:
        self.cur_index = 0
        self.remaining = len(self.l) - 1
        self.complete = False

    def get_current_word(self) -> str:
        return self.l[self.cur_index]
    
    def next(self) -> None:
        #print(self)
        if self.remaining <= 0:
            if self.remaining == 0:
                self.complete = True
            return
        
        self.cur_index += 1
        self.remaining -= 1
    
    def prev(self) -> None:
        '''This isnt really used, but might as well keep it.s'''
        if self.remaining >= 0:
            return
        
        self.cur_index -= 1
        self.remaining += 1

    def __txt_file_to_list(self, filepath: str) -> list[str]:
        
        with open(filepath, encoding="utf-8") as file:
            f_str = file.read()
            token_list = f_str.split()

        return token_list
    
    def __repr__(self) -> str:
        return __name__ + f"({self.cur_index=},{self.remaining=},{self.get_current_word()=})"
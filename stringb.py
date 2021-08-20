from colorama import Fore, Back, Style

class String(str):
    def __init__(self, text, *args, **kwargs):
        self.text = str(text)
        self.length = len(self.text)
        self.tokens = len(self.text.split())
        # self.__new__(*args, **kwargs)

    # def __new__(self, text):
        # super().__init__(text)
        # super().__new__(self, text)

    def color(self, name, style='bright'):
        return getattr(Style, style.upper())+getattr(Fore, name.upper())+self+Style.RESET_ALL

    def truncate(self, length=50):
        if len(self.text) < length:
            return String(self.text)
        else:
            return String(self.text[:length]+'...')

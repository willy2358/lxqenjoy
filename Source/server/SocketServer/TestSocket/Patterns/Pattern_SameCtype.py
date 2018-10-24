
from Patterns.Pattern import Pattern

class Pattern_SameCtype(Pattern):
    ELEMENT_NAME = "same_ctype"
    def __init__(self, gRule):
        super(Pattern_SameCtype, self).__init__(gRule)
        self.__ctype = "*"
        self.__count = 0

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_SameCtype.ELEMENT_NAME:
            return False
        return True


    def is_my_pattern(self, cards):
        return False
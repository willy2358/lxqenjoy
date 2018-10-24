
from xml.dom.minidom import parse
import xml.dom.minidom

from Cards.CFigure import CFigure, parse_cfigure
from Cards.CFigure import TOKEN as CFIGURE_TOKEN
from Cards.CType import CType, parse_ctype
from Cards.CType import TOKEN as CTYPE_TOKEN
from GCore.Engine import *
import GCore.Engine
from GCore.LeftOperand import LeftOperand


from Patterns.Pattern import Pattern
from GCore.Runtime import Runtime

class Pattern_Single(Pattern):
    ELEMENT_NAME = "single"
    def __init__(self, gRule):
        super(Pattern_Single, self).__init__(gRule)
        self.__ctype = CType.Any
        self.__cfigure = CFigure.Undefined

    def load(self, xmlElement):

        if xmlElement.tagName != Pattern_Single.ELEMENT_NAME:
            return False
        try:

            if xmlElement.hasAttribute(GCore.Engine.attr_name_cfigure):
                self.__cfigure = parse_cfigure(xmlElement.getAttribute(GCore.Engine.attr_name_cfigure))
            if xmlElement.hasAttribute(GCore.Engine.attr_name_ctype):
                self.__ctype = parse_ctype(xmlElement.getAttribute(GCore.Engine.attr_name_ctype), self.getGRule().get_gtype())
            if xmlElement.hasAttribute(Pattern.ATTR_NAME_POWER):
                powerAttrVal = xmlElement.getAttribute(Pattern.ATTR_NAME_POWER)
                if powerAttrVal.isnumeric():
                    self.set_power(int(powerAttrVal))
                elif is_str_statement(powerAttrVal) or is_var_ref(powerAttrVal) :
                    self.add_power_statement(parse_statement_str(xmlElement, powerAttrVal))
            if not xmlElement.hasChildNodes():
                return True
            for elem in Utils.getXmlChildElments(xmlElement):
                s = parse_statement_elem(elem)
                if s is None:
                    return False
                targetProp = s.get_target_property()
                if targetProp == Runtime.CARDS_POWER :
                    self.add_power_statement(s)
                elif targetProp == Runtime.CARDS_LEADING:
                    self.add_leading_statement(s)
            return True
        except Exception as ex:
            return False

    def is_my_pattern(self, cards):
        return False

from xml.dom.minidom import parseimport xml.dom.minidomimport reimport Utilsfrom GCore.Clause import Clausefrom GCore.Case import Casefrom GCore.Cases import Casesfrom GCore.Statement import Statementfrom GCore.Statements import Statementsfrom GCore.Update import Updatefrom GCore.Operator import Operatorimport GCore.Operatortag_name_lets = "lets"tag_name_let = "let"tag_name_when = "when"tag_name_case = "case"tag_name_cases = "cases"tag_name_var = "var"tag_name_vars = "vars"tag_name_else = "else"tag_name_then = "then"tag_name_ift = "ift" # if testtag_name_card = "card"tag_name_cards = "cards"tag_name_property = "property"tag_name_property = "properties"attr_name_op = "op"attr_name_power = "power"attr_name_leading = "leading"attr_name_property = "property"attr_name_value="value"attr_name_value_of = "value_of"attr_name_cfigure = "cfigure"attr_name_ctype = "ctype"attr_name_ret_as = "ret_as"attr_name_ret_is = "ret_is"attr_name_ret_not_is = "ret_not_is"attr_name_ret_not_as = "ret_not_as"attr_name_ret_lt = "ret_lt"attr_name_ret_lt_as = "ret_lt_as"attr_name_ret_not_lt = "ret_not_lt"attr_name_ret_not_lt_as = "ret_not_lt_as"attr_name_ret_gt = "ret_gt"attr_name_ret_gt_as = "ret_gt_as"attr_name_ret_not_gt = "ret_not_gt"attr_name_ret_not_gt_as = "ret_not_gt_as"attr_val_op_and = "and"attr_val_op_or = "or"attr_val_op_not = "not"attr_val_op_add = "add"attr_val_op_subtract = "subtract"attr_val_op_multiply = "multiply"statement_regex_pattern = "^:\((.*)\)$"statement_regex_variable = "^@([a-zA-Z][\w.]*)$"proc_name_ctype_of = "ctype_of"proc_name_cfigure_of = "cfigure_of"def value_of(var):    return Nonedef cfigure_of(var):    return Nonedef ctype_of(var):    return Nonedef parse_case(xmlNode):    passdef parse_update(xmlNode):    passdef parse_clause(xmlNode):    passdef parse_statement_str(strStatements):    passdef parse_statement_elem(xmlElem):    if type(xmlElem) is not xml.dom.minidom.Element:        return None    if xmlElem.tagName == tag_name_lets:        return parse_statement_lets(xmlElem)    elif xmlElem.tagName == tag_name_let:        return parse_statement_let(xmlElem)    elif xmlElem.tagName == tag_name_ift:        return parse_statement_ift(xmlElem)    else:        return None    # elif xmlElem.tagName == tag_name_case:    #     return parse_statement_case(xmlElem)def parse_statement_lets(xmlElem):    if not xmlElem.hasChildNodes():        return None    # usage lets/let ... when    lets = Utils.getXmlNamedChildElments(tag_name_let, xmlElem)    if not lets:        return None    clause = Clause()    for l in lets:        update = parse_statement_let(l)        if update:            clause.add_true_update(update)    when = Utils.getXmlFirstNamedChild(tag_name_when, xmlElem)    if when:        clause.set_case(when)    return clausedef parse_statement_let(xmlElem):    return parse_statement_update(xmlElem)def parse_statement_cases(xmlElem):    op = Operator.And    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    caseElems = Utils.getXmlNamedChildElments(tag_name_case, xmlElem)    if not caseElems:        return None    caseObjs = []    for c in caseElems:        case = parse_statement_case(c)        if case:            caseObjs.append(case)    if caseObjs:        if len(caseObjs) > 1:            caseInst = Cases(op)            for co in caseObjs:                caseInst.add_case(co)            return caseInst        else:            return caseObjs[0]    else:        return None# cases ... [then] ...[else]def parse_statement_ift(xmlElem):    clause = Clause()    casesNode = Utils.getXmlFirstNamedChild(tag_name_cases, xmlElem)    if casesNode:        clause.set_case(parse_statement_cases(casesNode))    else:        caseNode = Utils.getXmlFirstNamedChild(tag_name_case, xmlElem)        caseInst = parse_statement_case(caseNode)        if caseInst:            clause.set_case(caseInst)    childElems = Utils.getXmlChildElments(xmlElem)    for e in childElems:        if e.tagName == tag_name_else:            false_ups = parse_statement_else(xmlElem)            clause.set_false_updates(false_ups)        elif e.tagName == tag_name_then:            true_ups = parse_statement_then(xmlElem)            clause.set_true_updates(true_ups)        else:            true_up = parse_statement_update(xmlElem)            clause.add_true_update(true_up)def fetch_runtime_object(xmlElem):    return Nonedef fetch_runtime_object_property(propExpr):    return Nonedef parse_statement_update(xmlElem):    if not xmlElem.hasAttribute(attr_name_property):        return None    prop = xmlElem.getAttribute(attr_name_property)    if not xmlElem.hasAttribute(attr_name_value):        return None    # target = fetch_runtime_object(xmlElem)    # if not target:    #     return None    val = xmlElem.getAttribute(attr_name_value)    op = Operator.Update    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    return Update(prop, val, op)def parse_statement_then(xmlElem):    updates = []    childElems = Utils.getXmlChildElments(xmlElem)    for el in childElems:        up = parse_statement_update(el)        updates.append(up)    return updatesdef create_case_instance(testee, compareOp, compareVal):    return Case(testee, compareVal, compareOp)def parse_statement_case(xmlElem):    ret = is_valid_case_element(xmlElem)    if not ret[0]:        return None    return create_case_instance(ret[1], ret[2], ret[3])def is_valid_case_element(xmlElem):    if not xmlElem.hasAttribute(attr_name_value_of):        return False, None, None, None    testee = xmlElem.getAttribute(attr_name_value_of)    if xmlElem.hasAttribute(attr_name_ret_is):        return True, testee, Operator.Equal, xmlElem.getAttribute(attr_name_ret_is)    if xmlElem.hasAttribute(attr_name_ret_as):        return True, testee, Operator.Equal, xmlElem.getAttribute(attr_name_ret_as)    if xmlElem.hasAttribute(attr_name_ret_not_is):        return True, testee, Operator.NotEqual, xmlElem.getAttribute(attr_name_ret_not_is)    if xmlElem.hasAttribute(attr_name_ret_not_as):        return True, testee, Operator.NotEqual, xmlElem.getAttribute(attr_name_ret_not_as)    if xmlElem.hasAttribute(attr_name_ret_lt):        return True, testee, Operator.LessThan, xmlElem.getAttribute(attr_name_ret_lt)    if xmlElem.hasAttribute(attr_name_ret_lt_as):        return True, testee, Operator.LessThan, xmlElem.getAttribute(attr_name_ret_lt_as)    if xmlElem.hasAttribute(attr_name_ret_not_lt):        return True, testee, Operator.NotLessThan, xmlElem.getAttribute(attr_name_ret_not_lt)    if xmlElem.hasAttribute(attr_name_ret_not_lt_as):        return True, testee, Operator.NotLessThan, xmlElem.getAttribute(attr_name_ret_not_lt_as)    if xmlElem.hasAttribute(attr_name_ret_gt):        return True, testee, Operator.GreaterThan, xmlElem.getAttribute(attr_name_ret_gt)    if xmlElem.hasAttribute(attr_name_ret_gt_as):        return True, testee, Operator.GreaterThan, xmlElem.getAttribute(attr_name_ret_gt_as)    if xmlElem.hasAttribute(attr_name_ret_not_gt):        return True, testee, Operator.NotGreaterThan, xmlElem.getAttribute(attr_name_ret_not_gt)    if xmlElem.hasAttribute(attr_name_ret_not_gt_as):        return True, testee, Operator.NotGreaterThan, xmlElem.getAttribute(attr_name_ret_not_gt_as)    return False, None, None, Nonedef parse_statement_when(xmlElem):    op = Operator.And    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    ret = is_valid_case_element(xmlElem)    caseObjs = []    if ret[0]:        caseInst = create_case_instance(ret[1], ret[2], ret[3])        if caseInst:            caseObjs.append(caseInst)    childElems = Utils.getXmlChildElments(xmlElem)    if childElems:        for child in childElems:            if child.tagName == tag_name_case:                caseInst = parse_statement_case(child)                if caseInst:                    caseObjs.append(caseInst)            elif child.tagName == tag_name_cases:                caseInst = parse_statement_cases(child)                if caseInst:                    caseObjs.append(caseInst)    # merge the cases    if caseObjs:        if len(caseObjs) > 1:            caseInst = Cases(op)            for co in caseObjs:                caseInst.add_case(co)            return caseInst        else:            return caseObjs[0]    else:        return Nonedef parse_statement_else(xmlElem):    updates = []    childElems = Utils.getXmlChildElments(xmlElem)    for el in childElems:        if el.tagName == tag_name_then:            ups = parse_statement_then(xmlElem)            if ups:                updates.extend(ups)        else:            up = parse_statement_update(el)            updates.append(up)    return updatesdef is_var_ref(text):    if re.match(statement_regex_variable, text):        return True    else:        return Falsedef is_str_statement(text):    if re.match(statement_regex_pattern, text):        return True    else:        return False
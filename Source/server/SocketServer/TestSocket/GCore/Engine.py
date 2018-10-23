from xml.dom.minidom import parseimport xml.dom.minidomimport reimport Utilsfrom GCore.Clause import Clausefrom GCore.Case import Casefrom GCore.Cases import Casesfrom GCore.Statement import Statementfrom GCore.Statements import Statementsfrom GCore.Update import Updatefrom GCore.Operator import Operator, from_strimport GCore.Operatorfrom GCore.Operation import Operationfrom GCore.Block import Blockfrom GCore.CValue import CValueimport Mains.VarsSpace as VarsSpacefrom GCore.Variable import Variablefrom GCore.FuncCall import FuncCalltag_name_lets = "lets"tag_name_let = "let"tag_name_when = "when"tag_name_case = "case"tag_name_cases = "cases"tag_name_var = "var"tag_name_vars = "vars"tag_name_else = "else"tag_name_then = "then"tag_name_ift = "ift" # if testtag_name_card = "card"tag_name_cards = "cards"tag_name_property = "property"tag_name_property = "properties"attr_name_op = "op"attr_name_power = "power"attr_name_leading = "leading"attr_name_property = "property"attr_name_value="value"attr_name_value_of = "value_of"attr_name_cfigure = "cfigure"attr_name_ctype = "ctype"attr_name_ret_as = "ret_as"attr_name_ret_is = "ret_is"attr_name_ret_not_is = "ret_not_is"attr_name_ret_not_as = "ret_not_as"attr_name_ret_lt = "ret_lt"attr_name_ret_lt_as = "ret_lt_as"attr_name_ret_not_lt = "ret_not_lt"attr_name_ret_not_lt_as = "ret_not_lt_as"attr_name_ret_gt = "ret_gt"attr_name_ret_gt_as = "ret_gt_as"attr_name_ret_not_gt = "ret_not_gt"attr_name_ret_not_gt_as = "ret_not_gt_as"attr_val_op_and = "and"attr_val_op_or = "or"attr_val_op_not = "not"attr_val_op_add = "add"attr_val_op_subtract = "subtract"attr_val_op_multiply = "multiply"statement_regex_pattern = "^:\((.*)\)$"statement_regex_variable = "^@([a-zA-Z][\w.]*)$"statement_regex_var_def = "^var\s+\w+\s*$"statement_regex_func_call = "^\w+\(.+\)$"proc_name_ctype_of = "ctype_of"proc_name_cfigure_of = "cfigure_of"def value_of(var):    return Nonedef cfigure_of(var):    return Nonedef ctype_of(var):    return Nonedef parse_case(xmlNode):    passdef parse_update(xmlNode):    passdef parse_clause(xmlNode):    passdef parse_uni_operation(line):    passdef parse_func_call(codeText):    if not is_func_call(codeText):        return None    pos = codeText.index('(')    funcName = codeText[0, 2]    funcCall = FuncCall(funcName)    argsStr = codeText[pos, -1]    args = argsStr.split(',')    for arg in args:        op = parse_operand(arg.strip())        if not op:            funcCall.add_argument(op)def parse_operand(codeTxt):    if codeTxt.isnumeric():        return CValue(int(codeTxt))    elif codeTxt.startswith('@'):        return Variable(codeTxt)    else:        return parse_func_call(codeTxt)def record_variable(xmlElemnt, line):    varName = line.replace('var').strip()    VarsSpace.update(xmlElemnt, varName, None)def extract_var_name(words):    return words.replace('var').strip()# support format: c = a + b#          c = func(@a)#          c = func(@a) + func(@b)def parse_operation(xmlElement, line):    line = line.strip()    if is_var_defination(line):        record_variable(xmlElement, line)        return    ps = re.split('\s*=\s*', line)    var_name = None    if len(ps) > 1:        var_name = extract_var_name(ps[0])    mat = re.match(r'(?P<p1>.+)\s*(?P<op>\+|-|\*|/)\s*(?P<p2>.+)', line)    if not mat:        return parse_uni_operation(line)    operator = mat.groupdict()['op']    left = mat.groupdict()['p1']    right = mat.groupdict()['p2']    op1 = parse_operand(left)    op2 = parse_operand(right)    op = Operation(op1, op2, from_str(operator))    if var_name:        op.set_result_var(xmlElement, var_name)    op.set_xml_node(xmlElement)    return opdef parse_block(xmlElement, lines):    block = Block()    for l in lines:        op = parse_operation(l)        block.add_operation(op)    return blockdef parse_statement_str(xmlElement, strStatements):    txt = strStatements[2:-1]    lines = txt.split(';')    if len(lines) > 1:        return parse_block(lines)    else:        return parse_operation(txt)def parse_statement_elem(xmlElem):    if type(xmlElem) is not xml.dom.minidom.Element:        return None    if xmlElem.tagName == tag_name_lets:        return parse_statement_lets(xmlElem)    elif xmlElem.tagName == tag_name_let:        return parse_statement_let(xmlElem)    elif xmlElem.tagName == tag_name_ift:        return parse_statement_ift(xmlElem)    else:        return None    # elif xmlElem.tagName == tag_name_case:    #     return parse_statement_case(xmlElem)def parse_statement_lets(xmlElem):    if not xmlElem.hasChildNodes():        return None    # usage lets/let ... when    lets = Utils.getXmlNamedChildElments(tag_name_let, xmlElem)    if not lets:        return None    clause = Clause()    for l in lets:        update = parse_statement_let(l)        if update:            clause.add_true_update(update)    when = Utils.getXmlFirstNamedChild(tag_name_when, xmlElem)    if when:        clause.set_case(when)    return clausedef parse_statement_let(xmlElem):    return parse_statement_update(xmlElem)def parse_statement_cases(xmlElem):    op = Operator.And    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    caseElems = Utils.getXmlNamedChildElments(tag_name_case, xmlElem)    if not caseElems:        return None    caseObjs = []    for c in caseElems:        case = parse_statement_case(c)        if case:            caseObjs.append(case)    if caseObjs:        if len(caseObjs) > 1:            caseInst = Cases(op)            for co in caseObjs:                caseInst.add_case(co)            return caseInst        else:            return caseObjs[0]    else:        return None# cases ... [then] ...[else]def parse_statement_ift(xmlElem):    clause = Clause()    casesNode = Utils.getXmlFirstNamedChild(tag_name_cases, xmlElem)    if casesNode:        clause.set_case(parse_statement_cases(casesNode))    else:        caseNode = Utils.getXmlFirstNamedChild(tag_name_case, xmlElem)        caseInst = parse_statement_case(caseNode)        if caseInst:            clause.set_case(caseInst)    childElems = Utils.getXmlChildElments(xmlElem)    for e in childElems:        if e.tagName == tag_name_else:            false_ups = parse_statement_else(xmlElem)            clause.set_false_updates(false_ups)        elif e.tagName == tag_name_then:            true_ups = parse_statement_then(xmlElem)            clause.set_true_updates(true_ups)        else:            true_up = parse_statement_update(xmlElem)            clause.add_true_update(true_up)def fetch_runtime_object(xmlElem):    return Nonedef fetch_runtime_object_property(propExpr):    return Nonedef parse_statement_update(xmlElem):    if not xmlElem.hasAttribute(attr_name_property):        return None    prop = xmlElem.getAttribute(attr_name_property)    if not xmlElem.hasAttribute(attr_name_value):        return None    # target = fetch_runtime_object(xmlElem)    # if not target:    #     return None    val = xmlElem.getAttribute(attr_name_value)    op = Operator.Update    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    return Update(prop, val, op)def parse_statement_then(xmlElem):    updates = []    childElems = Utils.getXmlChildElments(xmlElem)    for el in childElems:        up = parse_statement_update(el)        updates.append(up)    return updatesdef create_case_instance(testee, compareOp, compareVal):    return Case(testee, compareVal, compareOp)def parse_statement_case(xmlElem):    ret = is_valid_case_element(xmlElem)    if not ret[0]:        return None    return create_case_instance(ret[1], ret[2], ret[3])def is_valid_case_element(xmlElem):    if not xmlElem.hasAttribute(attr_name_value_of):        return False, None, None, None    testee = xmlElem.getAttribute(attr_name_value_of)    if xmlElem.hasAttribute(attr_name_ret_is):        return True, testee, Operator.Equal, xmlElem.getAttribute(attr_name_ret_is)    if xmlElem.hasAttribute(attr_name_ret_as):        return True, testee, Operator.Equal, xmlElem.getAttribute(attr_name_ret_as)    if xmlElem.hasAttribute(attr_name_ret_not_is):        return True, testee, Operator.NotEqual, xmlElem.getAttribute(attr_name_ret_not_is)    if xmlElem.hasAttribute(attr_name_ret_not_as):        return True, testee, Operator.NotEqual, xmlElem.getAttribute(attr_name_ret_not_as)    if xmlElem.hasAttribute(attr_name_ret_lt):        return True, testee, Operator.LessThan, xmlElem.getAttribute(attr_name_ret_lt)    if xmlElem.hasAttribute(attr_name_ret_lt_as):        return True, testee, Operator.LessThan, xmlElem.getAttribute(attr_name_ret_lt_as)    if xmlElem.hasAttribute(attr_name_ret_not_lt):        return True, testee, Operator.NotLessThan, xmlElem.getAttribute(attr_name_ret_not_lt)    if xmlElem.hasAttribute(attr_name_ret_not_lt_as):        return True, testee, Operator.NotLessThan, xmlElem.getAttribute(attr_name_ret_not_lt_as)    if xmlElem.hasAttribute(attr_name_ret_gt):        return True, testee, Operator.GreaterThan, xmlElem.getAttribute(attr_name_ret_gt)    if xmlElem.hasAttribute(attr_name_ret_gt_as):        return True, testee, Operator.GreaterThan, xmlElem.getAttribute(attr_name_ret_gt_as)    if xmlElem.hasAttribute(attr_name_ret_not_gt):        return True, testee, Operator.NotGreaterThan, xmlElem.getAttribute(attr_name_ret_not_gt)    if xmlElem.hasAttribute(attr_name_ret_not_gt_as):        return True, testee, Operator.NotGreaterThan, xmlElem.getAttribute(attr_name_ret_not_gt_as)    return False, None, None, Nonedef parse_statement_when(xmlElem):    op = Operator.And    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    ret = is_valid_case_element(xmlElem)    caseObjs = []    if ret[0]:        caseInst = create_case_instance(ret[1], ret[2], ret[3])        if caseInst:            caseObjs.append(caseInst)    childElems = Utils.getXmlChildElments(xmlElem)    if childElems:        for child in childElems:            if child.tagName == tag_name_case:                caseInst = parse_statement_case(child)                if caseInst:                    caseObjs.append(caseInst)            elif child.tagName == tag_name_cases:                caseInst = parse_statement_cases(child)                if caseInst:                    caseObjs.append(caseInst)    # merge the cases    if caseObjs:        if len(caseObjs) > 1:            caseInst = Cases(op)            for co in caseObjs:                caseInst.add_case(co)            return caseInst        else:            return caseObjs[0]    else:        return Nonedef parse_statement_else(xmlElem):    updates = []    childElems = Utils.getXmlChildElments(xmlElem)    for el in childElems:        if el.tagName == tag_name_then:            ups = parse_statement_then(xmlElem)            if ups:                updates.extend(ups)        else:            up = parse_statement_update(el)            updates.append(up)    return updatesdef is_var_ref(text):    if re.match(statement_regex_variable, text):        return True    else:        return Falsedef is_str_statement(text):    if re.match(statement_regex_pattern, text):        return True    else:        return Falsedef is_var_defination(line):    if re.match(statement_regex_var_def, line):        return True    else:        return Falsedef is_func_call(text):    if re.match(statement_regex_func_call, text):        return True    else:        return False
from xml.dom.minidom import parseimport xml.dom.minidomimport reimport Utilsfrom GCore.Elements.Clause import Clausefrom GCore.Elements.Case import Casefrom GCore.Elements.Cases import Casesfrom GCore.Elements.Update import Updatefrom GCore.Operator import Operator, from_strimport GCore.Operatorfrom GCore.Operation import Operationfrom GCore.Block import Blockfrom GCore.CValue import CValueimport GCore.VarsSpace as VarsSpacefrom GCore.Elements.Variable import Variablefrom GCore.FuncCall import FuncCallfrom GCore.Elements.Loop import Loopfrom GCore.OpCards.DrawCards import DrawCardsfrom GCore.OpCards.DealCards import DealCardsfrom GCore.OpCards.PickCards import PickCardsfrom GCore.OpCards.SendCards import SendCardsfrom GCore.Elements.ActRef import ActReffrom GCore.Elements.ActRefs import ActRefsfrom GCore.Elements.ActOpts import ActOptsfrom GCore.Elements.ExitLoop import ExitLoopfrom GCore.Elements.ExitRound import ExitRoundfrom GCore.Elements.FindPlayer import FindPlayerfrom GCore.Elements.FindPlayers import FindPlayersfrom GCore.Elements.PubMsg import PubMsgfrom GCore.Elements.Proc import Procfrom GCore.Elements.Delay import Delayfrom GCore.Elements.Action import Actionfrom GCore.Elements.ProcRef import ProcReffrom GCore.Elements.Ret import Rettag_name_action = "action"tag_name_actions = "actions"tag_name_act_opts = "act_opts"tag_name_act_ref = "act_ref"tag_name_act_refs = "act_refs"   # acts will be listed in a varialbletag_name_attr = "attr"tag_name_attrs = "attrs"tag_name_card = "card"tag_name_cards = "cards"tag_name_case = "case"tag_name_cases = "cases"tag_name_draw_cards = "draw_cards" #draw some cards from the card stack, but without dealing them to a playertag_name_deal_cards = "deal_cards" #deal some cards to player, from the card stack <==> draw_cards + send_cardstag_name_delay = "delay" # sleeping for secondstag_name_else = "else"tag_name_exeref = "exeref"tag_name_exit_loop = "exitloop"tag_name_exit_round = "exitround"tag_name_find_player = "find_player"tag_name_find_players = "find_players"tag_name_ift = "ift" # if testtag_name_lets = "lets"tag_name_let = "let"tag_name_loop = "loop"tag_name_loop_until = "loop_until"tag_name_pick_cards = "pick_cards"tag_name_pub_msg = "pub_msg"tag_name_proc = "proc"tag_name_proc_ref = "proc_ref"tag_name_property = "property"tag_name_properties = "properties"tag_name_ret = "ret"tag_name_scene = "scene"tag_name_send_cards = "send_cards" #send the cards drawn to a playertag_name_then = "then"tag_name_update = "update"tag_name_var = "var"tag_name_vars = "vars"tag_name_when = "when"attr_name_act = "act"attr_name_acts = "acts"attr_name_attr = "attr"attr_name_attrs = "attrs"attr_name_cards = "cards"attr_name_count = "count"attr_name_cfigure = "cfigure"attr_name_ctype = "ctype"attr_name_from_player = "from_player"attr_name_leading = "leading"attr_name_max = "max"attr_name_min = "min"attr_name_msg = "msg"attr_name_name = "name"attr_name_op = "op"attr_name_player = "player"attr_name_players = "players"attr_name_power = "power"attr_name_proc = "proc"attr_name_property = "property"attr_name_seconds = "seconds"attr_name_timeout = "timeout"attr_name_timeout_act = "timeout_act"attr_name_to_var = "to_var"attr_name_to_player = "to_player"attr_name_value="value"attr_name_value_of = "value_of"attr_name_value_type = "value_type"attr_name_ret_as = "ret_as"attr_name_ret_is = "ret_is"attr_name_ret_not_is = "ret_not_is"attr_name_ret_not_as = "ret_not_as"attr_name_ret_lt = "ret_lt"attr_name_ret_lt_as = "ret_lt_as"attr_name_ret_not_lt = "ret_not_lt"attr_name_ret_not_lt_as = "ret_not_lt_as"attr_name_ret_gt = "ret_gt"attr_name_ret_gt_as = "ret_gt_as"attr_name_ret_not_gt = "ret_not_gt"attr_name_ret_not_gt_as = "ret_not_gt_as"attr_val_op_and = "and"attr_val_op_or = "or"attr_val_op_not = "not"attr_val_op_add = "add"attr_val_op_subtract = "subtract"attr_val_op_multiply = "multiply"statement_regex_pattern = "^:\((.*)\)$"statement_regex_variable = "^@([a-zA-Z][\w.]*)$"statement_regex_var_def = "^var\s+\w+\s*$"statement_regex_func_call = "^\w+\(.+\)$"proc_name_ctype_of = "ctype_of"proc_name_cfigure_of = "cfigure_of"def value_of(var):    return Nonedef cfigure_of(var):    return Nonedef ctype_of(var):    return Nonedef parse_elem_action(xmlNode):    if not xmlNode.hasAttribute(attr_name_name):        return None    actName = xmlNode.getAttribute(attr_name_name)    act = Action(actName)    for elem in Utils.getXmlChildElments(xmlNode):        stm = parse_elem(elem)        if stm:            act.add_statement(stm)    return actdef parse_elem_act_opts(xmlNode):    if not xmlNode.hasAttribute(attr_name_to_player) \        or not xmlNode.hasAttribute(attr_name_timeout) \        or not xmlNode.hasAttribute(attr_name_timeout_act):        return None    player = xmlNode.getAttribute(attr_name_to_player)    timeout = xmlNode.getAttribute(attr_name_timeout)    outAct = xmlNode.getAttribute(attr_name_timeout_act)    act_opts = ActOpts(player, timeout, outAct)    for elem in Utils.getXmlChildElments(xmlNode):        act_opt = parse_elem_act_ref(elem)        if act_opt:            act_opts.add_act_opt(act_opt)    return act_optsdef parse_elem_act_ref(xmlNode):    if not xmlNode.hasAttribute(attr_name_act):        return None    actRef = xmlNode.getAttribute(attr_name_act)    act_opt = ActRef(actRef)    return act_optdef parse_elem_act_refs(xmlNode):    if not xmlNode.hasAttribute(attr_name_acts):        return None    acts = xmlNode.getAttribute(attr_name_acts)    actRefs = ActRefs(acts)    return actRefsdef parse_elem_def_var(xmlNode):    if not xmlNode.hasAttribute(attr_name_name) \            or not xmlNode.hasAttribute(attr_name_value) \            or not xmlNode.hasAttribute(attr_name_value_type):        return None    vName = xmlNode.getAttribute(attr_name_name)    vType = xmlNode.getAttribute(attr_name_value_type)    value = xmlNode.getAttribute(attr_name_value)    var = Variable(vName)    var.set_value_type(vType)    var.set_value(value)    return vardef parse_elem_delay(xmlNode):    if not xmlNode.hasAttribute(attr_name_seconds):        return None    secs = xmlNode.getAttribute(attr_name_seconds)    delay = Delay(int(secs))    return delaydef parse_elem_deal_cards(xmlNode):    if not xmlNode.hasAttribute(attr_name_player)\        or xmlNode.hasAttribute(attr_name_count):        return None    player = xmlNode.getAttribute(attr_name_player)    count = xmlNode.getAttribute(attr_name_count)    return DealCards(count, player)def parse_elem_draw_cards(xmlNode):    if not xmlNode.hasAttribute(attr_name_to_var)\            or not xmlNode.hasAttribute(attr_name_count):        return None    count = xmlNode.getAttribute(attr_name_count)    to_var = xmlNode.getAttribute(attr_name_to_var)    drawCards = DrawCards(to_var, count)    return drawCardsdef parse_elem_exitloop(xmlNode):    return ExitLoop()def parse_elem_exitround(xmlNode):    return ExitRound()def parse_elem_find_player(xmlNode):    finder = FindPlayer()    if xmlNode.hasAttribute(attr_name_property) and xmlNode.hasAttribute(attr_name_value):        # <find_player property="IsMainPlayer" value="true">        propName = xmlNode.getAttribute(attr_name_property)        val = xmlNode.getAttribute(attr_name_value)        finder.set_test_property(propName, val)    elif xmlNode.hasAttribute(attr_name_player):        # <find_player player="@trick_init_player">        varPlayer = xmlNode.getAttribute(attr_name_player)        finder.set_from_var(varPlayer)    for elem in Utils.getXmlChildElments(xmlNode):        stm = parse_elem(elem)        if stm:            finder.add_statement(stm)    return finderdef parse_elem_find_players(xmlNode):    playerFinder = FindPlayers()    if xmlNode.hasAttribute(attr_name_property) and xmlNode.hasAttribute(attr_name_value):        # <find_player property="IsMainPlayer" value="true">        propName = xmlNode.getAttribute(attr_name_property)        val = xmlNode.getAttribute(attr_name_value)        playerFinder.set_test_property(propName, val)    elif xmlNode.hasAttribute(attr_name_player):        # <find_player player="@trick_init_player">        varPlayer = xmlNode.getAttribute(attr_name_player)        playerFinder.set_from_var(varPlayer)    for elem in Utils.getXmlChildElments(xmlNode):        stm = parse_elem(elem)        if stm:            playerFinder.add_statement(stm)    return playerFinderdef parse_elem_loop(xmlNode):    loop = Loop()    for elem in Utils.getXmlChildElments(xmlNode):        s = parse_elem(elem)        if s:            if type(s) is Clause:                true_stms = s.get_true_statements()                if len(true_stms) == 1 and type(true_stms[0]) is ExitLoop:                    loop.set_exit_case(s)                else:                    loop.add_clause(s)            else:                loop.add_clause(s)    return loopdef parse_elem_loop_until(xmlNode):    caseStm = parse_elem_case(xmlNode)    if not caseStm:        return None    loop = parse_elem_loop(xmlNode)    if loop:        loop.set_exit_case(caseStm)    return loopdef parse_elem_pick_cards(xmlNode):    if not xmlNode.hasAttribute(attr_name_to_var)\        or not xmlNode.hasAttribute(attr_name_from_player)\        or not xmlNode.hasAttribute(attr_name_count):        return None    fromPlayer = xmlNode.getAttribute(attr_name_from_player)    toVar = xmlNode.getAttribute(attr_name_to_var)    count = xmlNode.getAttribute(attr_name_count)    return PickCards(count, fromPlayer, toVar)def parse_elem_proc_ref(xmlNode):    if not xmlNode.hasAttribute(attr_name_proc):        return None    procName = xmlNode.getAttribute(attr_name_proc)    procRef = ProcRef(procName)    return procRefdef parse_elem_proc(xmlNode):    if not xmlNode.hasAttribute(attr_name_name):        return None    name = xmlNode.getAttribute(attr_name_name)    proc = Proc(name)    for elem in Utils.getXmlChildElments(xmlNode):        stm = parse_elem(elem)        if stm:            proc.add_statement(stm)    return procdef parse_elem_pub_msg(xmlNode):    if not xmlNode.hasAttribute(attr_name_players)\        or not xmlNode.hasAttribute(attr_name_msg):        return None    players = xmlNode.getAttribute(attr_name_players)    msg = xmlNode.getAttribute(attr_name_msg)    return PubMsg(players, msg)def parse_elem_ret(xmlNdoe):    if not xmlNdoe.hasAttribute(attr_name_value):        return None    value = xmlNdoe.getAttribute(attr_name_value)    retObj = Ret(value)    return retObjdef parse_elem_send_cards(xmlNode):    if not xmlNode.hasAttribute(attr_name_player)\            or not xmlNode.hasAttribute(attr_name_cards):        return None    player = xmlNode.getAttribute(attr_name_player)    cards = xmlNode.getAttribute(attr_name_cards)    return SendCards(cards, player)def parse_func_call(xmlElement, codeText):    if not is_func_call(codeText):        return None    pos = codeText.index('(')    funcName = codeText[0 : pos]    funcCall = FuncCall(funcName)    funcCall.set_xml_node(xmlElement)    argsStr = codeText[pos + 1 : -1]    args = argsStr.split(',')    for arg in args:        op = parse_operand(xmlElement, arg.strip())        if op:            funcCall.add_argument(op)    return funcCalldef parse_operand(xmlElement, codeTxt):    if codeTxt.isnumeric():        valObj = CValue(int(codeTxt))        valObj.set_xml_node(xmlElement)        return valObj    elif codeTxt.startswith('@'):        varObj = Variable(codeTxt)        varObj.set_xml_node(xmlElement)        return varObj    else:        return parse_func_call(xmlElement, codeTxt)def record_variable(xmlElemnt, line):    varName = line.replace('var').strip()    VarsSpace.update(xmlElemnt, varName, None)def extract_var_name(words):    return words.replace('var').strip()# support format: c = a + b#          c = func(@a)#          c = func(@a) + func(@b)def parse_operation(xmlElement, line):    line = line.strip()    if is_var_defination(line):        record_variable(xmlElement, line)        return None    ps = re.split('\s*=\s*', line)    var_name = None    if len(ps) > 1:        var_name = extract_var_name(ps[0])    mat = re.match(r'(?P<p1>.+)\s*(?P<op>\+|-|\*|/)\s*(?P<p2>.+)', line)    if not mat:        return parse_operand(xmlElement, line)    operator = mat.groupdict()['op']    left = mat.groupdict()['p1']    right = mat.groupdict()['p2']    op1 = parse_operand(xmlElement, left)    op2 = parse_operand(xmlElement, right)    op = Operation(op1, op2, from_str(operator))    if var_name:        op.set_result_var(xmlElement, var_name)    op.set_xml_node(xmlElement)    return opdef parse_block(xmlElement, lines):    block = Block()    for l in lines:        op = parse_operation(xmlElement, l)        block.add_operation(op)    block.set_xml_node(xmlElement)    return blockdef parse_statement_str(xmlElement, strStatements):    if is_var_ref(strStatements):        return parse_operand(xmlElement, strStatements)    txt = strStatements[2:-1]    lines = txt.split(';')    if len(lines) > 1:        return parse_block(xmlElement, lines)    else:        return parse_operation(xmlElement, txt)def parse_elem(xmlElem):    if type(xmlElem) is not xml.dom.minidom.Element:        return None    if xmlElem.tagName == tag_name_action:        return parse_elem_action(xmlElem)    if xmlElem.tagName == tag_name_act_refs:        return parse_elem_act_refs(xmlElem)    elif xmlElem.tagName == tag_name_act_ref:        return parse_elem_act_ref(xmlElem)    elif xmlElem.tagName == tag_name_act_opts:        return parse_elem_act_opts(xmlElem)    elif xmlElem.tagName == tag_name_deal_cards:        return parse_elem_deal_cards(xmlElem)    elif xmlElem.tagName == tag_name_delay:        return parse_elem_delay(xmlElem)    elif xmlElem.tagName == tag_name_draw_cards:        return parse_elem_draw_cards(xmlElem)    elif xmlElem.tagName == tag_name_exit_loop:        return parse_elem_exitloop(xmlElem)    elif xmlElem.tagName == tag_name_exit_round:        return parse_elem_exitround(xmlElem)    elif xmlElem.tagName == tag_name_find_player:        return parse_elem_find_player(xmlElem)    elif xmlElem.tagName == tag_name_find_players:        return parse_elem_find_players(xmlElem)    elif xmlElem.tagName == tag_name_ift:        return parse_elem_ift(xmlElem)    elif xmlElem.tagName == tag_name_let:        return parse_elem_let(xmlElem)    elif xmlElem.tagName == tag_name_lets:        return parse_elem_lets(xmlElem)    elif xmlElem.tagName == tag_name_loop:        return parse_elem_loop(xmlElem)    elif xmlElem.tagName == tag_name_loop_until:        return parse_elem_loop_until(xmlElem)    elif xmlElem.tagName == tag_name_pick_cards:        return parse_elem_pick_cards(xmlElem)    elif xmlElem.tagName == tag_name_proc:        return parse_elem_proc(xmlElem)    elif xmlElem.tagName == tag_name_proc_ref:        return parse_elem_proc_ref(xmlElem)    elif xmlElem.tagName == tag_name_pub_msg:        return parse_elem_pub_msg(xmlElem)    elif xmlElem.tagName == tag_name_ret:        return parse_elem_ret(xmlElem)    elif xmlElem.tagName == tag_name_update:        return parse_elem_update(xmlElem)    elif xmlElem.tagName == tag_name_var:        return parse_elem_def_var(xmlElem)    else:        return None    # elif xmlElem.tagName == tag_name_case:    #     return parse_statement_case(xmlElem)def parse_elem_lets(xmlElem):    if not xmlElem.hasChildNodes():        return None    # usage lets/let ... when    lets = Utils.getXmlNamedChildElments(tag_name_let, xmlElem)    if not lets:        return None    clause = Clause()    for l in lets:        update = parse_elem_let(l)        if update:            clause.add_true_statement(update)    when = Utils.getXmlFirstNamedChild(tag_name_when, xmlElem)    if when:        clause.set_case(when)    return clausedef parse_elem_let(xmlElem):    update = parse_elem_update(xmlElem)    if not update:        return None    whenNode = Utils.getXmlFirstNamedChild(tag_name_when, xmlElem)    if not whenNode:        return update    if not whenNode.hasChildNodes():        case = parse_elem_case(whenNode)        update.set_exe_case(case)    else:        case = parse_elem_cases(whenNode)        update.set_exe_case(case)    return updatedef parse_elem_cases(xmlElem):    op = Operator.And    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    caseElems = Utils.getXmlNamedChildElments(tag_name_case, xmlElem)    if not caseElems:        return None    caseObjs = []    for c in caseElems:        case = parse_elem_case(c)        if case:            caseObjs.append(case)    if caseObjs:        if len(caseObjs) > 1:            caseInst = Cases(op)            for co in caseObjs:                caseInst.add_case(co)            return caseInst        else:            return caseObjs[0]    else:        return None# cases ... [then] ...[else]def parse_elem_ift(xmlElem):    clause = Clause()    casesNode = Utils.getXmlFirstNamedChild(tag_name_cases, xmlElem)    if casesNode:        clause.set_case(parse_elem_cases(casesNode))    else:        caseNode = Utils.getXmlFirstNamedChild(tag_name_case, xmlElem)        if caseNode:            caseInst = parse_elem_case(caseNode)            if caseInst:                clause.set_case(caseInst)    childElems = Utils.getXmlChildElments(xmlElem)    for e in childElems:        if e.tagName == tag_name_case or e.tagName == tag_name_cases:            continue        if e.tagName == tag_name_else:            false_ups = parse_elem_else(e)            clause.set_false_statements(false_ups)        elif e.tagName == tag_name_then:            true_ups = parse_elem_then(e)            clause.set_true_statements(true_ups)        else:            stm = parse_elem(e)            if stm:                clause.add_true_statement(stm)    return clausedef fetch_runtime_object(xmlElem):    return Nonedef fetch_runtime_object_property(propExpr):    return Nonedef parse_elem_update(xmlElem):    if not xmlElem.hasAttribute(attr_name_property):        return None    prop = xmlElem.getAttribute(attr_name_property)    if not xmlElem.hasAttribute(attr_name_value):        return None    # target = fetch_runtime_object(xmlElem)    # if not target:    #     return None    val = xmlElem.getAttribute(attr_name_value)    op = Operator.Update    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    return Update(prop, val, op)def parse_elem_then(xmlElem):    updates = []    childElems = Utils.getXmlChildElments(xmlElem)    for el in childElems:        up = parse_elem_update(el)        updates.append(up)    return updatesdef create_case_instance(xmlElement, testee, compareOp, compareVal):    op1 = parse_statement_str(xmlElement, testee)    op2 = parse_statement_str(xmlElement, compareVal)    return Case(op1, op2, compareOp)def parse_elem_case(xmlElem):    ret = is_valid_case_element(xmlElem)    if not ret[0]:        return None    return create_case_instance(xmlElem, ret[1], ret[2], ret[3])def is_valid_case_element(xmlElem):    if not xmlElem or not xmlElem.hasAttribute(attr_name_value_of):        return False, None, None, None    testee = xmlElem.getAttribute(attr_name_value_of)    if xmlElem.hasAttribute(attr_name_ret_is):        return True, testee, Operator.Equal, xmlElem.getAttribute(attr_name_ret_is)    if xmlElem.hasAttribute(attr_name_ret_as):        return True, testee, Operator.Equal, xmlElem.getAttribute(attr_name_ret_as)    if xmlElem.hasAttribute(attr_name_ret_not_is):        return True, testee, Operator.NotEqual, xmlElem.getAttribute(attr_name_ret_not_is)    if xmlElem.hasAttribute(attr_name_ret_not_as):        return True, testee, Operator.NotEqual, xmlElem.getAttribute(attr_name_ret_not_as)    if xmlElem.hasAttribute(attr_name_ret_lt):        return True, testee, Operator.LessThan, xmlElem.getAttribute(attr_name_ret_lt)    if xmlElem.hasAttribute(attr_name_ret_lt_as):        return True, testee, Operator.LessThan, xmlElem.getAttribute(attr_name_ret_lt_as)    if xmlElem.hasAttribute(attr_name_ret_not_lt):        return True, testee, Operator.NotLessThan, xmlElem.getAttribute(attr_name_ret_not_lt)    if xmlElem.hasAttribute(attr_name_ret_not_lt_as):        return True, testee, Operator.NotLessThan, xmlElem.getAttribute(attr_name_ret_not_lt_as)    if xmlElem.hasAttribute(attr_name_ret_gt):        return True, testee, Operator.GreaterThan, xmlElem.getAttribute(attr_name_ret_gt)    if xmlElem.hasAttribute(attr_name_ret_gt_as):        return True, testee, Operator.GreaterThan, xmlElem.getAttribute(attr_name_ret_gt_as)    if xmlElem.hasAttribute(attr_name_ret_not_gt):        return True, testee, Operator.NotGreaterThan, xmlElem.getAttribute(attr_name_ret_not_gt)    if xmlElem.hasAttribute(attr_name_ret_not_gt_as):        return True, testee, Operator.NotGreaterThan, xmlElem.getAttribute(attr_name_ret_not_gt_as)    return False, None, None, Nonedef parse_elem_when(xmlElem):    op = Operator.And    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    ret = is_valid_case_element(xmlElem)    caseObjs = []    if ret[0]:        caseInst = create_case_instance(ret[1], ret[2], ret[3])        if caseInst:            caseObjs.append(caseInst)    childElems = Utils.getXmlChildElments(xmlElem)    if childElems:        for child in childElems:            if child.tagName == tag_name_case:                caseInst = parse_elem_case(child)                if caseInst:                    caseObjs.append(caseInst)            elif child.tagName == tag_name_cases:                caseInst = parse_elem_cases(child)                if caseInst:                    caseObjs.append(caseInst)    # merge the cases    if caseObjs:        if len(caseObjs) > 1:            caseInst = Cases(op)            for co in caseObjs:                caseInst.add_case(co)            return caseInst        else:            return caseObjs[0]    else:        return Nonedef parse_elem_else(xmlElem):    updates = []    childElems = Utils.getXmlChildElments(xmlElem)    for el in childElems:        if el.tagName == tag_name_then:            ups = parse_elem_then(xmlElem)            if ups:                updates.extend(ups)        else:            up = parse_elem_update(el)            updates.append(up)    return updatesdef is_var_ref(text):    if re.match(statement_regex_variable, text):        return True    else:        return Falsedef is_str_statement(text):    if re.match(statement_regex_pattern, text):        return True    else:        return Falsedef is_var_defination(line):    if re.match(statement_regex_var_def, line):        return True    else:        return Falsedef is_func_call(text):    if re.match(statement_regex_func_call, text):        return True    else:        return False
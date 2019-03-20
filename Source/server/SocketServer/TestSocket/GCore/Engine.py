from xml.dom.minidom import parseimport xml.dom.minidomimport reimport Utils#TODO:1. 座位号支持：1）座位号未指定：座位号递增；2）座位号有指定，players按座位号排序#TODO:2. 押注玩法的支持：一次性给所有（指定）players发送命令，在一定时间后搜集用户选择#TODO:3. 支持向购买服务的客户发送用户命令能力的查询，比如，在咋金花中，查询玩家是否有足够Token跟牌，比如，查询玩家是否有资格坐庄#TODO:4. 支持客户定制不同阶段等待的超时，比如一局结束，发送完输赢方后，要允许在客户端播放相应的表情动画#TODO 5. 删除Let, when的支持。from GCore.Elements.Clause import Clausefrom GCore.Elements.Case import Casefrom GCore.Elements.Cases import Casesfrom GCore.Elements.Update import Updatefrom GCore.Operator import Operator, from_strfrom GCore.Elements.PubAct import PubActfrom GCore.Elements.PubPStatus import PubPlayerStatusfrom GCore.Elements.PubRStatus import PubRoundStatusfrom GCore.Operation import Operationfrom GCore.Block import Blockfrom GCore.CValue import CValuefrom GCore.GArray import GArrayfrom GCore.Elements.Variable import Variablefrom GCore.FuncCall import FuncCallfrom GCore.Elements.Loop import Loopfrom GCore.OpCards.DrawCards import DrawCardsfrom GCore.OpCards.DealCards import DealCardsfrom GCore.OpCards.PickCards import PickCardsfrom GCore.OpCards.SendCards import SendCardsfrom GCore.Elements.ActRef import ActReffrom GCore.Elements.ActOpts import ActOptsfrom GCore.Elements.ExitLoop import ExitLoopfrom GCore.Elements.ExitRound import ExitRoundfrom GCore.Elements.PubMsg import PubMsgfrom GCore.Elements.Proc import Procfrom GCore.Elements.Delay import Delayfrom GCore.Elements.Action import Actionfrom GCore.Elements.ProcRef import ProcReffrom GCore.Elements.Ret import Retfrom GCore.OpCards.PlayCards import PlayCardsfrom GCore.ValueType import ValueTypefrom GCore.Return import Returnfrom GCore.VarRef import VarReffrom Mains import Logimport GCore.ValueTypeimport GCore.VarsSpace as VarsSpaceimport GCore.Operatortag_name_action = "action"tag_name_actions = "actions"tag_name_act_opts = "act_opts"tag_name_act_ref = "act_ref"tag_name_act_refs = "act_refs"   # acts will be listed in a varialbletag_name_attr = "attr"tag_name_attrs = "attrs"tag_name_card = "card"tag_name_cards = "cards"tag_name_case = "case"tag_name_cases = "cases"tag_name_check_param = "check_param"tag_name_draw_cards = "draw_cards" #draw some cards from the card stack, but without dealing them to a playertag_name_deal_cards = "deal_cards" #deal some cards to player, from the card stack <==> draw_cards + send_cardstag_name_delay = "delay" # sleeping for secondstag_name_else = "else"tag_name_exeref = "exeref"tag_name_exit_loop = "exitloop"tag_name_exit_round = "exitround"tag_name_find_player = "find_player"tag_name_find_players = "find_players"tag_name_ift = "ift" # if testtag_name_lets = "lets"tag_name_let = "let"tag_name_loop = "loop"tag_name_loop_until = "loop_until"tag_name_pick_cards = "pick_cards"tag_name_playcards = "playcards"tag_name_pub_act = "pub_act"tag_name_pub_msg = "pub_msg"tag_name_pub_player_status = "pub_player_status"tag_name_pub_round_status="pub_round_status"tag_name_proc = "proc"tag_name_proc_ref = "proc_ref"tag_name_property = "property"tag_name_properties = "properties"tag_name_ret = "ret"tag_name_scene = "scene"tag_name_send_cards = "send_cards" #send the cards drawn to a playertag_name_then = "then"tag_name_update = "update"tag_name_var = "var"tag_name_vars = "vars"tag_name_update_player = "update_player"tag_name_update_players = "update_players"tag_name_when = "when"attr_name_act = "act"attr_name_acts = "acts"attr_name_alias = "alias"attr_name_args = "args"attr_name_attr = "attr"attr_name_attrs = "attrs"attr_name_cards = "cards"attr_name_cards_face_up = "cards_face_up"attr_name_count = "count"attr_name_cfigure = "cfigure"attr_name_ctype = "ctype"attr_name_exer = "exer"attr_name_from_player = "from_player"attr_name_hidden = "hidden"attr_name_leading = "leading"attr_name_max = "max"attr_name_min = "min"attr_name_msg = "msg"attr_name_name = "name"attr_name_op = "op"attr_name_param = "param"attr_name_params = "params"attr_name_player = "player"attr_name_players = "players"attr_name_power = "power"attr_name_proc = "proc"attr_name_property = "property"attr_name_pub_status = "pub_status"attr_name_seconds = "seconds"attr_name_step = "step"attr_name_targets = "targets"attr_name_timeout = "timeout"attr_name_timeout_act = "timeout_act"attr_name_to_var = "to_var"attr_name_to_player = "to_player"attr_name_to_players = "to_players"attr_name_value="value"attr_name_value_of = "value_of"attr_name_value_type = "value_type"attr_name_ret_as = "ret_as"attr_name_ret_is = "ret_is"attr_name_ret_not_is = "ret_not_is"attr_name_ret_not_as = "ret_not_as"attr_name_ret_lt = "ret_lt"attr_name_ret_lt_as = "ret_lt_as"attr_name_ret_not_lt = "ret_not_lt"attr_name_ret_not_lt_as = "ret_not_lt_as"attr_name_ret_gt = "ret_gt"attr_name_ret_gt_as = "ret_gt_as"attr_name_ret_not_gt = "ret_not_gt"attr_name_ret_not_gt_as = "ret_not_gt_as"attr_val_op_and = "and"attr_val_op_or = "or"attr_val_op_not = "not"attr_val_op_add = "add"attr_val_op_subtract = "subtract"attr_val_op_multiply = "multiply"attr_val_op_append = "append"attr_val_op_remove = "remove"statement_regex_pattern = "^:\((.*)\)$"statement_regex_variable = "^@([a-zA-Z][\w.]*)$"statement_regex_var_def = "^var\s+\w+\s*$"statement_regex_func_call = "^\w+\(.*\)$"statement_regex_proc_call = "^#\w+\(.*\)$"proc_name_ctype_of = "ctype_of"proc_name_cfigure_of = "cfigure_of"def parse_elem_action(xmlNode, gRule = None):    ret = check_elem_attributes(xmlNode, attr_name_name)    if not ret:        return None    actName = ret[attr_name_name]    act = Action(actName)    set_statement_step(xmlNode, act)    elemCheckParam = Utils.getXmlFirstNamedChild(tag_name_check_param, xmlNode)    if elemCheckParam:        tempChilds = Utils.getXmlChildElments(elemCheckParam)        if tempChilds:            ckStm = parse_elem(tempChilds[0], gRule)            act.set_check_param_statement(ckStm)    for elem in Utils.getXmlOtherChildElements(tag_name_check_param, xmlNode):        stm = parse_elem(elem, gRule)        if stm:            act.add_statement(stm)    gRule.add_act(act, xmlNode)    return actdef parse_elem_act_opts(xmlNode, gRule = None):    ret = check_elem_attributes(xmlNode, attr_name_to_player, attr_name_timeout, attr_name_timeout_act)    if not ret:        return None    player = ret[attr_name_to_player]    timeout = ret[attr_name_timeout]    outAct = ret[attr_name_timeout_act]    if not gRule.is_act_exists(outAct):        Log.error("Refer to not existing act:{0}, xmlnode:{1}".format(outAct, xmlNode.toxml()))    player = parse_attribute_text(xmlNode, player, gRule)    act_opts = ActOpts(player, timeout, outAct)    set_statement_step(xmlNode, act_opts)    for elem in Utils.getXmlChildElments(xmlNode):        act_opt = parse_elem_act_ref(elem, gRule)        if act_opt:            act_opts.add_act_opt(act_opt)    return act_optsdef parse_elem_act_ref(xmlNode, gRule = None):    if not xmlNode.hasAttribute(attr_name_act):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_act, xmlNode.toxml()))        return None    actName = xmlNode.getAttribute(attr_name_act)    if not gRule.is_act_exists(actName):        Log.error("Refer to not existing act:{0}, xmlnode:{1}".format(actName, xmlNode.toxml()))    param = None    hidden = False    if xmlNode.hasAttribute(attr_name_param):        param = xmlNode.getAttribute(attr_name_param)        param = parse_attribute_text(xmlNode, param, gRule)    if xmlNode.hasAttribute(attr_name_hidden):        hid = xmlNode.getAttribute(attr_name_hidden)        if hid.lower().startswith("t"):            hidden = True    act_opt = ActRef(actName, param, hidden)    set_statement_step(xmlNode, act_opt)    return act_optdef parse_elem_attr(xmlNode, gRule = None, prefix="scene."):    ret = check_elem_attributes(xmlNode, attr_name_name, attr_name_value, attr_name_value_type)    if not ret:        return None    vName = ret[attr_name_name]    sType = ret[attr_name_value_type]    vType = GCore.ValueType.parse_from_str(sType)    pub_status = True if xmlNode.hasAttribute(attr_name_pub_status) else False    if vType == ValueType.undef:        Log.error("Invalid var value type:" + xmlNode.toxml())        return None    value = ret[attr_name_value]    vObj = parse_attribute_text(xmlNode, value, gRule)    var = Variable(vName)    var.set_value_type(vType)    var.set_value(vObj)    if pub_status:        var.set_pub_status()    gRule.add_var(Variable(prefix + vName), xmlNode)    return vardef parse_elem_var(xmlNode, gRule = None):    if not xmlNode.hasAttribute(attr_name_name):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_name, xmlNode.toxml()))        return None    if not xmlNode.hasAttribute(attr_name_value):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_value, xmlNode.toxml()))        return None    if not xmlNode.hasAttribute(attr_name_value_type):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_value_type, xmlNode.toxml()))        return None    vName = xmlNode.getAttribute(attr_name_name)    sType = xmlNode.getAttribute(attr_name_value_type)    vType = GCore.ValueType.parse_from_str(sType)    if vType == ValueType.undef:        Log.error("Invalid var value type:" + xmlNode.toxml())        return None    value = xmlNode.getAttribute(attr_name_value)    vObj = parse_attribute_text(xmlNode, value, gRule)    var = Variable(vName)    var.set_value_type(vType)    var.set_value(vObj)    gRule.add_var(var, xmlNode)    set_statement_step(xmlNode, var)    return vardef parse_elem_delay(xmlNode, gRule = None):    if not xmlNode.hasAttribute(attr_name_seconds):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_seconds, xmlNode.toxml()))        return None    secs = xmlNode.getAttribute(attr_name_seconds)    delay = Delay(int(secs))    set_statement_step(xmlNode, delay)    return delaydef parse_elem_deal_cards(xmlNode, gRule = None):    ret = check_elem_attributes(xmlNode, attr_name_player, attr_name_count)    if not ret:        return None    player = parse_attribute_text(xmlNode, ret[attr_name_player], gRule)    count = int(ret[attr_name_count])    obj = DealCards(count, player)    set_statement_step(xmlNode, obj)    return  objdef parse_elem_draw_cards(xmlNode, gRule = None):    ret = check_elem_attributes(xmlNode, attr_name_to_var, attr_name_count)    if not ret :        return None    count = xmlNode.getAttribute(attr_name_count)    to_var = xmlNode.getAttribute(attr_name_to_var)    to_var = parse_attribute_text(xmlNode, to_var, gRule)    drawCards = DrawCards(to_var, int(count))    set_statement_step(xmlNode, drawCards)    return drawCardsdef parse_elem_exitloop(xmlNode, gRule = None):    inst =  ExitLoop()    set_statement_step(xmlNode, inst)    return instdef parse_elem_exitround(xmlNode, gRule = None):    inst = ExitRound()    set_statement_step(xmlNode, inst)    return instdef parse_elem_loop(xmlNode, gRule = None):    loop = Loop()    set_statement_step(xmlNode, loop)    for elem in Utils.getXmlChildElments(xmlNode):        s = parse_elem(elem,gRule)        if s:            if type(s) is Clause:                true_stms = s.get_true_statements()                if len(true_stms) == 1 and type(true_stms[0]) is ExitLoop:                    loop.set_exit_case(s)                else:                    loop.add_clause(s)            else:                loop.add_clause(s)    return loopdef parse_elem_loop_until(xmlNode, gRule = None):    caseStm = parse_elem_case(xmlNode,gRule)    if not caseStm:        return None    loop = parse_elem_loop(xmlNode,gRule)    if loop:        loop.set_exit_case(caseStm)    return loop# <playcards player="@cmd_player" cards="@round.koupai" alias="kuopai" face_up="false"/>def parse_elem_play_cards(xmlNode, gRule = None):    attrs = check_elem_attributes(xmlNode, attr_name_player, attr_name_cards, attr_name_alias, attr_name_cards_face_up)    player = parse_attribute_text(xmlNode, attrs[attr_name_player], gRule)    cards = parse_attribute_text(xmlNode, attrs[attr_name_cards],gRule)    faceUp = parse_attribute_text(xmlNode, attrs[attr_name_cards_face_up],gRule)    alias = xmlNode.getAttribute(attr_name_alias)    playCards = PlayCards(player, cards, alias, faceUp)    set_statement_step(xmlNode, playCards)    return playCardsdef parse_elem_pick_cards(xmlNode, gRule = None):    attrs = check_elem_attributes(xmlNode, attr_name_to_var, attr_name_from_player, attr_name_count)    fromPlayer = parse_attribute_text(xmlNode, attrs[attr_name_from_player], gRule)    toVar =  parse_attribute_text(xmlNode, attrs[attr_name_to_var],gRule)    count = parse_attribute_text(xmlNode, attrs[attr_name_count],gRule)    inst = PickCards(count, fromPlayer, toVar)    set_statement_step(xmlNode, inst)    return instdef parse_elem_proc_ref(xmlNode, gRule = None):    if not xmlNode.hasAttribute(attr_name_proc):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_proc, xmlNode.toxml()))        return None    procName = xmlNode.getAttribute(attr_name_proc)    if not gRule.is_proc_exists(procName):        Log.error("Refered to not existing proc:{0},xmlnode:{1}".format(procName, xmlNode.toxml()))    procRef = ProcRef(procName)    set_statement_step(xmlNode, procRef)    return procRefdef parse_elem_proc(xmlNode, gRule = None):    if not xmlNode.hasAttribute(attr_name_name):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_name, xmlNode.toxml()))        return None    name = xmlNode.getAttribute(attr_name_name)    params = []    if xmlNode.hasAttribute(attr_name_params):        ps = xmlNode.getAttribute(attr_name_params).split(',')        for p in ps:            params.append(Variable(p.strip()))    proc = Proc(name, params)    for elem in Utils.getXmlChildElments(xmlNode):        stm = parse_elem(elem, gRule)        if stm:            proc.add_statement(stm)    gRule.add_proc(proc, xmlNode)    set_statement_step(xmlNode, proc)    return procdef parse_elem_pub_act(xmlNode, gRule=None):    ret = check_elem_attributes(xmlNode, attr_name_exer, attr_name_to_players, attr_name_act, attr_name_args)    if not ret:        return None    exe_player = parse_attribute_text(xmlNode, ret[attr_name_exer], gRule)    to_players = parse_attribute_text(xmlNode, ret[attr_name_to_players], gRule)    act = ret[attr_name_act]    act_args = parse_attribute_text(xmlNode, ret[attr_name_args], gRule)    pubAct = PubAct(exe_player, to_players, act, act_args)    set_statement_step(xmlNode, pubAct)    return pubActdef parse_elem_pub_msg(xmlNode, gRule = None):    ret = check_elem_attributes(xmlNode, attr_name_players, attr_name_msg)    if not ret:        return None    players = parse_attribute_text(xmlNode, ret[attr_name_players], gRule)    msg = parse_attribute_text(xmlNode, ret[attr_name_msg], gRule)    inst = PubMsg(players, msg)    set_statement_step(xmlNode, inst)    return instdef parse_elem_pub_player_status(xmlNode, gRule = None):    ret = check_elem_attributes(xmlNode, attr_name_players)    if not ret:        return None    players = parse_attribute_text(xmlNode, ret[attr_name_players], gRule)    inst = PubPlayerStatus(players)    set_statement_step(xmlNode,inst)    return instdef parse_elem_pub_round_status(xmlNode, gRule=None):    ret = check_elem_attributes(xmlNode, attr_name_players)    if not ret:        return None    players = parse_attribute_text(xmlNode, ret[attr_name_players], gRule)    inst = PubRoundStatus(players)    set_statement_step(xmlNode, inst)    return instdef parse_elem_ret(xmlNode, gRule = None):    if not xmlNode.hasAttribute(attr_name_value):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_value, xmlNode.toxml()))        return None    value = xmlNode.getAttribute(attr_name_value)    value = parse_attribute_text(xmlNode, value, gRule)    retObj = Ret(value)    set_statement_step(xmlNode, retObj)    return retObjdef parse_elem_send_cards(xmlNode, gRule = None):    if not xmlNode.hasAttribute(attr_name_player):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_player, xmlNode.toxml()))        return None    if not xmlNode.hasAttribute(attr_name_cards):        Log.error("lack of attr:{0}, xmlnode:{1}".format(attr_name_cards, xmlNode.toxml()))        return None    attrPlayer = xmlNode.getAttribute(attr_name_player)    attrCards = xmlNode.getAttribute(attr_name_cards)    playerObj = parse_attribute_text(xmlNode, attrPlayer,gRule)    cardsObj = parse_attribute_text(xmlNode, attrCards,gRule)    inst = SendCards(cardsObj, playerObj)    set_statement_step(xmlNode, inst)    return instdef parse_elem(xmlElem, gRule = None):    if type(xmlElem) is not xml.dom.minidom.Element:        return None    if xmlElem.tagName == tag_name_action:        return parse_elem_action(xmlElem,gRule)    elif xmlElem.tagName == tag_name_act_ref:        return parse_elem_act_ref(xmlElem,gRule)    elif xmlElem.tagName == tag_name_act_opts:        return parse_elem_act_opts(xmlElem,gRule)    elif xmlElem.tagName == tag_name_cases:        return parse_elem_cases(xmlElem,gRule)    elif xmlElem.tagName == tag_name_deal_cards:        return parse_elem_deal_cards(xmlElem,gRule)    elif xmlElem.tagName == tag_name_delay:        return parse_elem_delay(xmlElem,gRule)    elif xmlElem.tagName == tag_name_draw_cards:        return parse_elem_draw_cards(xmlElem,gRule)    elif xmlElem.tagName == tag_name_exit_loop:        return parse_elem_exitloop(xmlElem,gRule)    elif xmlElem.tagName == tag_name_exit_round:        return parse_elem_exitround(xmlElem,gRule)    elif xmlElem.tagName == tag_name_ift:        return parse_elem_ift(xmlElem,gRule)    elif xmlElem.tagName == tag_name_let:        return parse_elem_let(xmlElem,gRule)    elif xmlElem.tagName == tag_name_lets:        return parse_elem_lets(xmlElem,gRule)    elif xmlElem.tagName == tag_name_loop:        return parse_elem_loop(xmlElem,gRule)    elif xmlElem.tagName == tag_name_loop_until:        return parse_elem_loop_until(xmlElem,gRule)    elif xmlElem.tagName == tag_name_pick_cards:        return parse_elem_pick_cards(xmlElem,gRule)    elif xmlElem.tagName == tag_name_playcards:        return parse_elem_play_cards(xmlElem,gRule)    elif xmlElem.tagName == tag_name_proc:        return parse_elem_proc(xmlElem,gRule)    elif xmlElem.tagName == tag_name_proc_ref:        return parse_elem_proc_ref(xmlElem,gRule)    elif xmlElem.tagName == tag_name_pub_act:        return parse_elem_pub_act(xmlElem, gRule)    elif xmlElem.tagName == tag_name_pub_msg:        return parse_elem_pub_msg(xmlElem,gRule)    elif xmlElem.tagName == tag_name_pub_player_status:        return parse_elem_pub_player_status(xmlElem,gRule)    elif xmlElem.tagName == tag_name_pub_round_status:        return parse_elem_pub_round_status(xmlElem, gRule)    elif xmlElem.tagName == tag_name_ret:        return parse_elem_ret(xmlElem,gRule)    elif xmlElem.tagName == tag_name_send_cards:        return parse_elem_send_cards(xmlElem,gRule)    elif xmlElem.tagName == tag_name_update:        return parse_elem_update(xmlElem,gRule)    elif xmlElem.tagName == tag_name_var:        return parse_elem_var(xmlElem,gRule)    else:        return Nonedef parse_elem_cases(xmlElem, gRule = None):    op = Operator.And    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    caseElems = Utils.getXmlNamedChildElments(tag_name_case, xmlElem)    if not caseElems:        return None    caseObjs = []    for c in caseElems:        case = parse_elem_case(c,gRule)        if case:            caseObjs.append(case)    if caseObjs:        if len(caseObjs) > 1:            caseInst = Cases(op)            for co in caseObjs:                caseInst.add_case(co)            set_statement_step(xmlElem, caseInst)            return caseInst        else:            return caseObjs[0]    else:        return None# cases ... [then] ...[else]def parse_elem_ift(xmlElem, gRule = None):    clause = Clause()    casesNode = Utils.getXmlFirstNamedChild(tag_name_cases, xmlElem)    if casesNode:        clause.set_case(parse_elem_cases(casesNode,gRule))    else:        caseNode = Utils.getXmlFirstNamedChild(tag_name_case, xmlElem)        if caseNode:            caseInst = parse_elem_case(caseNode,gRule)            if caseInst:                clause.set_case(caseInst)        else:            caseInst = parse_elem_case(xmlElem,gRule)            if caseInst:                clause.set_case(caseInst)    if not clause.get_case():        Log.error("Invalid ift element:" + xmlElem.toxml())        return    childElems = Utils.getXmlChildElments(xmlElem)    for e in childElems:        if e.tagName == tag_name_case or e.tagName == tag_name_cases:            continue        if e.tagName == tag_name_else:            false_ups = parse_elem_else(e,gRule)            clause.set_false_statements(false_ups)        elif e.tagName == tag_name_then:            true_ups = parse_elem_then(e,gRule)            clause.set_true_statements(true_ups)        else:            stm = parse_elem(e,gRule)            if stm:                clause.add_true_statement(stm)    set_statement_step(xmlElem, clause)    return clausedef parse_elem_let(xmlElem, gRule = None):    update = parse_elem_update(xmlElem,gRule)    if not update:        return None    whenNode = Utils.getXmlFirstNamedChild(tag_name_when, xmlElem)    if not whenNode:        return update    if not whenNode.hasChildNodes():        case = parse_elem_case(whenNode,gRule)        update.set_exe_case(case)    else:        case = parse_elem_cases(whenNode,gRule)        update.set_exe_case(case)    return updatedef parse_elem_lets(xmlElem, gRule = None):    if not xmlElem.hasChildNodes():        return None    # usage lets/let ... when    lets = Utils.getXmlNamedChildElments(tag_name_let, xmlElem)    if not lets:        return None    clause = Clause()    for l in lets:        update = parse_elem_let(l,gRule)        if update:            clause.add_true_statement(update)    when = Utils.getXmlFirstNamedChild(tag_name_when, xmlElem)    if when:        clause.set_case(when)    return clausedef parse_elem_update(xmlElem, gRule = None):    attrs = check_elem_attributes(xmlElem, attr_name_property, attr_name_value)    if not attrs:        return None    prop = parse_attribute_text(xmlElem, attrs[attr_name_property],gRule)    val = parse_attribute_text(xmlElem, attrs[attr_name_value],gRule)    op = Operator.Update    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    gRule.check_op_var(attrs[attr_name_property].lstrip('@'), op, xmlElem)    inst =  Update(prop, val, op)    set_statement_step(xmlElem, inst)    return instdef parse_elem_then(xmlElem, gRule = None):    stms = []    childElems = Utils.getXmlChildElments(xmlElem)    for el in childElems:        up = parse_elem(el,gRule)        stms.append(up)    return stmsdef parse_elem_case(xmlElem, gRule = None):    ret = is_valid_case_element(xmlElem)    if not ret[0]:        return None    return create_case_instance(xmlElem, ret[1], ret[2], ret[3],gRule)def parse_codes_attr_text(xmlElement, codeTxt, gRule = None):    txt = codeTxt[2:-1]    lines = txt.split(';')    if len(lines) > 1:        return parse_block(xmlElement, lines,gRule)    else:        return parse_operation(xmlElement, txt,gRule)def parse_builtin_value( attrTxt, gRule = None):    if attrTxt.isdigit():        return CValue(int(attrTxt))    elif attrTxt.lower() == "none" or attrTxt.lower() == "null" :        return CValue(None)    elif attrTxt.lower() == "false" or attrTxt.lower() == "true":        return CValue(True if attrTxt.lower() == 'true' else False)    else:        return None# <case value_of=":(is_cards_contain_cfigure(@trick.played_cards,@score_cards))" ret_is="true"/># find_player(IsDefender:true ## IsMainPlayer:true)  ## <==> &&# find_player(IsDefender:true || IsMainPlayer:true)  || <==> ||# filter_inst(@round.players, IsDefender:true ## IsMainPlayer:true)# <update property="@round.bank_ctype" value=":(ctype_of(element_at(@cmd_param, 0)))"/># property="@round.winners.[].IsDefender"  .[]. 遍历def parse_attribute_text(xmlElement, attrTxt, gRule = None):    valObj = parse_builtin_value(attrTxt)    if valObj:        valObj.set_xml_node(xmlElement)        return valObj    elif attrTxt.lower() == "random":        valObj = CValue(attrTxt)        valObj.set_xml_node(xmlElement)        return valObj    elif attrTxt.startswith("list%"):        # format : list:s1,s2,s3   | list:s1,@s2,s3        elems = []        ps = attrTxt[5:].split(',')        for p in ps:            if p .startswith('@'):                elems.append(VarRef(p))                if not gRule.is_var_exists(p.lstrip('@')):                    Log.error("Refered to not existing var:{0},xmlnode:{1}".format(p, xmlElement.toxml()))            else:                elems.append(CValue(p))        valObj = GArray(elems)        valObj.set_xml_node(xmlElement)        return valObj    elif attrTxt.startswith("str%"):        valObj = CValue(attrTxt[4:])        valObj.set_xml_node(xmlElement)        return valObj    elif attrTxt.startswith("int%"):        valObj = CValue(int(attrTxt[4:]))        valObj.set_xml_node(xmlElement)        return valObj    elif attrTxt.startswith('@'):        varObj = VarRef(attrTxt)        varObj.set_xml_node(xmlElement)        if not gRule.is_var_exists(attrTxt.lstrip('@')):            Log.error("Refered to not existing var:{0},xmlnode:{1}".format(attrTxt, xmlElement.toxml()))        return varObj    elif is_code_block(attrTxt):        return parse_codes_attr_text(xmlElement, attrTxt, gRule)    elif len(attrTxt) > 0:        Log.warn("String {0} is used as a value, not a number.".format(attrTxt))        valObj = CValue(attrTxt)        valObj.set_xml_node(xmlElement)        return valObj    else:        return Nonedef check_elem_attributes(xmlElem, *args):    attrs = {}    for arg in args:        if not xmlElem.hasAttribute(arg):            Log.error("lack of attr:{0}, xmlnode:{1}".format(arg, xmlElem.toxml()))            return None        else:            val = xmlElem.getAttribute(arg)            attrs[arg] = val    return attrsdef is_valid_case_element(xmlElem):    if not xmlElem or not xmlElem.hasAttribute(attr_name_value_of):        Log.error("Invalid case element:" + xmlElem.toxml())        return False, None, None, None    testee = xmlElem.getAttribute(attr_name_value_of)    if xmlElem.hasAttribute(attr_name_ret_is):        return True, testee, Operator.Equal, xmlElem.getAttribute(attr_name_ret_is)    if xmlElem.hasAttribute(attr_name_ret_as):        return True, testee, Operator.Equal, xmlElem.getAttribute(attr_name_ret_as)    if xmlElem.hasAttribute(attr_name_ret_not_is):        return True, testee, Operator.NotEqual, xmlElem.getAttribute(attr_name_ret_not_is)    if xmlElem.hasAttribute(attr_name_ret_not_as):        return True, testee, Operator.NotEqual, xmlElem.getAttribute(attr_name_ret_not_as)    if xmlElem.hasAttribute(attr_name_ret_lt):        return True, testee, Operator.LessThan, xmlElem.getAttribute(attr_name_ret_lt)    if xmlElem.hasAttribute(attr_name_ret_lt_as):        return True, testee, Operator.LessThan, xmlElem.getAttribute(attr_name_ret_lt_as)    if xmlElem.hasAttribute(attr_name_ret_not_lt):        return True, testee, Operator.NotLessThan, xmlElem.getAttribute(attr_name_ret_not_lt)    if xmlElem.hasAttribute(attr_name_ret_not_lt_as):        return True, testee, Operator.NotLessThan, xmlElem.getAttribute(attr_name_ret_not_lt_as)    if xmlElem.hasAttribute(attr_name_ret_gt):        return True, testee, Operator.GreaterThan, xmlElem.getAttribute(attr_name_ret_gt)    if xmlElem.hasAttribute(attr_name_ret_gt_as):        return True, testee, Operator.GreaterThan, xmlElem.getAttribute(attr_name_ret_gt_as)    if xmlElem.hasAttribute(attr_name_ret_not_gt):        return True, testee, Operator.NotGreaterThan, xmlElem.getAttribute(attr_name_ret_not_gt)    if xmlElem.hasAttribute(attr_name_ret_not_gt_as):        return True, testee, Operator.NotGreaterThan, xmlElem.getAttribute(attr_name_ret_not_gt_as)    Log.error("Invalid case element:" + xmlElem.toxml())    return False, None, None, Nonedef parse_elem_when(xmlElem,gRule=None):    op = Operator.And    if xmlElem.hasAttribute(attr_name_op):        op = GCore.Operator.from_str(xmlElem.getAttribute(attr_name_op))    ret = is_valid_case_element(xmlElem)    caseObjs = []    if ret[0]:        caseInst = create_case_instance(ret[1], ret[2], ret[3],gRule)        if caseInst:            caseObjs.append(caseInst)    childElems = Utils.getXmlChildElments(xmlElem)    if childElems:        for child in childElems:            if child.tagName == tag_name_case:                caseInst = parse_elem_case(child,gRule)                if caseInst:                    caseObjs.append(caseInst)            elif child.tagName == tag_name_cases:                caseInst = parse_elem_cases(child,gRule)                if caseInst:                    caseObjs.append(caseInst)    # merge the cases    if caseObjs:        if len(caseObjs) > 1:            caseInst = Cases(op)            for co in caseObjs:                caseInst.add_case(co)            return caseInst        else:            return caseObjs[0]    else:        return Nonedef parse_elem_else(xmlElem,gRule=None):    stms = []    childElems = Utils.getXmlChildElments(xmlElem)    for el in childElems:        if el.tagName == tag_name_then:            ups = parse_elem_then(xmlElem,gRule)            if ups:                stms.extend(ups)        else:            up = parse_elem(el,gRule)            stms.append(up)    return stms# <case value_of=":(is_cards_contain_cfigure(@trick.played_cards,@score_cards))" ret_is="true"/># find_player(IsDefender:true ## IsMainPlayer:true)  ## <==> &&# find_player(IsDefender:true || IsMainPlayer:true)  || <==> ||# filter_inst(@round.players, IsDefender:true ## IsMainPlayer:true)def parse_func_named_arguments(xmlNode, args, split="&&", gRule=None):    ret = {}    cons = args.split(split)    for c in cons:        ps = c.split(':')        if len(ps) != 2:            Log.error("Invalid named argument:" + c)            continue        ret[ps[0]] = parse_attribute_text(xmlNode, ps[1],gRule)    return retdef parse_return_statement(xmlElem, codeText, gRule=None):    retObj = Return(codeText)    retObj.set_xml_node(xmlElem)    set_statement_step(xmlElem, retObj)    return retObjdef parse_func_call(xmlElem, codeText, gRule=None):    pos = codeText.index('(')    funcName = codeText[0 : pos]    funcCall = FuncCall(funcName)    funcCall.set_xml_node(xmlElem)    argsStr = codeText[pos + 1 : -1].strip()    if len(argsStr) == 0:        funcCall.add_ordered_argument('void')        return funcCall    if is_func_call(argsStr) or is_proc_call(argsStr):        arg = parse_func_call(xmlElem, argsStr, gRule)        if arg:            funcCall.add_ordered_argument(arg)        return funcCall    else:        args = argsStr.split(',')        for arg in args:            if ':' in arg:                split = "##"                if "||" in arg:                    split = "||"                cons = parse_func_named_arguments(xmlElem, arg, split, gRule)                for k in cons.keys():                    funcCall.add_named_argument(k, cons[k])                funcCall.set_named_arg_operator(GCore.Operator.from_str(split))            else:                op = parse_attribute_text(xmlElem, arg.strip(), gRule)                if op:                    funcCall.add_ordered_argument(op)        return funcCall# <case value_of=":(is_cards_contain_cfigure(@trick.played_cards,@score_cards))" ret_is="true"/># find_player(IsDefender:true ## IsMainPlayer:true)  ## <==> &&# find_player(IsDefender:true || IsMainPlayer:true)  || <==> ||# filter_inst(@round.players, IsDefender:true ## IsMainPlayer:true)def parse_operand(xmlElement, codeTxt,gRule=None):    if codeTxt.isdigit() or codeTxt.lower() == "true" or codeTxt.lower() == "fasle":        valObj = CValue(int(codeTxt))        valObj.set_xml_node(xmlElement)        return valObj    elif codeTxt.startswith('@'):        varObj = VarRef(codeTxt)        varObj.set_xml_node(xmlElement)        if not gRule.is_var_exists(codeTxt.lstrip('@')):            Log.error("Refered to not existing var:{0},xmlnode:{1}".format(codeTxt), xmlElement.toxml())        return varObj    elif 'none' in codeTxt.lower() or 'null' in codeTxt.lower():        return None    elif is_code_block(codeTxt):        return parse_func_call(xmlElement, codeTxt, gRule)    else:        Log.error("Un recognized code text:{0},xmlnode:{1}".format(codeTxt), xmlElement.toxml())        return Nonedef record_variable(xmlElemnt, line):    varName = line.replace('var','').strip()    VarsSpace.update(xmlElemnt, varName, None)def extract_var_name(words):    return words.replace('var','').strip()# support format:#          var c#          @c = @a - 2#          @c = func(@a)#          @c = @a + @b#          @d = @c# value_of=":(cfigure_of(@drawn_card))"def parse_operation(xmlElement, line, gRule=None):    line = line.strip()    if is_var_defination(line):        varName = line.replace('var','').strip()        var = Variable(varName)        gRule.add_var(var, xmlElement)        return var    if is_func_call(line) or is_proc_call(line):        return parse_func_call(xmlElement, line, gRule)    if is_return(line):        return parse_return_statement(xmlElement, line, gRule)    ps = re.split('\s*=\s*', line)    if len(ps) != 2:        Log.error("Invalid code line:" + line)        return None    varName = extract_var_name(ps[0])    lVar = VarRef("@" + varName.lstrip('@'))    if not gRule.is_var_exists(varName):        Log.error("Refered to not existing var:{0},code line:{1}".format(varName, line))    rhd = None    if is_func_call(ps[1]):        rhd = parse_func_call(xmlElement, ps[1],gRule)    else:        mat = re.match(r'(?P<p1>.+)\s*(?P<op>\+|-|\*|/)\s*(?P<p2>.+)', line)        if mat:            # @a - 2 | @a + @b            operator = mat.groupdict()['op']            p1 = mat.groupdict()['p1']            p2 = mat.groupdict()['p2']            op1 = parse_attribute_text(xmlElement, p1,gRule)            op2 = parse_attribute_text(xmlElement, p2,gRule)            rhd = Operation(op1, op2, from_str(operator))        else:            rhd = parse_attribute_text(xmlElement, line,gRule)    upObj = Update(lVar, rhd)    return upObjdef parse_block(xmlElement, lines,gRule=None):    block = Block()    for l in lines:        op = parse_operation(xmlElement, l,gRule)        block.add_operation(op)    block.set_xml_node(xmlElement)    return blockdef create_case_instance(xmlElem, testee, compareOp, compareVal, gRule=None):    op1 = parse_attribute_text(xmlElem, testee, gRule)    op2 = parse_attribute_text(xmlElem, compareVal, gRule)    inst =  Case(op1, op2, compareOp)    set_statement_step(xmlElem, inst)    return instdef set_statement_step(xmlNode, stm):    if xmlNode.hasAttribute(attr_name_step):        stm.set_step(xmlNode.getAttribute(attr_name_step))    stm.set_xml_text(xmlNode)def is_var_ref(text):    if re.match(statement_regex_variable, text):        return True    else:        return Falsedef is_str_statement(text):    if re.match(statement_regex_pattern, text):        return True    else:        return Falsedef is_var_defination(line):    if re.match(statement_regex_var_def, line):        return True    else:        return Falsedef is_code_block(text):    if text.startswith(":("):        return True    else:        return Falsedef is_func_call(text):    if re.match(statement_regex_func_call, text):        return True    else:        return Falsedef is_proc_call(text):    if re.match(statement_regex_proc_call, text):        return True    else:        return Falsedef is_return(text):    if re.match("return\s+@?\w+\s*", text):        return True    else:        return Falsedef get_variable_name(var):    if var.startswith('@'):        return var.lstrip('@')    else:        return var
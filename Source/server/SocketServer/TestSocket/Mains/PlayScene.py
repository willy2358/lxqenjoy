import random

from GRules.RulePart_Cards import RulePart_Cards
from GRules.RulePart_Actions import RulePart_Actions
from GRules.RulePart_Following import RulePart_Following
from GRules.RulePart_Players import RulePart_Players
from GRules.RulePart_Round import RulePart_Round
from GRules.RulePart_Running import RulePart_Running
from GRules.RulePart_Scene import RulePart_Scene
from GRules.RulePart_Procs import RulePart_Procs

from GCore.Elements.Variable import Variable
from GCore.Elements.Loop import Loop

from GCore.Elements.ActRef import ActRef
from GCore.Elements.ProcRef import ProcRef
from GCore.Elements.Action import Action
from GCore.Elements.Delay import Delay
from GCore.Elements.PubMsg import PubMsg
from GCore.Elements.Clause import Clause
from GCore.Elements.ActOpts import ActOpts
from GCore.Elements.Case import Case
from GCore.Elements.Cases import Cases
from GCore.VarRef import VarRef
from Mains.Player import Player
from GCore.FuncCall import FuncCall
from GCore.GArray import GArray

from Mains.GVar import GVar
from GCore.ValueType import ValueType
from Mains.ExtAttrs import ExtAttrs
from Mains.Round import Round
from Cards import Card
from GCore.CValue import CValue
from Cards.CFigure import CFigure

from Mains import Errors
import Mains.InterProtocol as InterProtocol

import Utils

class PlayScene(ExtAttrs):
    def __init__(self, rule):
        super(PlayScene, self).__init__()
        self.__cur_round = None
        self.__history_rounds = []
        self.__players = []
        self.__rule = rule
        self.__runtimes = []
        self.__cards_space = []
        self.__pending_player = None
        self.__pending_cmds = None
        self.__pending_seconds = 0
        self.__timeout_cmd = None

        # for exec action
        self.__cmd_player = None
        self.__cmd_param = None

        self.__local_vars = {}
        self.__procs = {}
        self.__actions = {} # {act_name: func}
        self.parse_rule(self.__rule)

    def is_player_in(self, player):
        return player in self.__players

    def get_players(self):
        return self.__players

    def get_rule(self):
        return self.__rule

    def get_next_player(self, ref_player):
        idx = self.__players.index(ref_player)
        idx += 1
        if idx >= len(self.__players):
            idx = 0

        return self.__players[idx]

    def get_proc_local_var(self, varName):
        if varName in self.__local_vars:
            return self.__local_vars[varName]
        else:
            return None

    def get_runtime_objs(self, varStr):
        if varStr.startswith("@round."):
            r = self.get_current_round()
            return r.get_attr(varStr[len("@round."):])
        elif varStr.startswith("@scene."):
            return self.get_attr(varStr[len("@scene."):])
        elif varStr.startswith("@#"):
            return self.get_proc_local_var(varStr.lstrip("@"))
        elif varStr.startswith("@"):
            return self.get_var(varStr.lstrip("@"))
        else:
            return None

    def get_obj_value(self, obj):
        if isinstance(obj, CFigure):
            return int(obj)
        elif isinstance(obj, int) or isinstance(obj, bool) or isinstance(obj, str):
            return obj
        elif isinstance(obj, Player):
            return obj
        elif isinstance(obj, list):
            return obj
        elif isinstance(obj, GArray):
            return obj.gen_runtime_obj(self)()
        elif type(obj) is GVar:
            return self.get_obj_value(obj.get_value())
        elif isinstance(obj, CValue):
            return obj.get_value()
        elif type(obj) is VarRef:
            return self.get_obj_value(obj.gen_runtime_obj(self)())
        elif isinstance(obj, FuncCall):
            return self.get_obj_value(obj.gen_runtime_obj(self)())
        elif callable(obj):
            return self.get_obj_value(obj())
        else:
            return None

    def get_rt_var(self, obj):
        if isinstance(obj, GVar):
            return obj
        elif isinstance(obj, VarRef):
            return self.get_rt_var(obj.gen_runtime_obj(self)())
        elif callable(obj):
            return self.get_rt_var(obj())
        else:
            return None

    def set_obj_value(self, obj, value):
        if isinstance(obj, VarRef):
            var = obj.gen_runtime_obj(self)()
            if isinstance(var, GVar):
                var.set_value(value)

    def add_proc_local_var(self, varName, vType, value):
        self.__local_vars[varName] = GVar(varName, vType, value)

    def get_current_round(self):
        return self.__cur_round

    def draw_cards(self, count):
        return  self.__cur_round.draw_cards(count)

    def add_player(self, player):
        if player not in self.__players:
            self.__players.append(player)
            self.init_player_attrs(player)
            return True
        else:
            return False

    def init_player_attrs(self, player):
        playerPart = self.__rule.get_part_by_name(RulePart_Players.PART_NAME)
        if not playerPart:
            return

        for attr in playerPart.get_custom_attrs():
            name = attr.get_name()
            vtype = attr.get_value_type()
            val = attr.get_value()
            player.add_cus_attr(name, vtype, val)

    def _append_rt_obj(self, obj):
        self.__runtimes.append(obj)


    def remove_player(self, player):
        if player in self.__players:
            self.__players.remove(player)
            return True
        return False

    def has_vacancy(self):
        return len(self.__players) < self.__rule.get_max_players_capacity()

    def parse_rule(self, rule):
        self.load_cards_space(rule)
        self.load_scene_attrs(rule)
        self.load_procedures(rule)
        self.load_actions(rule)

        partRun = rule.get_part_by_name(RulePart_Running.PART_NAME)
        assert partRun
        rt = None
        for stm in partRun.get_statements():
            obj = stm.gen_runtime_obj(self)
            if obj:
                self._append_rt_obj(obj)

    def load_cards_space(self, rule):
        cards_set= Card.get_cards(rule.get_gtype())
        cardsPart = rule.get_part_by_name(RulePart_Cards.PART_NAME)
        if not cardsPart:
            self.__cards_space = cards_set
            return
        excludes = cardsPart.get_excluded_cards()
        for ex in excludes:
            while cards_set.index(ex) >= 0:
                cards_set.remove(ex)

        sets = 1
        c = cardsPart.get_card_sets()
        if c > 1:
            sets = c
        self.__cards_space = cards_set * sets

    def load_scene_attrs(self, rule):
        scenePart = rule.get_part_by_name(RulePart_Scene.PART_NAME)
        if scenePart:
            for attr in scenePart.get_custom_attrs():
                name = attr.get_name()
                vtype = attr.get_value_type()
                val = attr.get_value()
                self.add_cus_attr(name, vtype, val)

    def load_procedures(self, rule):
        procsPart = rule.get_part_by_name(RulePart_Procs.PART_NAME)
        for proc in procsPart.get_procs():
            func = proc.gen_runtime_obj(self)
            if callable(func):
                self.__procs[proc.get_name()] = (proc.get_param_names(), func)

    def load_actions(self, rule):
        actsPart = rule.get_part_by_name(RulePart_Actions.PART_NAME)
        if not actsPart:
            return

        for act in actsPart.get_actions():
            funcObj = act.gen_runtime_obj(self)
            if callable(funcObj):
                self.__actions[act.get_name()] = funcObj

    def start_game(self):
        self.init_player_type_attrs()
        self.create_new_round()
        for rtObj in self.__runtimes:

            rtObj()

        #
        # run_part = self.__rule.get_part_by_name(RulePart_Running.PART_NAME)
        #
        # codeBlocks = run_part.get_code_blocks()
        # for i in range(len(codeBlocks)):
        #     self.exe_block(codeBlocks[i])
    def init_player_type_attrs(self):
        if not self.__players:
            return
        attrs = self.get_attrs()
        for attr in attrs:
            # attr is a GVar
            if attrs[attr].get_value_type() == ValueType.player:
                val = attrs[attr].get_value()
                if type(val) is CValue:
                    if val.get_value() == "random":
                        attrs[attr].set_value(self.__players[0])

    def call_proc(self, proc_name, args):
        if proc_name in self.__procs:
            params = self.__procs[proc_name][0]
            if params:
                for i in range(len(params)):
                    if i < len(args):
                        gVar = self.get_proc_local_var(params[i])
                        if gVar:
                            gVar.set_value(args[i])

            return self.__procs[proc_name][1]()
        else:
            return None

    def exe_block(self, code_block):
        pass

    def create_new_round(self):
        newRound = Round()
        roundPart = self.__rule.get_part_by_name(RulePart_Round.PART_NAME)
        if roundPart:
            for attr in roundPart.get_custom_attrs():
                name = attr.get_name()
                vtype = attr.get_value_type()
                val = attr.get_value()
                newRound.add_cus_attr(name, vtype, val)

        newRound.init_cards_pack(self.__cards_space)
        self.__history_rounds.append(newRound)
        self.__cur_round = newRound


    def set_pending_player_and_cmds(self, player, cmds, timeout_seconds, timeout_act):
        self.__pending_player = player
        self.__pending_cmds = cmds
        self.__pending_seconds = timeout_seconds
        self.__timeout_cmd = timeout_act


    def process_player_exed_cmd(self, player, cmd, cmd_args):
        if player != self.__pending_player:
            player.response_err_pack(Errors.player_not_pending_cmd)
        else:
            validCmd = False
            for c in self.__pending_cmds:
                if c.get_cmd() == cmd and cmd_args == c.get_cmd_param():
                   validCmd = True

            if not validCmd:
                player.response_err_pack(Errors.invalid_cmd_or_param)
            else:
                pack = InterProtocol.create_player_exed_cmd_json_packet(cmd, cmd_args)
                for p in self.get_players():
                    p.send_server_cmd_packet(pack)

                # 准备参数
                self.__cmd_player = player
                self.__cmd_param = cmd_args

                #执行内部逻辑
                if cmd in self.__actions:
                    if callable(self.__actions[cmd]):
                        self.__actions[cmd]()







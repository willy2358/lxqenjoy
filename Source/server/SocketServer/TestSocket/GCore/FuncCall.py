
from GCore.Operand import Operand
from GCore.Operator import Operator
import GCore.Funcs as Funcs

# find_player(IsDefender:true ## IsMainPlayer:true)  ## <==> &&
# find_player(IsDefender:true || IsMainPlayer:true)  || <==> ||
# filter_inst(@round.players, IsDefender:true ## IsMainPlayer:true)
class FuncCall(Operand):
    def __init__(self, funcName):
        self.__func_name = funcName
        self.__ordered_args = []
        self.__named_args = {}
        self.__named_arg_op = Operator.And

    def add_ordered_argument(self, arg):
        self.__ordered_args.append(arg)


    def add_named_argument(self, name, value):
        self.__named_args[name] = value

    def set_named_arg_operator(self, op=Operator.And):
        self.__named_arg_op = op


    def gen_runtime_obj(self, scene):
        def func():
            if self.__ordered_args:
                return Funcs.invoke(self.__func_name, scene, self.__ordered_args)
            elif self.__named_args:
                if self.__func_name == "find_player" or self.__func_name == "find_players":
                    return self.filter_insts(scene, "@round.players")
            else:
                return None
        return func

    def filter_insts(self, scene, instsStr):
        insts = scene.get_runtime_objs(instsStr)
        if not insts:
            return []
        objs = []
        for inst in insts:
            if inst.is_meet_conditions(self.__named_args, self.__named_arg_op):
                objs.append(inst)
        return objs







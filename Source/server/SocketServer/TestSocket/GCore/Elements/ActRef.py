
from Mains.PlayCmd import PlayCmd
from GCore.Statement import Statement
import Mains.Log as Log
# from Mains.PlayScene import PlayScene

#<act_ref act="jiaozhu" param="@drawn_card"/>
class ActRef(Statement):
    def __init__(self, act_ref, param, hidden=False):
        super(ActRef, self).__init__()
        self.__ref_act_name = act_ref
        self.__param = param
        self.__hidden = hidden

    def get_act_name(self):
        return self.__ref_act_name

    def gen_runtime_obj(self, scene):
        def ret_cmd():
            Log.debug("Executing act ref:{0} ....".format(self.get_step()))
            param = scene.get_obj_value(self.__param)
            cmd = PlayCmd(None, self.__ref_act_name, scene.get_obj_value(self.__param))
            if self.__hidden:
                cmd.set_silent_flag(True)
            return cmd
        return ret_cmd





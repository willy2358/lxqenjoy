
from GCore.Statement import Statement
from Mains.Player import Player
import Mains.Log as Log

import Mains.InterProtocol as InterProtocol
# from Mains.PlayScene import PlayScene

# <act_opts timeout="30" timeout_act="pass" to_player="@drawer">
#                     <act_opt act="jiaozhu"/>
#                     <act_opt act="pass"/>
#                 </act_opts>

class ActOpts(Statement):
    def __init__(self, to_player, timeout_sec, timeout_act):
        super(ActOpts, self).__init__()
        self.__to_player = to_player
        self.__timeout_seconds = timeout_sec
        self.__timeout_act = timeout_act
        self.__opts = []

    def add_act_opt(self, act_opt):
        self.__opts.append(act_opt)

    def gen_runtime_obj(self, scene):
        def send_act_opts():
            try:
                Log.debug("Executing:{0} ....".format(self.get_step()))
                recv_player = scene.get_obj_value(self.__to_player)
                cmd_opts = []
                def_act = None
                for opt in self.__opts:
                    cmdObj = opt.gen_runtime_obj(scene)()
                    cmdObj.set_cmd_player(recv_player)
                    cmd_opts.append(cmdObj)
                    if opt.get_act_name() == self.__timeout_act:
                        def_act = cmdObj

                scene.send_player_cmd_opts(recv_player, cmd_opts, self.__timeout_seconds, def_act)
            except Exception as ex:
                Log.exception(ex)
        return send_act_opts

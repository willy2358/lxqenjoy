import threading

from Mains import Log, InterProtocol, Errors

from Rooms.Closet import Closet

def process_player_request(player, cmd, req_json):
    room = player.get_closet()
    if room:
        room.process_player_request(player, cmd, req_json)
    else:
        player.response_err_pack(cmd, Errors.did_not_call_enter_room)


class Room():
    def __init__(self, roomId):

        self._room_id = roomId
        self._seated_players = []
        self._all_players = []
        self._max_seated_players = 0
        self._min_seated_players = 0

        self._max_players_number = 10
        self._round_num = 2
        self._current_round_order = 0
        self._current_round = None
        self._fee_stuff_id = 0
        self._fee_stuff_name = ""
        self._stake_stuff_id = 0
        self._stake_stuff_name = ""
        self._last_winners = []
        self._players_total_score = {}
        self._lock_seated_players = threading.Lock()
        self._lock_all_players = threading.Lock()

        self.__lookon_players = []

        self.__closets = []
        self.__closet_limts = 10

    def is_player_in(self, player):
        return player in self._seated_players

    def get_seated_player_count(self):
        return len(self._seated_players)

    def get_room_id(self):
        return self._room_id

    def get_scene_players(self):
        return self._seated_players

    def get_last_winners(self):
        return self._last_winners

    def get_player_total_score(self, player):
        if player in self._players_total_score:
            return self._players_total_score[player]
        else:
            return 0

    def get_closet_by_id(self, closetid):
        sid = str(closetid)
        for c in self.__closets:
            if str(c.get_closetId()) == sid:
                return c

        return None

    def get_all_players(self):
        return self.__lookon_players + self.get_scene_players()

    def can_new_player_seated(self):
        return len(self._seated_players) < self._max_seated_players

    def can_new_player_enter(self):
        return len(self._all_players) < self._max_players_number

    def create_closet(self, gRule):
        closet = Closet(gRule, len(self.__closets) + 1)
        self.__closets.append(closet)


    def add_seated_player(self, player, seatid):
        try:
            if self._lock_seated_players.acquire(5):
                if self.can_new_player_seated():
                    self._seated_players.append(player)
                    player.set_my_room(self)
                    player.set_seatid(seatid)
                    return True, Errors.ok
                else:
                    return False, Errors.room_no_empty_seat
        except Exception as ex:
            Log.exception(ex)
            return False, Errors.unknown_error
        finally:
            self._lock_seated_players.release()

    def remove_player_from_seat(self, player):
        try:
            if self._lock_seated_players.acquire(5):
                if player in self._seated_players:
                    self._seated_players.remove(player)
                    return True, Errors.ok
                else:
                    return False, Errors.player_not_in_game

        except Exception as ex:
            Log.exception(ex)
            return False, Errors.unknown_error
        finally:
            self._lock_seated_players.release()

    def remove_player(self, player):
        if player in self._seated_players:
            self._seated_players.remove(player)
        if player in self._all_players:
            self._all_players.remove(player)

    def add_new_enter_player(self, player):
        try:
            if self._lock_all_players.acquire(5):
                if self.can_new_player_enter():
                    self._all_players.append(player)
                    # player.set_closet(self)
                    return True, Errors.ok
                else:
                    return False, Errors.room_is_full
        except Exception as ex:
            Log.exception(ex)
            return False, Errors.unknown_error
        finally:
            self._lock_all_players.release()

    def remove_player_from_room(self, player):
        try:
            if self._lock_all_players.acquire(5):
                if player in self._all_players:
                    self._all_players.remove(player)
                    player.set_closet(None)
                    return True, Errors.ok
                else:
                    return False, Errors.player_not_in_room
        except Exception as ex:
            Log.exception(ex)
            return False, Errors.unknown_error
        finally:
            self._lock_all_players.release()

    def set_last_winners(self, winners):
        self._last_winners = winners

    def process_player_request(self, player, cmd, req_json):
        req_cmd = cmd.lower()
        if req_cmd == InterProtocol.client_req_cmd_enter_room:
            self.process_player_enter_room(player)
        elif req_cmd == InterProtocol.client_req_cmd_new_closet:
            self.process_player_create_closet(player, req_json)
        elif req_cmd == InterProtocol.client_req_cmd_leave_room:
            self.process_player_leave_room(player)
        elif req_cmd == InterProtocol.client_req_cmd_join_game:
            seatid = req_json[InterProtocol.seat_id]
            closetid = req_json[InterProtocol.field_closetid]
            self.process_join_game(player, closetid, seatid)
        elif req_cmd == InterProtocol.client_req_cmd_leave_game:
            self.process_player_leave_game(player)
        elif req_cmd == InterProtocol.client_req_type_exe_cmd:
            if InterProtocol.client_req_exe_cmd not in req_json:
                err = InterProtocol.create_request_error_packet(req_cmd)
                player.send_server_cmd_packet(err)
            elif self._current_round:
                cmd = req_json[InterProtocol.client_req_exe_cmd]
                const_param = InterProtocol.client_req_cmd_param
                cmd_param = req_json[const_param] if const_param in req_json else None
                self._current_round.process_player_execute_command(player, cmd, cmd_param)
        elif req_cmd == InterProtocol.client_req_play_cards:
            if InterProtocol.cmd_data_cards not in req_json:
                err = InterProtocol.create_request_error_packet(req_cmd)
                player.send_server_cmd_packet(err)
            else:
                cards = req_json[InterProtocol.cmd_data_cards]
                self._current_round.process_player_execute_command(player, InterProtocol.client_req_play_cards, cards)

        elif req_cmd == InterProtocol.client_req_robot_play:
            flag = str(req_json[InterProtocol.client_req_robot_play])
            if flag.lower().startswith('y'):
                self._current_round.process_player_robot_play_request(player, True)
            elif flag.lower().startswith('n'):
                self._current_round.process_player_robot_play_request(player, False)
            else:
                err = InterProtocol.create_request_error_packet(req_cmd)
                player.send_server_cmd_packet(err)

    def process_player_leave_game(self, player):
        cmd = InterProtocol.client_req_cmd_leave_game
        resp_pack = None
        if player in self._seated_players:
            self.remove_player_from_seat(player)
            resp_pack = InterProtocol.create_success_resp_pack(cmd)
        else:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_not_in_game)

        player.send_server_cmd_packet(resp_pack)


    def process_player_leave_room(self, player):
        cmd = InterProtocol.client_req_cmd_leave_room
        resp_pack = None
        if player in self._all_players:
            self.remove_player_from_room(player)
            player.set_my_room(None)
            resp_pack = InterProtocol.create_success_resp_pack(cmd)
        else:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_not_in_room)

        player.send_server_cmd_packet(resp_pack)

    def process_player_enter_room(self, player):
        cmd = InterProtocol.client_req_cmd_enter_room
        if player in self._all_players:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_already_in_room)
            player.send_server_cmd_packet(resp_pack)
        elif not self.can_new_player_enter():
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.room_is_full)
            player.send_server_cmd_packet(resp_pack)
        else:
            ret, err = self.add_new_enter_player(player)
            resp_pack = None
            if ret:
                roomObj = {
                    InterProtocol.room_id : self._room_id,
                    InterProtocol.resp_players: self.get_players_status(),
                    InterProtocol.field_closets: self.get_closets_status()
                }
                resp_pack = InterProtocol.create_success_resp_data_pack(cmd, InterProtocol.resp_room, roomObj)
            else:
                resp_pack = InterProtocol.create_error_pack(cmd, err)
            player.send_server_cmd_packet(resp_pack)
            self.publish_players_status()

    def process_player_create_closet(self, player, req_json):
        pass

    def process_join_game(self, player, closetid, seatid):
        cmd = InterProtocol.client_req_cmd_join_game
        closet = self.get_closet_by_id(closetid)
        if not closet:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.invalid_closetid)
            player.send_server_cmd_packet(resp_pack)

        if not closet.is_seatid_valid(seatid):
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.invalid_seat_id)
            player.send_server_cmd_packet(resp_pack)
        elif player not in self._all_players:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_not_in_room)
            player.send_server_cmd_packet(resp_pack)
        elif player in self._seated_players:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_already_in_game)
            player.send_server_cmd_packet(resp_pack)
        elif self.is_seatid_has_been_occupied(seatid):
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.seat_id_occupied)
            player.send_server_cmd_packet(resp_pack)
        else:
            ret, errCode = self.add_seated_player(player, seatid)
            if not ret:
                resp_pack = InterProtocol.create_error_pack(cmd, errCode)
                player.send_server_cmd_packet(resp_pack)

            else:
                resp_pack = InterProtocol.create_success_resp_pack(cmd)
                player.send_server_cmd_packet(resp_pack)

                self.publish_players_status()

                if self.get_seated_player_count() >= self._min_seated_players:
                    self.test_continue_next_round()

    def is_seatid_has_been_occupied(self, seatid):
        if seatid < 1:
            return False

        for p in self._all_players:
            if p.get_seat_id() == seatid:
                return True

        return False

    def is_seatid_valid(self, seatid):
        seatids = self._game_rule.get_seats_ids()
        if seatids is None or len(seatids) < 2: #at least two players
            return True

        return seatid in self._game_rule.get_seats_ids()

    def get_players_status(self):
        players = []
        for p in self._all_players:
            info = {
                InterProtocol.user_id: p.get_userid(),
            }
            players.append(info)

        return players

    def get_closets_status(self):
        infos = []
        for c in self.__closets:
            info = {
                InterProtocol.field_gameid: c.get_rule().get_ruleid(),
                InterProtocol.field_closetid: c.get_closetId(),
                InterProtocol.field_players: c.get_players_status()
            }
            infos.append(info)
        return infos

    def publish_players_status(self):
        players = self.get_players_status()

        pack = InterProtocol.create_game_players_packet(players)
        for p in self._all_players:
            p.send_server_cmd_packet(pack)

    def test_continue_next_round(self):
        if self._current_round_order < self._round_num:
            self.begin_next_game_round()
        else:
            self.close_room()

    def update_player_total_score(self, player):
        if player not in self._players_total_score:
            self._players_total_score[player] = player.get_won_score()
        else:
            self._players_total_score[player] += player.get_won_score()


    def begin_next_game_round(self):
        pass

    def close_room(self):
        packet = InterProtocol.create_game_status_packet("Room will be closed")
        if self._current_round:
            self._current_round.publish_round_states(packet)

    def set_max_seated_player_num(self, max_number):
        self._max_seated_players = max_number

    def set_min_seated_player_num(self, min_number):
        self._min_seated_players = min_number

    def set_max_player_number(self, max_number):
        self._max_players_number = max_number

    def set_round_number(self, number):
        self._round_num = number

    def set_fee_stuff(self, stuffid, stuffname):
        self._fee_stuff_id = stuffid
        self._fee_stuff_name = stuffname

    def set_stake_stuff(self, stuffid, stuffname):
        self._stake_stuff_id = stuffid
        self._stake_stuff_name = stuffname

    #################new design


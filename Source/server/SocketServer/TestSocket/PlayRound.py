import random

import Utils


class PlayRound:
    def __init__(self, play_rule):
        self.__play_rule = play_rule
        self.__players = []
        self.__started = False
        self.__cur_call_player_idx = -1
        self.__cur_call_action_id = ""
        self.__cur_stage = play_rule.get_next_game_stage()
        for s in self.__play_rule.get_game_stages():
            s.set_my_round(self)

    def get_players(self):
        return self.__players

    def get_players_count(self):
        return len(self.__players)

    def add_player(self, player):
        self.__players.append(player)
        player.set_game_round(self)
        # if len(self.__players) >= self.__play_rule.get_player_min_number():
        #     self.begin_game()
        # self.test_and_update_current_stage()

    def test_and_update_current_stage(self):
        if self.__cur_stage and self.__cur_stage.is_completed():
            self.__cur_stage = self.__play_rule.get_next_game_stage()
            self.__cur_stage.begin()

    def begin_game(self):
        self.__started = True
        self.deal_cards()

    def deal_cards(self):
        cards = self.__play_rule.get_cards()
        cards_b = cards[:]  # copy this list
        remain_cards = random.sample(cards_b, self.__play_rule.get_cards_number_not_deal())
        Utils.list_remove_parts(cards_b, remain_cards)
        player_num = len(self.__players)
        for p in self.__players:
            p.begin_new_deal()
        while len(cards_b) > 0:
            cards_one_deal = random.sample(cards_b, player_num)
            for j in range(player_num):
                self.__players[j].deal_one_card(cards_one_deal[j])
            Utils.list_remove_parts(cards_b, cards_one_deal)
        for p in self.__players:
            p.finish_new_deal()

    def process_player_cards_sorted(self):
        all_arranged = True
        for p in self.__players:
            if not p.is_cards_sorted():
                all_arranged = False
                break
        if all_arranged:
            self.begin_players_call_process()

    def get_players_call_turns(self):
        return self.__players

    def begin_players_call_process(self):
        # players_in_turn = self.get_players_call_turns()
        # player = self.get_next_call_player()
        # if player:
        #    call_commands = self.get_next_call_actions()
        #    player.send_call_command_options(call_commands)
        self.make_next_player_select_action(None)

    def make_next_player_select_action(self, prev_action_id):
        player = self.get_next_call_player()
        call_acts_group = self.get_next_call_action_group(prev_action_id)
        if player and call_acts_group:
            player.send_call_command_options(call_acts_group)

    def get_rule(self):
        return self.__play_rule

    def can_new_player_in(self):
        return not self.__started and len(self.__players) < self.__play_rule.get_player_max_number()

    def get_next_call_player(self):
        self.__cur_call_player_idx += 1
        if self.__cur_call_player_idx >= len(self.__players):
            self.__cur_call_player_idx = 0
        if self.__cur_call_player_idx < len(self.__players):
            return self.__players[self.__cur_call_player_idx]
        else:
            return None

    def get_next_call_action_group(self, action_id):
        return self.__play_rule.get_follow_up_action_group(action_id)
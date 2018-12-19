from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
from constants import *
import pickle
import random

class RL(BasePokerPlayer):
    def __init__(self):
        self.q_vals = self.load_obj('data')
        self.street = None
        self.pot = 0
        self.stack = None
        self.last_action = None
        self.last_opp_action = None
        self.position = None
        self.q_keys = []

    def declare_action(self, valid_actions, hole_card, round_state):
        self.stack = [seat for seat in round_state['seats'] if seat['uuid'] == self.uuid][0]['stack']
        hand_ranking = self.gen_hand_ranking(hole_card, round_state['community_card'])

        key = (hand_ranking, self.get_street(), self.last_opp_action, self.position)
        self.q_keys.append(key)

        e = random.random()
        call_amount = valid_actions[1]['amount']

        val = self.q_vals[key]
        f, c, r = float(val[0]), float(val[1]), float(val[2])
        total = sum([f, c, r])
        f, c, r = f/total, c/total, r/total

        if e <= c:
            action = 'call'
            amount = call_amount
        elif e <= c + r:
            if call_amount >= self.stack:
                action = 'call'
                amount = call_amount
            else:
                action = 'raise'
                pot_after_call = self.pot + call_amount
                amount = min(int(round(pot_after_call*0.67)), valid_actions[2]['amount']['max'])
        else:
            action = 'fold'
            amount = 0

        self.last_action = action

        return action, amount

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.q_keys = []

    def receive_street_start_message(self, street, round_state):
        self.street = street
        if round_state['dealer_btn'] == 0:
            self.position = DEALER
        else:
            self.position = SB
        self.last_opp_action = NONE
        self.last_action = None

    def receive_game_update_message(self, action, round_state):
        self.pot = round_state['pot']['main']['amount']
        if action['player_uuid'] != self.uuid:
            if action['action'] == 'call':
                self.last_opp_action = CALL
            elif action['action'] == 'raise':
                self.last_opp_action = RAISE

    def receive_round_result_message(self, winners, hand_info, round_state):
        amount = round_state['pot']['main']['amount']/2
        won = True
        if winners[0]['uuid'] != self.uuid:
            won = False

        self.update_q_vals(won, amount)
        self.save_obj(self.q_vals, 'data')

    def gen_hand_ranking(self, hole_card, community_card):
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=100,
                nb_player=2,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if win_rate <= 0.45:
            return BAD
        elif win_rate <= 0.6:
            return OK
        elif win_rate <= 0.75:
            return GOOD
        else:
            return GREAT

    def get_street(self):
        if self.street == 'preflop':
            return PREFLOP
        elif self.street == 'flop':
            return FLOP
        elif self.street == 'turn':
            return TURN
        else:
            return RIVER

    def update_q_vals(self, won, amount):
        if self.last_action == 'fold':
            fold_delta = 2*amount
            call_delta = -amount
            raise_delta = -amount
        elif self.last_action == 'call':
            if won:
                fold_delta = -amount
                call_delta = amount
                raise_delta = 2*amount
            else:
                fold_delta = 2*amount
                call_delta = -amount
                raise_delta = -2*amount
        elif self.last_action == 'raise':
            if won:
                fold_delta = -amount
                call_delta = -amount
                raise_delta = 2*amount
            else:
                fold_delta = 2*amount
                call_delta = amount
                raise_delta = -amount
        else:
            return

        for key in self.q_keys:
            if key not in self.q_vals:
                self.q_vals[key] = (0, 0, 0)
            new_vals = (self.q_vals[key][0] + fold_delta, self.q_vals[key][1] + call_delta, self.q_vals[key][2] + raise_delta)
            if new_vals[0] < 0:
                new_vals = (0, new_vals[1], new_vals[2])
            if new_vals[1] < 0:
                new_vals = (new_vals[0], 0, new_vals[2])
            if new_vals[2] < 0:
                new_vals = (new_vals[0], new_vals[1], 0)

            self.q_vals[key] = new_vals

    def init_q_vals(self):
        self.q_vals = {}
        for h in range(4):
            for s in range(4):
                for l in range(3):
                    for p in range(2):
                        key = (h, s, l, p)
                        i = random.randint(1, 80000)
                        j = random.randint(1, 80000)
                        self.q_vals[key] = (0, i, j)

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)

def setup_ai():
	return RL()
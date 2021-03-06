from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

class MonteCarlo(BasePokerPlayer):
    def __init__(self):
        self.curr_pot = 0
        self.stack = None
    
    def declare_action(self, valid_actions, hole_card, round_state):
        self.stack = [seat for seat in round_state['seats'] if seat['uuid'] == self.uuid][0]['stack']
        call_amount = valid_actions[1]['amount']
        curr_pot = self.curr_pot
        pot_after_call = curr_pot + call_amount
        pot_odds = float(call_amount)/float(curr_pot)

        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=100,
                nb_player=2,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )

        action = None
        amount = None

        if win_rate >= 0.51:
            # if all in to call
            if call_amount >= self.stack:
                action = 'call'
                amount = call_amount
            elif win_rate >= 0.8:
                action = 'raise'
                amount = valid_actions[2]['amount']['max']
            else:
                action = 'raise'
                amount = min(int(round(pot_after_call*0.67)), valid_actions[2]['amount']['max'])
        elif win_rate >= pot_odds:
            action = 'call'
            amount = call_amount
        else:
            action = 'fold'
            amount = 0

        return action, amount

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        self.curr_pot = round_state['pot']['main']['amount']

    def receive_game_update_message(self, action, round_state):
        self.curr_pot = round_state['pot']['main']['amount']

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass
            
def setup_ai():
    return MonteCarlo()

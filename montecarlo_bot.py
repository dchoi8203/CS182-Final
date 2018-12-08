from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

class montecarlo_bot(BasePokerPlayer):
	def __init__(self):
		super().__init__()
		self.wins = 0
		self.losses = 0

	def declare_action(self, valid_actions, hole_card, round_state):
		win_rate = estimate_hole_card_win_rate(
                nb_simulation=500,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
		if win_rate > 0.5:
			


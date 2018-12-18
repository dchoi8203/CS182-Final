from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine.card import Card
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate, _pick_unused_card, _fill_community_card, evaluate_hand, _montecarlo_simulation


hole_cards = ['DA', 'CK']
hc = gen_cards(hole_cards)
print(hole_cards)

community_cards = ['D4', 'DQ', 'SA', 'HA', 'H2']

win_rate = estimate_hole_card_win_rate(
                nb_simulation=100,
                nb_player=2,
                hole_card=hc,
                community_card=gen_cards(community_cards)
                )

print(win_rate)

# total = 0
# r = 1000
# for i in range(r):
# 	e = evaluate_hand(hc, _fill_community_card([], hc))
# 	total += e['strength']
# print(total/r)

# print(evaluate_hand(hc, gen_cards(['SA', 'H4', 'SK', 'S2', 'H3'])))

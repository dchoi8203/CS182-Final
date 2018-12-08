from pypokerengine.api.game import setup_config, start_poker

from AlwaysCall import AlwaysCall
from FoldIfWinning import FoldIfWinning
import numpy as np

stack_log = []
for r in range(10):
	p1, p2 = AlwaysCall(), FoldIfWinning()

	config = setup_config(max_round=5, initial_stack=200, small_blind_amount=1)
	config.register_player(name="cb", algorithm=p1)
	config.register_player(name="fb", algorithm=p2)
	game_result = start_poker(config, verbose=0)

	stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])

print('Avg stack: {}'.format(int(np.mean(stack_log))))
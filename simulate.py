from pypokerengine.api.game import setup_config, start_poker

from AlwaysCall import AlwaysCall
# from CallIfWinning import CallIfWinning
from MonteCarlo import MonteCarlo
import numpy as np

stack_log = []
for r in range(1):
	p1, p2 = MonteCarlo(), AlwaysCall()

	config = setup_config(max_round=1, initial_stack=200, small_blind_amount=1)
	config.register_player(name='player_1', algorithm=p1)
	config.register_player(name='player_2', algorithm=p2)
	game_result = start_poker(config, verbose=1)

	stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])

print('Avg stack: {}'.format(int(np.mean(stack_log))))
print('Number of hands played: {}'.format(len(stack_log)))
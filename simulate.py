from pypokerengine.api.game import setup_config, start_poker

from AlwaysCall import AlwaysCall
from AlwaysAllIn import AlwaysAllIn
from MonteCarlo import MonteCarlo
from CallIfWinning import CallIfWinning
from RL import RL
import numpy as np

play1, play2, play3, play4, play5, play6 = False, False, False, True, False, False

if play1:
	print('RL vs AlwaysAllIn')
	stack_log = []
	for r in range(1000):
		print(r)
		p1, p2 = RL(), AlwaysAllIn()

		config = setup_config(max_round=1, initial_stack=200, small_blind_amount=1)
		config.register_player(name='player_1', algorithm=p1)
		config.register_player(name='player_2', algorithm=p2)
		game_result = start_poker(config, verbose=0)

		stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])
		

	print('Avg stack: {}'.format(int(np.mean(stack_log))))
	print('Number of games played: {}'.format(len(stack_log)))

if play2:
	print('RL vs AlwaysCall')
	stack_log2 = []
	for r in range(1):
		print(r)
		p1, p2 = RL(), AlwaysCall()

		config = setup_config(max_round=1, initial_stack=200, small_blind_amount=1)
		config.register_player(name='player_1', algorithm=p1)
		config.register_player(name='player_2', algorithm=p2)
		game_result = start_poker(config, verbose=0)

		stack_log2.append([player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])
		

	print('Avg stack: {}'.format(int(np.mean(stack_log2))))
	print('Number of games played: {}'.format(len(stack_log2)))

if play3:
	print('RL vs CallIfWinning')
	stack_log3 = []
	for r in range(1):
		print(r)
		p1, p2 = RL(), CallIfWinning()

		config = setup_config(max_round=5, initial_stack=200, small_blind_amount=1)
		config.register_player(name='player_1', algorithm=p1)
		config.register_player(name='player_2', algorithm=p2)
		game_result = start_poker(config, verbose=0)

		stack_log3.append([player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])

	print('Avg stack: {}'.format(int(np.mean(stack_log3))))
	print('Number of games played: {}'.format(len(stack_log3)))

if play4:
	print('RL vs MonteCarlo')
	stack_log = []
	for r in range(50):
		print(r)
		p1, p2 = RL(), MonteCarlo()

		config = setup_config(max_round=20, initial_stack=200, small_blind_amount=1)
		config.register_player(name='player_1', algorithm=p1)
		config.register_player(name='player_2', algorithm=p2)
		game_result = start_poker(config, verbose=0)

		stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])
		

	print('Avg stack: {}'.format(int(np.mean(stack_log))))
	print('Number of games played: {}'.format(len(stack_log)))

if play5:
	print('MonteCarlo vs AlwaysCall')
	stack_log = []
	for r in range(50):
		print(r)
		p1, p2 = MonteCarlo(), AlwaysCall()

		config = setup_config(max_round=20, initial_stack=200, small_blind_amount=1)
		config.register_player(name='player_1', algorithm=p1)
		config.register_player(name='player_2', algorithm=p2)
		game_result = start_poker(config, verbose=0)

		stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])
		

	print('Avg stack: {}'.format(int(np.mean(stack_log))))
	print('Number of games played: {}'.format(len(stack_log)))

if play6:
	print('MonteCarlo vs AlwaysAllIn')
	stack_log = []
	for r in range(1000):
		print(r)
		p1, p2 = MonteCarlo(), AlwaysAllIn()

		config = setup_config(max_round=1, initial_stack=200, small_blind_amount=1)
		config.register_player(name='player_1', algorithm=p1)
		config.register_player(name='player_2', algorithm=p2)
		game_result = start_poker(config, verbose=0)

		stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])
		

	print('Avg stack: {}'.format(int(np.mean(stack_log))))
	print('Number of games played: {}'.format(len(stack_log)))
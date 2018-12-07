from pypokerengine.api.game import setup_config, start_poker
from CallBot import CallBot
from FoldBot import FoldBot

config = setup_config(max_round=10, initial_stack=200, small_blind_amount=1)
config.register_player(name="p1", algorithm=CallBot())
config.register_player(name="p2", algorithm=FoldBot())
game_result = start_poker(config, verbose=1)
print game_result
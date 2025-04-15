# PARAMETERS TO CONTROL THE BEHAVIOR OF THE GAME ENGINE
# DO NOT REMOVE OR RENAME THIS FILE
PLAYER_1_NAME = 'A'
PLAYER_1_PATH = './openaibot'
# NO TRAILING SLASHES ARE ALLOWED IN PATHS
PLAYER_2_NAME = 'B'
PLAYER_2_PATH = './player1_ABC'
# ./player2_monte_carlo
# ./player3_strong
# ./player4_weak
# GAME PROGRESS IS RECORDED HERE
GAME_LOG_FILENAME = 'gamelog'
# PLAYER_LOG_SIZE_LIMIT IS IN BYTES
PLAYER_LOG_SIZE_LIMIT = 52428800
# STARTING_GAME_CLOCK AND TIMEOUTS ARE IN SECONDS
ENFORCE_GAME_CLOCK = False
STARTING_GAME_CLOCK = 500000.
BUILD_TIMEOUT = 30.
CONNECT_TIMEOUT = 30.
# THE GAME VARIANT FIXES THE PARAMETERS BELOW
# CHANGE ONLY FOR TRAINING OR EXPERIMENTATION
NUM_ROUNDS = 20
STARTING_STACK = 400
BIG_BLIND = 2
SMALL_BLIND = 1
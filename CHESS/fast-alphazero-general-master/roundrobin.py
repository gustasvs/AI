import pyximport; pyximport.install()

from pathlib import Path
import pprint
from glob import glob
from utils import *
from NNetWrapper import NNetWrapper as nn
from connect4.Connect4Game import Connect4Game as Game
from GenericPlayers import *
from MCTS import MCTS
from Arena import Arena
import numpy as np
import choix

args = dotdict({
    'arenaCompare': 50,
    'arenaTemp': 0,
    'temp': 1,
    'tempThreshold': 10,
    # use zero if no montecarlo
    'numMCTSSims': 50,
    'cpuct': 4,
    'playRandom': False,
})

if __name__ == '__main__':
    print('Args:')
    pprint.pprint(args)
    if not Path('roundrobin').exists():
        Path('roundrobin').mkdir()
    print('Beginning round robin')
    networks = sorted(glob('roundrobin/*'),reverse=True)
    model_count = len(networks) + int(args.playRandom)

    if model_count <= 2:
        print(
            "Too few models for round robin. Please add models to the roundrobin/ directory")
        exit()

    total_games = 0
    for i in range(model_count):
        total_games += i
    total_games *= args.arenaCompare
    print(
        f'Comparing {model_count} different models in {total_games} total games')
    win_matrix = np.zeros((model_count, model_count))

    g = Game(6)
    nnet1 = nn(g)
    nnet2 = nn(g)

    for i in range(model_count - 1):
        for j in range(i+1, model_count):
            file1 = Path(networks[i])
            file2 = Path('random' if args.playRandom and j ==
                         model_count - 1 else networks[j])
            print(f'{file1.stem} vs {file2.stem}')
            nnet1.load_checkpoint(folder='roundrobin', filename=file1.name)
            if args.numMCTSSims <= 0:
                p1 = NNPlayer(g, nnet1, args.arenaTemp,
                              args.tempThreshold).play
            else:
                mcts1 = MCTS(g, nnet1, args)

                def p1(x, turn):
                    if turn <= 2:
                        mcts1.reset()
                    temp = args.temp if turn <= args.tempThreshold else args.arenaTemp
                    policy = mcts1.getActionProb(x, temp=temp)
                    return np.random.choice(len(policy), p=policy)
            if file2.name != 'random':
                nnet2.load_checkpoint(folder='roundrobin', filename=file2.name)
                if args.numMCTSSims <= 0:
                    p2 = NNPlayer(g, nnet1, args.arenaTemp,
                                  args.tempThreshold).play
                else:
                    mcts2 = MCTS(g, nnet2, args)

                    def p2(x, turn):
                        if turn <= 2:
                            mcts2.reset()
                        temp = args.temp if turn <= args.tempThreshold else args.arenaTemp
                        policy = mcts2.getActionProb(x, temp=temp)
                        return np.random.choice(len(policy), p=policy)
            else:
                p2 = RandomPlayer(g).play
            arena = Arena(p1, p2, g)
            p1wins, p2wins, draws = arena.playGames(args.arenaCompare)
            win_matrix[i, j] = p1wins + 0.5*draws
            win_matrix[j, i] = p2wins + 0.5*draws
            print(f'wins: {p1wins}, ties: {draws}, losses:{p2wins}\n')

    print("\nWin Matrix(row beat column):")
    print(win_matrix)
    try:
        with np.errstate(divide='ignore', invalid='ignore'):
            params = choix.ilsr_pairwise_dense(win_matrix)
        print("\nRankings:")
        for i, player in enumerate(np.argsort(params)[::-1]):
            name = 'random' if args.playRandom and player == model_count - \
                1 else Path(networks[player]).stem
            print(f"{i+1}. {name} with {params[player]:0.2f} rating")
        print(
            "\n(Rating Diff, Winrate) -> (0.5, 62%), (1, 73%), (2, 88%), (3, 95%), (5, 99%)")
    except Exception:
        print("\nNot Enough data to calculate rankings")

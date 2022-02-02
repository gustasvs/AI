class HumanTicTacToePlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board, turn):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print(int(i/self.game.n), int(i % self.game.n))
        while True:
            # Python 3.x
            a = input()
            # Python 2.x
            # a = raw_input()

            x, y = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x != -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a

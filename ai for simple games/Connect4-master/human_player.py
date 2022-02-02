class HumanPlayer:

    def __init__(self, tag, exploration_factor=1):
        self.print_value = False
        self.exp_factor = exploration_factor
        self.tag = tag

    @staticmethod
    def choose_move(state, winner, learn):
        print(state)
        return int(input('Choose move number: ')) - 1

    def save_memory(self):
        pass
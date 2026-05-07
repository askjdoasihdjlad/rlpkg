# GAME BASE CLASS
class Game:
    def legal_steps(self, state):
        """Steps that can be made in given state."""
        raise NotImplementedError()

    def take_step(self, step, state):
        """Result of taking step in given state."""
        raise NotImplementedError

    def goodness(self, state, player):
        """Goodness measure of the state."""
        raise NotImplementedError()

    def is_leaf(self, state):
        """Is the node a terminal node."""
        return not self.legal_steps(state)

    def next_player(self, state):
        """Return next player."""
        raise NotImplementedError()

    def print(self, state):
        """Print current state."""
        print(state)

    def next_state(self, state):
        """Return next (step, state) list."""
        return [(step, self.take_step(step, state))
                for step in self.legal_steps(state)]

    def __repr__(self):
        """Print the name of the game."""
        return '<%s>' % self.__class__.__name__

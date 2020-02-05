class Cell:
    SIZE = 12
    ALIVE = 1
    DEAD = 0

    def __init__(self, state, rect):
        if state is not self.ALIVE and state is not self.DEAD:
            raise Exception("Cell state is excepting a boolean. Given value is: {}".format(state))
        self.state = state
        self.rect = rect
        self.next_state = None

    def swap_state(self):
        if self.state is self.ALIVE:
            self.state = self.DEAD
        else:
            self.state = self.ALIVE

    def save_next_state(self, next_state):
        if next_state is not self.ALIVE and next_state is not self.DEAD:
            raise Exception("Cell state is excepting a boolean. Given value is: {}".format(next_state))
        self.next_state = next_state

    def apply_next_state(self):
        if self.next_state is not None:
            self.state = self.next_state
            self.next_state = None

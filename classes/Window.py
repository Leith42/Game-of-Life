class Window:
    def __init__(self, config):
        self.width = config.getint('WINDOW', 'Width')
        self.height = config.getint('WINDOW', 'Height')

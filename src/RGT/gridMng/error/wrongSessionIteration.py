class WrongSessionIteration(Exception):
    def __init__(self, msg):
        Exception.__init__(self, 'Session does not contain that iteration')
        
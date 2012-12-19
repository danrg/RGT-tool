class WrongNodeType(Exception):
    '''
    Used when a function is expecting a node of a certain type but encounters a node of an
    unexpected type
    '''


    def __init__(self, msg):
        Exception.__init__(self, msg)
        
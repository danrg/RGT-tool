class ResultAlternativeConcernTableData(object):
    concerns = None # data used to generate the concern result table. format: [('leftConcern', 'righConcern', nPairCited, nLeftConCited, nRightConCited, isPairNew), ....]
    alternatives = None # date used to generate the alternative result table. format: [('alternativeName', ntimesCited, isNew), ...]

    def __init__(self):
        pass

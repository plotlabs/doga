class RelatedContentNotFound(Exception):
    def __init__(self, *args):
        super(RelatedContentNotFound, self).__init__(*args)
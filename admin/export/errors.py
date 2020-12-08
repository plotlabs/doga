class RDSCreationError(Exception):
    def __init__(self, *args):
        super(RDSCreationError, self).__init__(*args)


class EC2CreationError(Exception):
    def __init__(self, *args):
        super(EC2CreationError, self).__init__(*args)


class DogaEC2toRDSconnectionError(Exception):
    def __init__(self, *args):
        super(DogaEC2toRDSconnectionError, self).__init__(*args)


class DogaDirectoryCreationError(Exception):
    def __init__(self, *args):
        super(DogaDirectoryCreationError, self).__init__(*args)


class DogaHerokuDeploymentError(Exception):
    def __init__(self, *args):
        super(DogaHerokuDeploymentError, self).__init__(*args)

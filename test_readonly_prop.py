class Article(object):
    def __init__(self, name, available):
        self._name = name
        self.available = available

    @property
    def name(self):
        return self._name
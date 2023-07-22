class PageResult:
    def __init__(self, data, page=1, number=20):
        self.__dict__ = dict(zip(['data', 'page', 'number'], [data, page, number]))
        self.full_listing = [self.data[i:i + number] for i in range(0, len(self.data), number)]

    def __iter__(self):
        if not self.full_listing:
            return ''
        for i in self.full_listing[self.page - 1]:
            yield i

    def __repr__(self):
        return "/web/logs/{}".format(self.page + 1)

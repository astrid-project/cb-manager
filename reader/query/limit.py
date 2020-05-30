def _limit(self, query):
    limit = query.get('limit', {})
    start = limit.get('from', None)
    end = limit.get('to', None)
    if end is None:
        if start is not None: self.s = self.s[start:]
    else:
        self.s = self.s[start:(end + 1)]

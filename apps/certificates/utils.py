class AttrDict(dict):
    """
    Dict-like object that exposes its keys as attributes.

    Examples
    --------
    >>> d = AttrDict({'a': 1, 'b': 2})
    >>> d.a
    1
    >>> d = AttrDict({'a': 1, 'b': {'c': 3, 'd': 4}})
    >>> d.b.c
    3
    """

    def __getattr__(self, attr):
        value = self[attr]
        if isinstance(value, dict):
            return AttrDict(value)
        return value

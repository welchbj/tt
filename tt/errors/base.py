"""The base tt exception type."""


class TtError(Exception):

    """Base exception type for tt errors.

    .. note::

        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """

    def __init__(self, message, *args):
        self._message = message
        super(TtError, self).__init__(self._message, *args)

    @property
    def message(self):
        """A helpful message intended to be shown to the end user.

        :type: :class:`str <python:str>`

        """
        return self._message

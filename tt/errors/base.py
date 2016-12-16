"""The base tt exception type."""


class TtError(Exception):

    """Base exception type for tt errors.

    Attributes:
        message (str): An additional helpful message that could be displayed
            to the user to better explain the error.

    Notes:
        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """

    def __init__(self, message, *args):
        self.message = message
        super(TtError, self).__init__(self.message, *args)

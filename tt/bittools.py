"""A module for simple manipulation of bits.
"""


def get_int_concatenation(int1, int2, int_size):
    """Get the concatenation of two ints.

    Args:
        int1 (int): The int that will be the leading bit sequence in the
            result.
        int2 (int): The int that will be the trailing bit sequence in the
            result.
        int_size (int): The length (as number of bits) of ``int1`` and
            ``int2``.

    Returns:
        int: The concatention of ``int1`` and ``int2``, treated as integers
            with bit length of ``int_size``.

    Examples:
    >>> x = get_int_concatentation(1, 2, 2)
    >>>bin(x)
    '0b110'
    >>> x = get_int_concatentation(1, 2, 3)
    >>>bin(x)
    '0b1010'

    """
    return (int1 << int2.bit_length) | int2


def get_parity(x):
    """Get the bit parity of ``x``.

    Note:
        Not currently used, but this may be useful in the future.

    """
    c = 0
    while x:
        c += 1
        x &= x - 1
    return c


def get_nth_gray_code(n):
    """Get the nth gray code.

    Args:
        n (int): The n in nth gray code.

    Returns:
        int: The nth gray code.

    """
    return n ^ (n >> 1)


def get_bit_string(n, num_chars=None):
    """Convert ``n`` to a binary string representation.

    Args:
        n (int):
        num_chars (int): The total number of chars the result should include.
            The result is zero-filled to reach this number if necessary.

    Returns:
        str: The binary representation of ``n``.

    """
    fmt_str = '{:0' + (str(num_chars) if num_chars is not None else '') + 'b}'
    return fmt_str.format(n)

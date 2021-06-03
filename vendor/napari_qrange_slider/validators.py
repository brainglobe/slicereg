# Taken from https://github.com/napari/napari/blob/102a7e8f845893c874d2b86f9371d41130100b89/napari/utils/validators.py

from collections.abc import Collection, Generator


def validate_n_seq(n: int, dtype=None):
    """Creates a function to validate a sequence of len == N and type == dtype.

    Currently does **not** validate generators (will always validate true).

    Parameters
    ----------
    n : int
        Desired length of the sequence
    dtype : type, optional
        If provided each item in the sequence must match dtype, by default None

    Returns
    -------
    function
        Function that can be called on an object to validate that is a sequence
        of len `n` and (optionally) each item in the sequence has type `dtype`

    Examples
    --------
    >>> validate = validate_n_seq(2)
    >>> validate([4, 5])  # just fine, thank you very much
    """

    def func(obj):
        """Function that validates whether an object is a sequence of len `n`.

        Parameters
        ----------
        obj : any
            the object to be validated

        Raises
        ------
        TypeError
            If the object is not an indexable collection.
        ValueError
            If the object does not have length `n`
        TypeError
            If `dtype` was provided to the wrapper function and all items in
            the sequence are not of type `dtype`.
        """

        if isinstance(obj, Generator):
            return
        if not (isinstance(obj, Collection) and hasattr(obj, '__getitem__')):
            raise TypeError(
                f"object '{obj}' is not an indexable collection "
                f"(list, tuple, or np.array), of length {n}"
            )
        if not len(obj) == n:
            raise ValueError(f"object must have length {n}, got {len(obj)}")
        if dtype is not None:
            for item in obj:
                if not isinstance(item, dtype):
                    raise TypeError(
                        f"Every item in the sequence must be of type {dtype}, "
                        f"but {item} is of type {type(item)}"
                    )

    return func

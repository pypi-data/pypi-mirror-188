"""
**puissant**  provides a collection of functions for command-line validated user input.
The following conveninence user-input functions are available:

- :func:`puissant.menu` to choose single string options from a menu.
- :func:`puissant.yes_no` for yes/no questions input.
- :func:`puissant.tickbox_menu` for multiple choices from a menu
- :func:`puissant.ranged_int` for ranged integer input.
- :func:`puissant.ranged_float` for ranged floating point input.
- :func:`puissant.enum_str` for user input chosen from a string out of a list.

All of the above functions are wrappers around :func:`puissant.vinput`, which allows writing
generic user-validated input functions.

Examples
===========

- yes or no questions (`bool` output)::

    >>> from puissant import *
    >>> yes_no(prompt = 'Do you want to continue', default = 'n')
    Do you want to continue [y/n]?(default:n) y
    True
    >>> yes_no(prompt = 'Do you want to continue', default = 'n')
    Do you want to continue [y/n]?(default:n) <= Enter
    False

- menu input::

    >>> menu(prompt = 'what next?', options = ['restart', 'continue', 'quit'])
    what next?
     1 - restart
     2 - continue
     3 - quit
    select an item [range: 1..3]: 5
    input must be in range 1..3.
    select an item [range: 1..3]: 3
    (2, 'quit')

- tickbox menu::

    >>> tickbox_menu('add extras', ['mayo', 'ketchup', 'garlic', 'tabasco'])
    add extras
    1  [ ] - mayo
    2  [ ] - ketchup
    3  [ ] - garlic
    4  [ ] - tabasco

    - type a number to tick the option.
    - "a" selects all.
    - "n" de-selects all.
    - "d" selection done.

    Option? : 1
    add extras
    1  [x] - mayo
    2  [ ] - ketchup
    3  [ ] - garlic
    4  [ ] - tabasco

    - type a number to tick the option.
    - "a" selects all.
    - "n" de-selects all.
    - "d" selection done.

    Option? : 4
    add extras
    1  [x] - mayo
    2  [ ] - ketchup
    3  [ ] - garlic
    4  [x] - tabasco

    - type a number to tick the option.
    - "a" selects all.
    - "n" de-selects all.
    - "d" selection done.

    Option? : d
    [(0, 'mayo'), (3, 'tabasco')]


- string enumeration input::

    >>> enum_str(prompt = 'how do you want it?', enum = ['fried', 'poached', 'scrambled'])
    how do you want it? (valid choices: fried, poached, scrambled):
    raw
     input must be one of fried, poached, scrambled.
    how do you want it? (valid choices: fried, poached, scrambled):
    poached
    'poached'

- ranged integer input::

    >>> ranged_int(prompt = 'how old are you?', low = 1, high = 150)
    how old are you? [range: 1..150]: -3
    input must be in range 1..150.
    how old are you? [range: 1..150]: 151
    input must be in range 1..150.
    how old are you? [range: 1..150]: 35
    35

"""

from __future__ import annotations


from typing import Tuple, TypeVar, Sequence, Callable, List, Type, Any
import os

T = TypeVar("T")
R = TypeVar("R")


def _identity(x: T) -> Any:
    return x


def _always_good(x: T) -> bool:
    return True


def menu(prompt: str, options: List[str], retries=-1) -> str:
    """gets a validated input string from a string menu.

    Example::

        >>> from puissant import *
        >>> menu(prompt = 'pick a fruit', options = ['pear','apple','orange'])
        pick a fruit
         1 - pear
         2 - apple
         3 - orange
        select an item [range: 1..3]: 4
        input must be in range 1..3.
        select an item [range: 1..3]: pear
        input must be of type int.
        select an item [range: 1..3]: 2
        (1, 'apple')

    Arguments:
        prompt: user input prompt.
        options: list of strings from which users selects one.
        retries: numbers of retries before input is aborted (-1 = no limit)

    Returns:
        the string selected by user from `options`, if input is valid.

    Raises:
        ValueError: if invalid input is entered for ``retries + 1``

    """
    menu_str = prompt + "\n"
    menu_str += "\n".join([f"{i+1:2} - {o}" for i, o in enumerate(options)])
    print(menu_str, flush=True)
    i = ranged_int("select an item", 1, len(options), retries=retries)
    return options[i - 1]


def yes_no(prompt: str, default: str | None = None, retries: int = -1) -> bool:
    """gets validated input from user for a yes/no question.

    Example::

        >>> from puissant import *
        >>> yes_no('do you want desert')
        do you want desert [y/n]?maybe
         input must be one of y, n, yes, no.
        do you want desert [y/n]?y
        True
        >>> yes_no('are you ok', default = 'n')
        are you ok [y/n]?(default:n)
        False

    Arguments:
        prompt: user input prompt.
        default: default input value if user enters newline only.
        retries: allowed number of extra attempts for user input (-1 = unlimited)

    Returns:
        True (affirmative answer) or False (negative answer)

    Raises:
        ValueError: if invalid input is entered for ``retries + 1``
    """
    return vinput(
        prompt + " [y/n]?",
        typ=str,
        default=default,
        retries=retries,
        enum=["y", "n", "yes", "no"],
        pre_fn=str.lower,
        post_fn=lambda x: x in ["y", "yes"],
    )


def tickbox_menu(prompt: str, options: List[str]) -> List[Tuple[int, str]]:
    """gets validated, multiple user input from a tick-box menu.

    Examples::

        >>> tickbox_menu('make up your own menu', options = ['fries', 'burger', 'onion rings', 'salad'])
        make up your own menu
        1  [ ] - fries
        2  [ ] - burger
        3  [ ] - onion rings
        4  [ ] - salad

        - type a number to tick the option.
        - "a" selects all.
        - "n" de-selects all.
        - "d" selection done.

        Option? : 1
        make up your own menu
        1  [x] - fries
        2  [ ] - burger
        3  [ ] - onion rings
        4  [ ] - salad

        - type a number to tick the option.
        - "a" selects all.
        - "n" de-selects all.
        - "d" selection done.

        Option? : 2
        make up your own menu
        1  [x] - fries
        2  [x] - burger
        3  [ ] - onion rings
        4  [ ] - salad

        - type a number to tick the option.
        - "a" selects all.
        - "n" de-selects all.
        - "d" selection done.

        Option? : d
        [(0, 'fries'), (1, 'burger')]

    Arguments:
        prompt: user input prompt.
        options: list of options to tick.

    Returns:
        a list of tuples, each one containing the index of a ticket item, and the item itself.

    """
    marked_options = list([0 for o in options])
    while True:
        menu_str = prompt + "\n"
        for i, o in enumerate(options):
            m = "x" if marked_options[i] else " "
            menu_str += f"{i+1:<2} [{m}] - {o}\n"

        menu_str += "\n- type a number to tick the option.\n"
        menu_str += '- "a" selects all.\n'
        menu_str += '- "n" de-selects all.\n'
        menu_str += '- "d" selection done.\n'
        print(menu_str)
        x = _rint_estr_in("Option? ", low=1, high=len(options), enum=["a", "n", "d"])

        try:
            marked_options[int(x) - 1] = 1
        except ValueError:
            if x == "a":
                marked_options = list([1 for o in options])
            elif x == "n":
                marked_options = list([0 for o in options])
            elif x == "d":
                break
    return [(i, o) for i, o in enumerate(options) if marked_options[i]]


def _rint_estr_in(prompt: str, low: int, high: int, enum: List[str], retries=-1) -> str:
    """get user input from a range of ints and a list of strings.

    Internal function, not meant for API (to be used inside menu_tickbox function).
    """
    extended_enum = enum + list([str(i) for i in range(low, high + 1)])
    return enum_str(prompt, extended_enum, quiet=True, retries=retries)


def enum_str(
    prompt: str,
    enum: List[str],
    default: str | None = None,
    quiet: bool = False,
    retries=-1,
) -> str:

    valid_choices = ", ".join(enum)

    if quiet:
        fprompt = prompt + ": "
    else:
        fprompt = f"{prompt} (valid choices: {valid_choices}):\n"
        # if len(valid_choices) + len(prompt) > (os.get_terminal_size()[0] - 18):
        #     fprompt = f'{prompt}\n(valid choices: {valid_choices}):\n'
        # else:
        #     fprompt = f'{prompt} (valid choices: {valid_choices}):\n'

    return vinput(fprompt, typ=str, default=default, retries=retries, enum=enum)


def ranged_int(
    prompt: str, low: int, high: int, default: int | None = None, retries: int = -1
) -> int:
    """gets ranged integer validated user input.

    Example::

        >>> ranged_int(prompt = 'roll a dice...', low = 1, high = 6)
        roll a dice... [range: 1..6]: 0
        input must be in range 1..6.
        roll a dice... [range: 1..6]: 1
        1

    Arguments:
        prompt: user input prompt.
        low: minimum allowed integer input.
        high: maximum allowed integer input.
        default: default result if user only presses Return.
        retries: allowed number of attempts for user input.

    Returns:
        The integer user input, if it is deemed valid.

    Raises:
        ValueError, after ``retries + 1`` invalid user input attemtpts.
    """

    return vinput(
        prompt + f" [range: {low}..{high}]: ",
        typ=int,
        default=default,
        retries=retries,
        nrange=(low, high),
    )


def ranged_float(
    prompt: str, low: float, high: float, default: float | None = None, retries=-1
) -> float:
    """gets ranged float validated user input.

    Example::

        >>> ranged_float('how tall are you in meters?', 0.5, 2.75)
        how tall are you in meters? [range: 0.5..2.75]: 0.3
        input must be in range 0.5..2.75.
        how tall are you in meters? [range: 0.5..2.75]: 3.0
        input must be in range 0.5..2.75.
        how tall are you in meters? [range: 0.5..2.75]: 1.75
        1.75

    Arguments:
        prompt: user input prompt.
        low: minimum allowed floating point input.
        high: maximum allowed floating point input.
        default: default result if user only presses Return.
        retries: allowed number of attempts for user input.

    Returns:
        The floating point user input, if it is deemed valid.

    Raises:
        ValueError, after ``retries + 1`` invalid user input attemtpts.
    """

    return vinput(
        prompt + f" [range: {low}..{high}]: ",
        typ=float,
        default=default,
        retries=retries,
        nrange=(low, high),
    )


def vinput(
    prompt: str,
    typ: Type[T],
    default: T | None = None,
    retries: int = -1,
    nrange: Tuple[T, T] | None = None,
    enum: Sequence[T] | None = None,
    pre_fn: Callable[[T], Any] = _identity,
    validation_fn: Callable[[T], bool] = _always_good,
    post_fn: Callable[[T], Any] = _identity,
    type_err_msg: str | None = None,
    enum_err_msg: str | None = None,
    range_err_msg: str | None = None,
) -> Any:

    """performs validated command line user input.

    Examples:

    * yes/no question::

        >>> from puissant import *
        >>> vinput(prompt = 'Do you want to continue [y/n]? ',
        ...        typ = str,
        ...        enum = ['y','n','yes','no'],
        ...        pre_fn = str.lower,
        ...        post_fn = lambda x: x in ['y','yes']
        ...
        ... )
        Do you want to continue [y/n]? maybe
         input must be one of y, n, yes, no.
        Do you want to continue [y/n]? 2
         input must be one of y, n, yes, no.
        Do you want to continue [y/n]? y
        True

    * string enumeration choice::

        >>> vinput(prompt = 'which color do you prefer? ',
        ...        typ = str,
        ...        enum = ['green','blue','red','yellow','purple'])
        which color do you prefer? white
         input must be one of green, blue, red, yellow, purple.
        which color do you prefer? 3
         input must be one of green, blue, red, yellow, purple.
        which color do you prefer? green
        'green'

    * ranged integer input with custom error message and retries limit::

        >>> vinput(prompt = 'enter your age: ',
        ...        typ = int,
        ...        nrange = (0,130),
        ...        retries = 2,
        ...        range_err_msg = "Surely that's not your age!")
        enter your age: 150
        Surely that's not your age!
        enter your age: james
        input must be of type int.
        enter your age: -3
        Surely that's not your age!
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/home/garciaal/prj/puissant/puissant/__init__.py", line 233, in vinput
            raise ValueError(f"Invalid user input for {tries - 1} times.")
        ValueError: Invalid user input for 3 times.


    Arguments:
        prompt:  prompt for the user.
        typ:     expected type of user input.
        default: default value for user input if only Return pressed.
        retries: allowed number of user input retries. -1 for infinte.
        nrange:  optional allowed ``(min,max)`` range for user input.
        enum:    optional enumeration of allowed user inputs.
        pre_fn:  hook for a function to be called on input data prior to validate it. If not fgiven, identity function is used (returns its input unchanged)
        validation_fn: optional custom validation function. If none given, data is always deemed valid, if it has type ``typ`` and meets belongs to ``nrange`` or ``enum`` if given.
        post_fn: optional post-validation function to be run on input data. If not given, the identity function is used (returns its input unchanged)
        type_err_msg: optional custom message to print if input data is not of type ``type``.
        enum_err_msg: custom message to print if input data is not included in ``enum``.
        range_err_msg: custom message to print if input data is out of range ``nrange``

    Returns:
        ``post_fn(pre_fn(user_input))`` if input is deemed valid.

    Raises:
        ValueError after ``retries + 1`` invalid user input attempts.
    """

    if nrange != None and enum != None:
        raise ValueError("nrange and enum are mutually exclusive parameters.")

    tries = 0

    if default != None:
        prompt = prompt + f"(default:{default}) "

    while True:
        tries += 1
        if retries >= 0 and tries > retries + 1:
            raise ValueError(f"Invalid user input for {tries - 1} times.")
        print(prompt, end="")
        rin = input("")

        if rin == "" and default != None:
            return post_fn(pre_fn(default))

        try:
            tin = typ(rin)
        except ValueError:
            if type_err_msg == None:
                print(f"input must be of type {typ.__name__}.")
            else:
                print(type_err_msg)

            continue

        kin = pre_fn(tin)

        if nrange != None:
            min_ = nrange[0]
            max_ = nrange[1]

            if kin < min_ or kin > max_:
                if range_err_msg == None:
                    print(f"input must be in range {min_}..{max_}.")
                else:
                    print(range_err_msg)

                continue

        if enum != None:
            enum_str = ", ".join([str(e) for e in enum])
            if not kin in enum:
                if enum_err_msg == None:
                    print(f" input must be one of {enum_str}.")
                else:
                    print(enum_err_msg)

                continue

        good = validation_fn(kin)
        if not good:
            continue

        # if nothing went wrong, the value is accepted
        break

    return post_fn(kin)

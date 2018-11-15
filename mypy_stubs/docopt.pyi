# reference: https://github.com/docopt/docopt/pull/334

from typing import (
    Any,
    List,
    Tuple,
    Union,
    # These docopt classes must not be clobbered.
    Dict as TDict,
    Optional as TOptional,
)


# Acceptable source types for parsing.
TSource = Union[str, List[str]]

# Acceptable values in a Docopt Dict.
TDocoptValue = Union[bool, int, str, List[str]]

# A map of flags/options to their acceptable values.
TDocoptDict = TDict[str, TDocoptValue]

def docopt(
    doc: str,
    argv: TOptional[TSource]=None,
    help: TOptional[bool]=True,
    version: TOptional[str]=None,
    options_first: TOptional[bool]=False) -> TDocoptDict: ...

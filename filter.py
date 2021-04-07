import re
from typing import Union

from utils import num_to_char_lut, build_pattern
from functools import lru_cache


class Filter:

    def __init__(self, rgx: Union[str, None], pattern: Union[str, None]):
        # initialize regex and pattern
        if rgx is not None:
            self.filter = re.compile(rgx.lstrip('='))
        else:
            self.filter = None

        if pattern is not None:
            self.pattern = pattern.lstrip('=')
        else:
            self.pattern = None

    def good(self, v: str) -> bool:
        """
        checks if a given string matches the filter
        if no filter was specified in __init__ then this always returns True

        :param v: the string you want to match
        :return: False if it does not match the filter
        """

        if self.filter is None:
            return True
        return self.filter.match(v) is not None

    @lru_cache(maxsize=32)
    def _make_default_pattern(self, col):
        # in case that self.pattern is None, we need to generate a
        # default input pattern from the input data

        default_pattern = ''

        # attach a sequence of form `{<char>0}-` for each line in the
        # collection
        for i in range(len(col)):
            char = num_to_char_lut(i)
            default_pattern += '{' + char + '0}-'

        # get rid of trailing `-`
        default_pattern.strip('-')

        # add the ending `.wav`
        default_pattern += '.wav'
        self.pattern = default_pattern

    def pattern_replace(self, col):

        # check if a pattern was specified
        if self.pattern is None:
            self._make_default_pattern(tuple(col))

        # this dictionary will hold all sub-patterns,
        # with the key being the string to be replaced
        # and the value the string to replace
        match_dict = {}

        for i, item in enumerate(col):

            # the current category is the corresponding letter
            # in the alphabet
            category = num_to_char_lut(i)

            # helper function to build the string of format `{<category><match-num>}`
            def to_entry(num):
                return '{' + category + str(num) + '}'

            # the 0th element is always the entire match
            match_dict[to_entry(0)] = item

            # if a filter is available, all the matches after that is the groups of
            # the regex filter
            if self.filter is not None:
                for inner, content in enumerate(self.filter.match(item).groups()):
                    match_dict[to_entry(inner + 1)] = content

        # collapse the dictionary into the pattern
        return build_pattern(match_dict, self.pattern)

    def __str__(self):
        return f"Filter: [{self.filter}] Pattern: [{self.pattern}]"

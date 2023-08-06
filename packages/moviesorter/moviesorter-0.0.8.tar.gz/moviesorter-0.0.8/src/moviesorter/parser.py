import logging
import os
import re
from typing import List, Tuple, Optional


class ParsingError(Exception):
    pass


# Try all of these to look for a release year in the media name.
# Year is 4 numbers after all, so this can get pretty vague,
# so let's start with the most likely patterns, this is the best we can do (?)
YEAR_PATTERNS = (
    re.compile(r"\(([0-9]{4})\)"),
    re.compile(r"[^0-9]\(?([0-9]{4})\)?[^0-9]"),
    re.compile(r"^\(?([0-9]{4})\)?$"),
)

# Try all of these patterns to look for Sxx Eyy identifiers.
# Incoming basename will be split and rejoined with spaces, so there is less possibilities...
SxxEyy_PATTERNS = (
    re.compile(r"[Ss]([0-9]+) ?[Ee]([0-9]+)"),  # Show S05 E
    re.compile(r" ([0-9][0-9][0-9]?) ([0-9][0-9]?[0-9]?) "),  # Show 05 24.avi
)

SxxEyy_PATTERNS_EXTENDED = (
    *SxxEyy_PATTERNS,
    re.compile(r"E([0-9][0-9])[^0-9]"),  # Show with episode id only
    re.compile(r" ([0-9][0-9]) "),  # Show with episode id only in a very vague format, last resort!
)


# Try all of these patterns to clean up any leftover "junk" in the media name after
# "Sxx Eyy" or "year" data has been extracted.
CLEAN_PATTERNS = (
    re.compile(r"\[[^ ]*]"),
    *YEAR_PATTERNS
)


log = logging.getLogger(".".join([__package__, __name__]))


def split_basename(
        src_path: str,
        split_characters: List[str] = (".", " "),
        min_split_length: int = 3,
        invalid_single_characters: List[str] = ("-",)
) -> List[List[str]]:
    """
    Split a source path file name (basename) into individual words.

    :param src_path:str: Pass the source path to the function
    :param split_characters:List[str]: Specify the characters that are used to split the filename
    :param min_split_length:int: Specify the minimum number of parts that is allowed in the filename
    :param invalid_single_characters:List[str]: Exclude invalid single characters.
    :return: A list of strings
    """
    basename = os.path.basename(src_path)  # Get basename from the path
    filename = os.path.splitext(basename)[0]  # Discard the extension to get the filename

    # Try splitting the filename
    splits = [filename.split(split_character) for split_character in split_characters]
    splits.sort(key=lambda parts: len(parts), reverse=True)
    # filename_parts = splits[0]
    # if len(filename_parts) < min_split_length:
    #     raise ParsingError(
    #         f"Filename '{filename}' could not be split into sufficient parts to be parsed."
    #     )

    result = []
    for split in splits:
        if len(split) < min_split_length:
            continue
        # Some 'special' characters can mess up the search query.
        # Ignore in case of such filename formatting, e.g.: "Westworld - S03E08.avi"
        result.append([part for part in split if part not in invalid_single_characters])

    if not result:
        raise ParsingError(
            f"Filename '{filename}' could not be split into sufficient parts to be parsed."
        )

    return result


def _find_sxx_eyy(
        src_path: str, split_characters: List[str], min_split_length: int, force: bool = False
) -> Tuple[List[str], int, int]:

    # Try all the possibilities base on the configured split chars.
    splits = split_basename(src_path, split_characters=split_characters, min_split_length=min_split_length)

    # Start with the longest split.
    splits.sort(key=lambda array: len(array), reverse=True)

    for possible_split in splits:
        string = " ".join(possible_split)
        for pat in SxxEyy_PATTERNS if not force else SxxEyy_PATTERNS_EXTENDED:
            if match := re.search(pat, string):
                # Yay! That was easy...
                if len(match.groups()) == 1:
                    season_id = str(1)
                    episode_id = match.groups()[0]
                else:
                    season_id, episode_id = match.groups()
                season_id = int(season_id)
                episode_id = int(episode_id)
                start_index, _ = match.span()
                return string[:start_index].split(), season_id, episode_id
    raise ParsingError(f"No valid Sxx Eyy found in '{src_path}'.")


def _find_title_and_year(
        src_path: str, split_characters: List[str], min_split_length: int
) -> Tuple[List[str], Optional[int]]:
    """
    The _find_title_and_year function takes a path to a file and splits it into its title and year.

    :param src_path:str: Get the source path of a file
    :param split_characters:List[str]: Define the characters that will be used to split the string
    :param min_split_length:int: Determine how many characters we should split on
    :return: A tuple of two values:
    :doc-author: Trelent
    """

    # Try all the possibilities based on the configured split chars.
    splits = split_basename(src_path, split_characters=split_characters, min_split_length=min_split_length)

    # Start with the longest split.
    splits.sort(key=lambda array: len(array), reverse=True)

    # Go by patterns - there are many possibilities, we want to try to find the best patterns first.
    for pat in YEAR_PATTERNS:
        for possible_split in splits:
            string = " ".join(possible_split)
            if match := re.search(pat, string):
                matched_group = match.groups()[-1]
                start_index = match.span()[-2]
                return string[:start_index].split(), int(matched_group)
    return splits[0], None


def parse_season_and_episode(
        src_path: str, split_characters: List[str], min_split_length: int, force: bool = False
) -> Optional[Tuple[str, int, int]]:
    """
    The parse_season_and_episode function attempts to parse a series name, season number, and episode number from the
    given source path. It does this by first splitting the filename into words (separated by spaces), then searching for
    words that match SxxExx in them. If one is found, it is assumed to be part of the series title and removed from the list
    of words. The remaining words are then searched for numbers that could be either season or episode identifiers; if both
    are found, they are returned as a tuple along with the cleaned-up version of what was originally in src_path.

    :param src_path:str: Specify the path to the file that is being processed
    :param split_characters:List[str]: Specify a list of characters that should be used to split the filename into parts
    :param min_split_length:int: Specify the minimum length of a split word to be considered
    :param force:bool=False: Force the function to search for sxxexx even if it is not found in the filename
    :return: A tuple of three values:
    :doc-author: Trelent
    """
    """Try to search for and parse series and episode identifiers (SxxEyy)."""
    filename_parts, season_id, episode_id = _find_sxx_eyy(
        src_path, split_characters=split_characters, min_split_length=min_split_length, force=force
    )

    raw_series_title = list()
    for word in filename_parts:

        # Skip years in the title, because of The Grand Tour
        for pat in YEAR_PATTERNS:
            if re.search(pat, word):
                break
        else:
            raw_series_title.append(word)

    final_name = ' '.join([x.lower() for x in raw_series_title])
    for pat in CLEAN_PATTERNS:
        final_name = re.sub(pat, "", final_name).strip()

    return final_name, season_id, episode_id


def parse_movie_name(
    src_path: str, split_characters: List[str], min_split_length: int
) -> Tuple[str, Optional[str]]:
    """Try to search for and parse movie title and release year."""
    # Pick the longest (= best chance of the right one in case of a mixed name).
    # filename_parts = split_basename(src_path, split_characters, min_split_length)[0]

    filename_parts, movie_year = _find_title_and_year(
        src_path, split_characters=split_characters, min_split_length=min_split_length
    )

    if not movie_year:
        log.warning(f"No valid year found in '{src_path}'.")

    final_name = " ".join([part.lower() for part in filename_parts])
    for pat in CLEAN_PATTERNS:
        final_name = re.sub(pat, "", final_name)

    return final_name, movie_year


def fix_leading_the(series_title):
    """Fix leading The's in the series title"""
    if re.match('[Tt]he\s(.*)', series_title):
        return re.match('[Tt]he\s(.*)', series_title).group(1) + ', The'
    return series_title

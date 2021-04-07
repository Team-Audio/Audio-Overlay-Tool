import asyncio
import os
from typing import AnyStr, Dict

from pydub import AudioSegment
from pathlib import Path


def is_file_in_dir(file: AnyStr, directory: AnyStr) -> bool:
    """
    same as os.path.isfile but with a cwd

    :param file: the file you want to check
    :param directory: the directory that the file lives in
    :return: True if the file exists
    """
    return os.path.isfile(os.path.join(directory, file))


def merge_audio(a, *rest, out) -> None:
    """
    Merges two or more audio files

    :param a: the path to the  base file
    :param rest: the paths to the other files you want to overlay
    :param out: the path to save the new file under
    """

    # open samples
    start = AudioSegment.from_file(a)
    others = [AudioSegment.from_file(x) for x in rest]

    # keep overlaying
    for other in others:
        start = start.overlay(other)

    # export final audio
    start.export(out, format='wav')


def ensure_folder(path: AnyStr) -> None:
    """
    Makes sure that a folder and all its parents exist
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def num_to_char_lut(num: int) -> str:
    """
    Translates a number to the corresponding character in the alphabet
    0->a
    1->b
    2->c etc..
    """
    lut = "abcdefghijklmnopqrstuvwxyz"
    return lut[num]


def build_pattern(match_dict: Dict[str, str], pattern: str) -> str:
    """
    Collapses a dictionary into a string based on the keys
    For example:
    match_dict = { 'a' : 'c' }
    pattern = 'abc'

    result = 'cbc'

    :return:
    """

    p = pattern
    for key, value in match_dict.items():
        p = p.replace(key, value)
    return p


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped

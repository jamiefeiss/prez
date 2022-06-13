import os
import re
from typing import Dict, List

import jinja2
from starlette_core.templating import Jinja2Templates

from config import *


def get_config(var):
    """Gets a config variable from config.py"""
    import config

    return getattr(config, var)


def append_qsa(uri: str, qsas: Dict[str, str]) -> str:
    """Appends QSAs to a URL & sorts according to an order"""

    def qsa_sort(key: str) -> int:
        if key == "uri":
            return 0
        elif key == "_profile":
            return 1
        elif key == "_mediatype":
            return 2
        else:
            return 3

    qsa_dict = {}
    if "?" in uri:
        path, qsa_str = uri.split("?")
        for qsa in qsa_str.split("&"):
            key, value = qsa.split("=")
            qsa_dict[key] = value
    else:
        path = uri
    qsa_dict.update(qsas)
    qsa_list = [(key, value) for key, value in qsa_dict.items()]
    for i, qsa in enumerate(sorted(qsa_list, key=lambda k: qsa_sort(k[0]))):
        if i == 0:
            path += f"?{qsa[0]}={qsa[1]}"
        else:
            path += f"&{qsa[0]}={qsa[1]}"
    return path

def file_exists(path: str) -> bool:
    """Checks whether a file exists"""
    return os.path.isfile(path)

def match(s: str, pattern: str) -> bool:
    """Matches a string to a regex pattern"""
    if re.match(pattern, s):
        return True
    else:
        return False

def prez_title(s: str) -> str:
    """Correctly formats the casing of a *Prez string when lower case
    i.e. vocprez -> VocPrez"""
    return "".join([substr.capitalize() for substr in re.split("(prez)", s)[:2]])

def join_list_keys(l: List, key: str, sep: str) -> str:
    """Concatenates a list of dicts into a string of key values with a specified separator"""
    return sep.join([e[key] for e in l])


template_list = ["templates"]
if THEME_VOLUME is not None:
    template_list.insert(0, f"{THEME_VOLUME}/templates")

templates = Jinja2Templates(
    loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(template_list)])
)
templates.env.filters["get_config"] = get_config
templates.env.filters["append_qsa"] = append_qsa
templates.env.filters["file_exists"] = file_exists
templates.env.filters["match"] = match
templates.env.filters["prez_title"] = prez_title
templates.env.filters["join_list_keys"] = join_list_keys

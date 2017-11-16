from jinja2.filters import FILTERS
import re

__all__ = ["format_price_table", "format_number", "format_altitude", "format_index", "format_none",
           "format_specials", "format_title", "description"]

symbols = {
    "BOOST": "boost",
    "SETBACK": "setback",
    "ABILITY": "ability",
    "PROFICIENCY": "proficiency",
    "DIFFICULTY": "difficulty",
    "CHALLENGE": "challenge",
    "SUCCESS": "success",
    "ADVANTAGE": "advantage",
    "TRIUMPH": "triumph",
    "FAILURE": "failure",
    "THREAT": "threat",
    "DESPAIR": "despair",
    "FORCE": "force",
    "FORCE POINT": "force-pip",
    "LIGHT": "force-light",
    "DARK": "force-dark"
}

diff = {
    "SIMPLE": "Simple (-)",
    "EASY": 'Easy (<span class="symbol difficulty">d</span>)',
    "AVERAGE": 'Average (<span class="symbol difficulty">dd</span>)',
    "HARD": 'Hard (<span class="symbol difficulty">ddd</span>)',
    "DAUNTING": 'Daunting (<span class="symbol difficulty">dddd</span>)',
    "FORMIDABLE": 'Formidable (<span class="symbol difficulty">ddddd</span>)'
}

check_regex = re.compile(r"\[CHECK:([A-Z]+):([a-zA-Z()_]+)\]")
diff_skill_regex = re.compile(r"\[([A-Z]+):([a-zA-Z()_]+)\]")
diff_regex = re.compile(r"\[DIFF:([A-Z]+)\]")


def description(s: str):
    """Simple function that does all the filtering it needs to for most descriptions"""
    for (key, value) in symbols.items():
        # todo optimise? use something similar to re.sub
        s = s.replace(f"[{key}]", f'<span class="symbol {value}"></span>')
    s = re.sub(check_regex, lambda match: f"<b>{diff[match.group(1)]} {format_skill(match.group(2))} check</b>", s)
    s = re.sub(diff_skill_regex, lambda match: f'<b>{diff[match.group(1)]} {format_skill(match.group(2))}</b>', s)
    s = re.sub(diff_regex, lambda match: f'<b>{diff[match.group(1)]}</b>', s)
    return s


def format_skill(skill):
    return f'<a href="/skills/{skill}">{format_title(skill)}</a>'


def format_number(s):
    s = str(s)
    if len(s) <= 3:
        return s
    for i in range(len(s)-3, 0, -3):
        s = f'{s[:i]},{s[i:]}'
    return s


def format_price_table(price, restricted):
    s = ""
    if restricted:
        s += "(R) "
    s += format_number(price)
    return s


def format_index(arr):
    out = ""
    for index in arr:
        if len(index) == 0:
            continue
        out += f'<a href="/books/{index.split(":")[0]}">{index.split(":")[0]}:{index.split(":")[1]}</a>, '
    return out[:-2]


def format_specials(arr):
    out = ""
    for special in arr:
        out += f'<a href="/qualities/{special["special"]}">{format_title(special["special"])}</a>'
        if "rank" in special:
            out += f" {str(special['rank'])}"
        out += ", "
    return out[:-2]


def format_none(s):
    if type(s) == int and s == 0:
        return "None"
    return s


def format_altitude(s):
    if s >= 1000:
        return str(s)[:-3] + " kilometers"
    if s == 1:
        return str(s) + " meter"
    return str(s) + " meters"


def format_title(s: str):
    return s.replace("_", " ")


def register():
    FILTERS["formatnum"] = format_number
    FILTERS["formatprice"] = format_price_table
    FILTERS["formatindex"] = format_index
    FILTERS["special"] = format_specials
    FILTERS["none"] = format_none
    FILTERS["altitude"] = format_altitude
    FILTERS["title"] = format_title
    FILTERS["description"] = description

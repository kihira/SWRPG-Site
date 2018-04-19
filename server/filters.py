import re

from flask import json

__all__ = ["format_price_table", "format_number", "format_altitude", "format_index", "format_none",
           "format_list", "title", "description"]

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
    "NONE": "",
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
    s = re.sub(diff_regex, lambda match: f'<b>{diff[match.group(1)]}</b>', s)
    s = re.sub(diff_skill_regex, lambda match: f'<b>{diff[match.group(1)]} {format_skill(match.group(2))}</b>', s)
    return s


def to_json(model: {}):
    out = {"columns": [], "index": model.index, "categories": model["category"] is not None}
    for field in model.fields:
        if field.table_display():
            out["columns"].append(field.get_datatables_object())
    return json.dumps(out)


def format_skill(skill):
    return f'<a href="/skills/{skill}">{title(skill)}</a>'


def format_number(s):
    return "{:,}".format(s)


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


def format_list(arr, url):
    if not arr and len(arr) == 0:
        return "None"
    out = ""
    for special in arr:
        if type(special) == dict:
            out += f'<a href="/{url}/{special["id"]}">{title(special["id"])}</a>'
            if "value" in special:
                out += f" {str(special['value'])}"
        else:
            out += f'<a href="/{url}/{special}">{title(special)}</a>'
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


def title(s: str):
    return s.replace("_", " ")


def register(FILTERS: dict):
    FILTERS["formatnum"] = format_number
    FILTERS["formatprice"] = format_price_table
    FILTERS["formatindex"] = format_index
    FILTERS["link_list"] = format_list
    FILTERS["none"] = format_none
    FILTERS["altitude"] = format_altitude
    FILTERS["title"] = title
    FILTERS["description"] = description
    FILTERS["modeltojson"] = to_json

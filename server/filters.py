import re

from flask import json

__all__ = ["format_price", "format_number", "format_altitude", "format_index", "format_none",
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
skill_regex = re.compile(r"\[SKILL:([a-zA-Z()_]+)\]")
talent_regex = re.compile(r"\[TALENT:([a-zA-Z()_]+)\]")
characteristic_regex = re.compile(r"\[CHARACTERISTIC:([a-zA-Z()_]+)\]")
quality_regex = re.compile(r"\[QUALITY:([a-zA-Z()_]+)\]")


def description(s: str) -> str:
    """Simple function that does all the filtering it needs to for most descriptions"""
    for (key, value) in symbols.items():
        # todo optimise? use something similar to re.sub
        s = s.replace(f"[{key}]", f'<span class="symbol {value}"></span>')
    s = re.sub(talent_regex, lambda match: f'{format_talent(match.group(1))}', s)
    s = re.sub(characteristic_regex, lambda match: f'{match.group(1)}', s)  # todo implement this
    s = re.sub(quality_regex, lambda match: f'{format_quality_object(match.group(1))}', s)
    s = re.sub(skill_regex, lambda match: f'{format_skill(match.group(1))}', s)
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


def format_skill(skill: str) -> str:
    return f'<a href="/skills/{skill}">{title(skill)}</a>'


def format_talent(talent: str) -> str:
    return f'<a href="/talents/{talent}">{title(talent)}</a>'


def format_quality_object(quality: any) -> str:
    if type(quality) is dict:
        return format_quality(quality["id"], quality["value"])
    return format_quality(quality, 0)


def format_quality(quality: str, rating: int) -> str:
    return f'<a href="/qualities/{quality}">{title(quality)}{f" {str(rating)}" if rating != 0 else ""}</a>'


def format_number(s) -> str:
    return "{:,}".format(s)


def format_yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def format_price(price, restricted):
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
    if (type(s) == int and s == 0) or (type(s) == list and len(s) == 0):
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
    FILTERS["price"] = format_price
    FILTERS["formatindex"] = format_index
    FILTERS["link_list"] = format_list
    FILTERS["none"] = format_none
    FILTERS["altitude"] = format_altitude
    FILTERS["title"] = title
    FILTERS["description"] = description
    FILTERS["modeltojson"] = to_json
    FILTERS["skill"] = format_skill
    FILTERS["talent"] = format_talent
    FILTERS["quality"] = format_quality

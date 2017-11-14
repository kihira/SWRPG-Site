from jinja2.filters import FILTERS

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


def symbol(s: str):
    for (key, value) in symbols.items():
        s = s.replace(f"[{key}]", f'<span class="symbol {value}"></span>')
    return s


def skill_check(s: str):
    import re
    return re.sub(r"\[([A-Z]+):([a-zA-Z]+)\]", skill, s)


def skill(match):
    diff = match.group(1)
    out = "<b>"
    if diff == "EASY":
        out += 'Easy (<span class="symbol difficulty">d</span>)'
    elif diff == "AVERAGE":
        out += 'Average (<span class="symbol difficulty">dd</span>)'
    elif diff == "HARD":
        out += 'Hard (<span class="symbol difficulty">ddd</span>)'
    elif diff == "DAUNTING":
        out += 'Daunting (<span class="symbol difficulty">dddd</span>)'
    elif diff == "FORMIDABLE":
        out += 'Formidable (<span class="symbol difficulty">ddddd</span>)'
    else:
        out += diff.title()
    return f'{out} <a href="/skills/{match.group(2)}">{format_title(match.group(2))}</a></b>'


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
            out += f' {str(special["rank"]))}'
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
    return s.replace("_", " ").title()


def register():
    FILTERS["symbol"] = symbol
    FILTERS["formatnum"] = format_number
    FILTERS["formatprice"] = format_price_table
    FILTERS["formatindex"] = format_index
    FILTERS["special"] = format_specials
    FILTERS["none"] = format_none
    FILTERS["altitude"] = format_altitude

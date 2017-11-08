from jinja2.filters import FILTERS

symbols = {
    "BOOST": "boost",
    "SETBACK": "setback",
    "ABILITY": "ability",
    "PROFICIENCY": "proficiency",
    "DIFFICULTY": "difficulty",
    "CHALLENGE": "challenge"
}


def symbol(s):
    for (key, value) in symbols.items():
        s = s.replace("[{0}]".format(key), "<span class=\"symbol {0}\"></span>".format(value))
    return s


def format_number(s):
    s = str(s)
    if len(s) <= 3:
        return s
    for i in range(len(s)-3, 0, -3):
        s = s[:i] + "," + s[i:]
    return s


def format_price_table(price, restricted):
    s = ""
    if restricted:
        s += "(R) "
    s += format_number(price)
    return s


def register():
    FILTERS["symbol"] = symbol
    FILTERS["formatnum"] = format_number
    FILTERS["formatprice"] = format_price_table

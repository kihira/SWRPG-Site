from jinja2.filters import FILTERS

symbols = {
    "BOOST": "boost",
    "SETBACK": "setback",
    "ABILITY": "ability",
    "PROFICIENCY": "proficiency",
    "DIFFICULTY": "difficulty",
    "CHALLENGE": "challenge",
    "ADVANTAGE": "advantage",
    "THREAT": "threat"
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


def format_index(arr):
    out = ""
    for index in arr:
        if len(index) == 0:
            continue
        out += "<a href=\"/books/{0}\">{0}:{1}</a>, ".format(index.split(":")[0], index.split(":")[1])
    return out[:-2]


def format_specials(arr):
    out = ""
    for special in arr:
        out += "<a href=\"/qualities/{0}\">{1}</a>".format(special["special"], special["special"].replace("_", " ").title())
        if "rank" in special:
            out += " " + str(special["rank"])
        out += ", "
    return out[:-2]


def register():
    FILTERS["symbol"] = symbol
    FILTERS["formatnum"] = format_number
    FILTERS["formatprice"] = format_price_table
    FILTERS["formatindex"] = format_index
    FILTERS["special"] = format_specials

from server.endpoint import Endpoint
from server.model import Model, Field, CheckboxField, TextareaField, SelectField, ArrayField
from server import filters

talents_endpoint = Endpoint("talents", "Talents", Model([
    Field("_id", "Talent", table=False),
    TextareaField("short", "Description", render=filters.description),
    TextareaField("description", "Long Description", table=False),
    SelectField("activation", "Activation", options=[
        {"display": "Passive", "value": "passive"},
        {"display": "Active", "value": "active"},
        {"display": "Active (Action)", "value": "active_action"},
        {"display": "Active (Incidental)", "value": "active_incidental"},
        {"display": "Active (Incidental, Out Of Turn)", "value": "active_incidental_oot"},
        {"display": "Active (Maneuver)", "value": "active_maneuver"},
    ], render=lambda x: activation(x)),
    CheckboxField("ranked", "Ranked"),
    CheckboxField("force", "Force Sensitive"),
    ArrayField(Field("index", "Index"), table=False)
]), objectid=False)
talents_endpoint.table_sort = {"key": "_id", "dir": 1}

abilities_endpoint = Endpoint("abilities", "Abilities", Model([
    Field("_id", "Ability", table=False),
    TextareaField("description", "Description", render=filters.description),
    ArrayField(Field("index", "Index"), table=False)
]))
abilities_endpoint.table_sort = {"key": "_id", "dir": 1}


def activation(value):
    if value == "passive":
        return "Passive"
    elif value == "active":
        return "Active"
    elif value == "active_action":
        return "Active (Action)"
    elif value == "active_incidental":
        return "Active (Incidental)"
    elif value == "active_incidental_oot":
        return "Active (Incidental, Out Of Turn)"
    elif value == "active_maneuver":
        return "Active (Maneuver)"
    else:
        return "Unknown"


def to_list(dic):
    out = ""
    for key in dic:
        out += key.replace("_", " ") + ", "
    return out[:-2]

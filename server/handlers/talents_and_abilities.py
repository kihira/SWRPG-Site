from server.decorators import get_item, login_required
from server.endpoint import Endpoint
from server.model import Model, Field, CheckboxField, TextareaField, SelectField, ArrayField
from server.app import app
from server.db import db
from server import filters
from flask import render_template, request, flash

talents_endpoint = Endpoint("talents", "Talents", Model([
    Field("_id", "Talent", table=False),
    TextareaField("short", "Description", render=filters.description),
    TextareaField("description", "Long Description", table=False),
    SelectField("activation", "Activation", options=[
        {"display": "Passive", "value": "passive"},
        {"display": "Active (Action)", "value": "active_action"},
        {"display": "Active (Incidental)", "value": "active_incidental"},
        {"display": "Active (Maneuver)", "value": "active_maneuver"},
        {"display": "Active (Out Of Turn)", "value": "active_oot"},
    ], render=lambda x: activation(x)),
    CheckboxField("ranked", "Ranked"),
    CheckboxField("force", "Force Sensitive"),
    ArrayField(Field("index", "Index"), table=False)
]))
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
    if value == "active_action":
        return "Active (Action)"
    if value == "active_incidental":
        return "Active (Incidental)"
    if not value:
        return "Passive"
    elif type(value) == dict:
        return "Active (" + to_list(value) + ")"
    else:
        return "Active"


def to_list(dic):
    out = ""
    for key in dic:
        out += key.replace("_", " ") + ", "
    return out[:-2]

from flask import Markup, render_template

from server.endpoint import Endpoint
from server.model import Model, Field, CheckboxField, TextareaField, SelectField, ArrayField, NumberField, FieldGroup, \
    ObjectIdField
from server.decorators import get_item
from server import filters
from server.app import app
from server.db import db
from server.filters import format_quality_object, format_skill

weapons_endpoint = Endpoint("weapons", "Weapons", Model([
    ObjectIdField("_id", "ID"),
    Field("name", "Name", table=False),
    SelectField("category", "Category", options=[
        "Brawl",
        "Energy",
        "Explosives",
        "Grenades",
        "Lightsaber Hilts",
        "Melee",
        "Micro-Rockets",
        "Other",
        "Portable Missiles",
        "Slugthrowers",
        "Thrown"
    ], table=False),
    SelectField("skill", "Skill", options=[
        {"display": "Brawl", "value": "brawl"},
        {"display": "Melee", "value": "melee"},
        {"display": "Lightsaber", "value": "lightsaber"},
        {"display": "Ranged (Light)", "value": "ranged_light"},
        {"display": "Ranged (Heavy)", "value": "ranged_heavy"},
        {"display": "Gunnery", "value": "gunnery"},
    ], render=format_skill),
    Field("damage", "Damage", default=0),
    Field("critical", "Critical", default="-"),
    SelectField("range", "Range", options=["Engaged", "Short", "Medium", "Long", "Extreme"]),
    NumberField("encumbrance", "Encumbrance"),
    NumberField("hardpoints", "Hardpoints"),
    NumberField("price", "Price", max=100000),
    CheckboxField("restricted", "Restricted"),
    NumberField("rarity", "Rarity", max=10),
    ArrayField(
        FieldGroup("qualities", "Special", [
            Field("id", "Quality ID"),
            NumberField("value", "Rating"),
        ], format_quality_object)),
    TextareaField("short", "Short Description", table=False),
    TextareaField("description", "Long Description", table=False),
    ArrayField(Field("index", "Index"), table=False),
]))

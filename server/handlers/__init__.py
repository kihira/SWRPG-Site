__all__ = []

from server.endpoint import Endpoint
from server.model import ObjectIdField, Field, SelectField, NumberField, CheckboxField, Model, TextareaField, \
    ArrayField, FieldGroup

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)


attachments = Endpoint("attachments", "Attachments", Model([
    ObjectIdField("_id", "ID", readonly=True),
    Field("name", "Name", table=False),
    SelectField("category", "Category", ["Armor", "Lightsaber", "Weapon"], table=False),
    NumberField("price", "Price", max=100000),
    CheckboxField("restricted", "Restricted"),
    NumberField("encumbrance", "Encumbrance"),
    NumberField("hardpoints", "HP Required"),
    NumberField("rarity", "Rarity", max=10),
    ArrayField(Field("models", "Model")),
    Field("modifiers", "Base Modifier"),
    ArrayField(
        FieldGroup("modification", "Modification", [
            NumberField("max", "Max", min=1),
            SelectField("type", "Type", [
                {"display": "Damage", "value": "damage"},
                {"display": "Weapon Quality", "value": "weapon_quality"},
                {"display": "Innate Talent", "value": "talent"},
                {"display": "Skill", "value": "skill"},
                {"display": "Characteristic", "value": "characteristic"},
                {"display": "Additional", "value": "other"},
            ]),
            Field("value", "Value"),
            Field("quality", "Weapon Quality", required=False),
            Field("talent", "Talent", required=False),
            Field("skill", "Skill", required=False),
            Field("characteristic", "Characteristic", required=False),
        ]), table=False),
    TextareaField("description", "Description"),
    ArrayField(Field("index", "Index"), table=False)
]))

armor = Endpoint("armor", "Armor", Model([
    ObjectIdField("_id", "ID", readonly=True),
    Field("name", "Name", table=False),
    NumberField("defense", "Defense", max=5),
    NumberField("soak", "Soak"),
    NumberField("price", "Price", max=100000),
    CheckboxField("restricted", "Restricted"),
    NumberField("encumbrance", "Encumbrance"),
    NumberField("hardpoints", "Hardpoints"),
    NumberField("rarity", "Rarity", max=10),
    TextareaField("description", "Description", table=False),
    ArrayField(Field("index", "Index"), table=False)
]))

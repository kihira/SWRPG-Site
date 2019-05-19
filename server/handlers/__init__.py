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
    Field("name", "Name"),
    SelectField("category", "Category", ["Armor", "Lightsaber", "Weapon"]),
    NumberField("price", "Price", max=100000),
    CheckboxField("restricted", "Restricted"),
    NumberField("encumbrance", "Encumbrance"),
    NumberField("hardpoints", "HP Required"),
    NumberField("rarity", "Rarity", max=10),
    TextareaField("description", "Description"),
    ArrayField(
        FieldGroup("modification", "Modification", [
            NumberField("number", "Number", min=1),
            SelectField("type", "Type", [
                {"display": "Damage", "value": "damage"},
                {"display": "Weapon Quality", "value": "weapon_quality"},
                {"display": "Innate Talent", "value": "innate_talent"},
                {"display": "Skill", "value": "skill"},
                {"display": "Characteristic", "value": "characteristic"},
                {"display": "Additional", "value": "additional"}
            ])
        ]), table=False),
    ArrayField(Field("index", "Index"), table=False)
]))

armor = Endpoint("armor", "Armor", Model([
    ObjectIdField("_id", "ID", readonly=True),
    Field("name", "Name"),
    NumberField("defense", "Defense", max=5),
    NumberField("soak", "Soak"),
    NumberField("hardpoints", "Hardpoints"),
    NumberField("encumbrance", "Encumbrance"),
    NumberField("price", "Price", max=100000),
    CheckboxField("restricted", "Restricted"),
    NumberField("rarity", "Rarity", max=10),
    TextareaField("description", "Description"),
    ArrayField(Field("index", "Index"), table=False)
]))

import re

from server.endpoint import Endpoint
from server.model import Model, Field, CheckboxField, TextareaField, SelectField, ArrayField, NumberField, ObjectIdField

gear_endpoint = Endpoint("gear", "Items", Model([
    ObjectIdField("_id", "ID"),
    Field("name", "Item", table=False),
    NumberField("price", "Price"),
    NumberField("encumbrance", "Encumbrance"),
    NumberField("rarity", "Rarity"),
    CheckboxField("restricted", "Restricted"),
    TextareaField("description", "Long Description", table=False),
    SelectField("category", "Category", options=[
        "Adversary",
        "Ancient Talismans",
        "Communications",
        "Consumables",
        "Cybernetics",
        "Detection Devices",
        "Droids",
        "Drugs",
        "Field Equipment",
        "Illegal Equipment",
        "Medical",
        "Poison",
        "Recreational",
        "Scanning and Surveillance",
        "Security",
        "Storage",
        "Survival",
        "Tools",
        "Uniforms"
    ], table=False),
    ArrayField(Field("index", "Index"), table=False)
]))
gear_endpoint.table_query = {"category": {"$not": re.compile("Adversary")}}

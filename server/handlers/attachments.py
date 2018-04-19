from server.endpoint import Endpoint
from server.model import Model, ObjectIdField, Field, NumberField, CheckboxField, TextareaField, SelectField

endpoint = Endpoint("attachments", Model([
    ObjectIdField("_id", "ID", readonly=True),
    Field("name", "Name"),
    SelectField("category", "Category", ["Armor", "Lightsaber", "Weapon"]),
    NumberField("price", "Price", max=100000),
    CheckboxField("restricted", "Restricted"),
    NumberField("encumbrance", "Encumbrance"),
    NumberField("hardpoints", "HP Required"),
    NumberField("rarity", "Rarity", max=10),
    TextareaField("description", "Description")
]))

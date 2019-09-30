from server.endpoint import Endpoint
from server.model import Model, Field, CheckboxField, FieldGroup, NumberField

from pymongo import ASCENDING


species_endpoint = Endpoint("species", "Species", Model([
    Field("_id", "Name", table=False),
    CheckboxField("player", "Player"),
    FieldGroup("characteristics", "Characteristics", [
        NumberField("brawn", "Brawn", 1, 5, default=1),
        NumberField("agility", "Agility", 1, 5, default=1),
        NumberField("intellect", "Intellect", 1, 5, default=1),
        NumberField("cunning", "Cunning", 1, 5, default=1),
        NumberField("willpower", "Willpower", 1, 5, default=1),
        NumberField("presence", "Presence", 1, 5, default=1),
    ]),
    NumberField("wound", "Wound Threshold"),
    NumberField("strain", "Strain Threshold"),
    NumberField("xp", "Starting XP", required=False)
]))
species_endpoint.table_sort = {"key": "_id", "dir": ASCENDING}

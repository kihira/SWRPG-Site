from server import filters

from server.endpoint import Endpoint
from server.model import Model, Field, ObjectIdField, SelectField, ArrayField, FieldGroup, NumberField

creatures_endpoint = Endpoint("creatures", "Creatures", Model([
    ObjectIdField("_id", "ID", readonly=True),
    Field("name", "Name", table=False),
    SelectField("level", "Type", ["Minion", "Rival", "Nemesis"]),
    FieldGroup("characteristics", "Characteristics", [
        NumberField("brawn", "Brawn", 1, 5, default=1),
        NumberField("agility", "Agility", 1, 5, default=1),
        NumberField("intellect", "Intellect", 1, 5, default=1),
        NumberField("cunning", "Cunning", 1, 5, default=1),
        NumberField("willpower", "Willpower", 1, 5, default=1),
        NumberField("presence", "Presence", 1, 5, default=1),
    ]),
    NumberField("soak", "Soak", table=False),
    NumberField("wound", "Wound Threshold", table=False),
    NumberField("strain", "Strain Threshold", table=False),
    ArrayField(FieldGroup("skills", "Skills", [
        Field("id", "Skill"),
        NumberField("value", "Value")
    ], render_method=filters.format_skill)),
    ArrayField(Field("talents", "Talents", render=filters.format_talent)),
    ArrayField(Field("abilities", "Abilities", render=filters.format_ability)),
    ArrayField(FieldGroup("equipment", "Weapons", [
        Field("name", "Name"),
        Field("damage", "Damage"),
        Field("critical", "Critical"),
        SelectField("range", "Range", ["Engaged", "Short", "Medium", "Long", "Extreme"]),
        SelectField("skill", "Skill", ["Brawl", "Ranged_Light", "Ranged_Heavy"]),
        ArrayField(FieldGroup("special", "Special", [
            Field("id", "Quality ID"),
            NumberField("value", "Value"),
        ]))
    ], render_method=lambda x: x["name"])),
    ArrayField(Field("index", "Index"), table=False)
]))


def process_items(items: list):
    for item in items:
        item["skills"] = filters.format_list(item["skills"], "skills")
        item["talents"] = filters.format_list(item["talents"], "talents")
        item["abilities"] = filters.format_list(item["abilities"], "abilities")
        equipment = ""
        for i in item["equipment"]:
            equipment += f'{i["name"]}, '
        item["equipment"] = equipment[:-2]
    return items

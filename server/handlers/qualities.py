from server import filters

from server.endpoint import Endpoint
from server.model import Model, Field, SelectField, TextareaField, CheckboxField, ArrayField

qualities_endpoint = Endpoint("qualities", "Qualities", Model([
    Field("_id", "Name", table=False),
    SelectField("active", "Active", ["Active", "Passive"]),
    TextareaField("description", "Description", render=filters.description),
    CheckboxField("ranked", "Ranked", render=filters.format_yes_no),
    ArrayField(Field("index", "Index"), table=False),
]), objectid=False)

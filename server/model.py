from bson import ObjectId
from werkzeug.datastructures import MultiDict
from typing import Callable


class Field:
    mongo_name: str
    human_name: str
    html_type: str
    default: object
    readonly: bool
    required: bool
    table: bool
    render_method: Callable[[any], str] = str

    def __init__(self, mongo_name, human_name, html_type="text", default=None, readonly=False, required=True, table=True, render=None):
        self.mongo_name = mongo_name
        self.human_name = human_name
        self.html_type = html_type
        self.default = default
        self.readonly = readonly
        self.required = required
        self.table = table

        if render is not None:
            self.render_method = render

    def get_value(self, form: MultiDict):
        return form.get(self.mongo_name, self.default)

    def table_display(self) -> bool:
        return self.table

    def get_datatables_object(self) -> object:
        """
        Gets a dict that will be used for Datatables
        :return:
        """
        return {"name": self.mongo_name, "filter": self.get_filter()}

    def get_filter(self):
        """
        Gets filter object for use in Datatables
        :return:
        """
        return {"type": self.html_type}

    def render(self, value) -> str:
        """
        Render the value to display on the items page or in a table
        """
        return self.render_method(value)


class CheckboxField(Field):
    def __init__(self, mongo_name, human_name, default=False, readonly=False, required=True, table=True, render=None):
        super().__init__(mongo_name, human_name, html_type="checkbox", default=default, readonly=readonly, required=required, table=table, render=render)

    def get_value(self, form: MultiDict):
        return self.mongo_name in form

    def get_datatables_object(self):
        # A bit hacky but this is most likely going to be the only case
        return {"name": self.mongo_name, "filter": self.get_filter(), "hidden": self.mongo_name == "restricted"}


class TextareaField(Field):
    def __init__(self, mongo_name, human_name, readonly=False, required=True, table=True, render=None):
        super().__init__(mongo_name, human_name, html_type="textarea", readonly=readonly, required=required, table=table, render=render)

    def get_value(self, form: MultiDict):
        return super().get_value(form).replace("\r\n", " ").replace("\n", " ")


class SelectField(Field):
    options = []

    def __init__(self, mongo_name, human_name, options: [], readonly=False, required=True, table=True, render=None):
        super().__init__(mongo_name, human_name, html_type="select", readonly=readonly, required=required, table=table, render=render)

        self.options = options

    def get_filter(self):
        return {"type": self.html_type, "data": self.options}


class NumberField(Field):
    min: int
    max: int
    step: int

    def __init__(self, mongo_name, human_name, min=0, max=100, default=0, step=1, required=True, table=True):
        super().__init__(mongo_name, human_name, html_type="number", default=default, required=required, table=table)

        self.min = min
        self.max = max
        self.step = step

    def get_value(self, form: MultiDict):
        return form.get(self.mongo_name, default=self.default, type=int)


class ObjectIdField(Field):
    def __init__(self, mongo_name, human_name, readonly=False):
        super().__init__(mongo_name, human_name, readonly=readonly, table=False)

    def get_value(self, form: MultiDict):
        val = form.get(self.mongo_name, "")
        if len(val) == 0:
            return ObjectId()
        return ObjectId(val)


class ArrayField(Field):
    field: Field

    def __init__(self, field: Field, readonly=False, required=True, table=True):
        super().__init__(field.mongo_name, field.human_name, html_type="array", readonly=readonly, required=required, table=table)

        self.field = field

    def get_value(self, form: MultiDict):
        return form.getlist(self.mongo_name + "[]")

    def render(self, value) -> str:
        out = ""
        for i in value:
            out += f'{self.field.render(i)}, '
        return out[:-2]


class FieldGroup(Field):
    fields: [Field]

    def __init__(self, group_name: str, human_name: str, fields: [Field], render: Callable[[any], str]=None):
        super().__init__(group_name, human_name, html_type="group", render=render)

        self.fields = fields
        self.render_method = render

    def get_value(self, form: MultiDict):
        values = {}
        for field in self.fields:
            values[field.mongo_name] = field.get_value(form)
        return values


class Model:
    fields: [Field]
    index: bool

    def __init__(self, fields: [Field], index=True):
        self.fields = fields
        self.index = index

    def __getitem__(self, item):
        for field in self.fields:
            if item == field.mongo_name:
                return field

    def get_table_fields(self):
        """
        Gets all the fields that should be displayed in the table when displaying them together
        :return:
        """
        fields = []
        for field in self.fields:
            if field.table_display():
                fields.append(field)
        return fields

    def from_form(self, form: MultiDict):
        out = {}
        for field in self.fields:
            out[field.mongo_name] = field.get_value(form)
        return out

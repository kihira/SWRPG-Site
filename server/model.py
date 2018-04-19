from bson import ObjectId
from werkzeug.datastructures import MultiDict


class Field:
    mongo_name: str
    human_name: str
    html_type: str
    default: object
    readonly: bool
    required: bool

    def __init__(self, mongo_name, human_name, html_type="text", default=None, readonly=False, required=True):
        self.mongo_name = mongo_name
        self.human_name = human_name
        self.html_type = html_type
        self.default = default
        self.readonly = readonly
        self.required = required

    def get_value(self, form: MultiDict):
        return form.get(self.mongo_name, self.default)

    def table_display(self):
        return self.mongo_name != "_id" and self.mongo_name != "name" and self.mongo_name != "category" and self.mongo_name != "description"

    def get_datatables_object(self):
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


class CheckboxField(Field):
    def __init__(self, mongo_name, human_name, default=False):
        super().__init__(mongo_name, human_name, html_type="checkbox", default=default)

    def get_value(self, form: MultiDict):
        return self.mongo_name in form

    def get_datatables_object(self):
        # A bit hacky but this is most likely going to be the only case
        return {"name": self.mongo_name, "filter": self.get_filter(), "hidden": self.mongo_name == "restricted"}


class TextareaField(Field):
    def __init__(self, mongo_name, human_name):
        super().__init__(mongo_name, human_name, html_type="textarea")

    def get_value(self, form: MultiDict):
        return super().get_value(form).replace("\r\n", " ").replace("\n", " ")


class SelectField(Field):
    options = []

    def __init__(self, mongo_name, human_name, options: []):
        super().__init__(mongo_name, human_name, html_type="select")

        self.options = options

    def get_filter(self):
        return {"type": self.html_type, "data": self.options}


class NumberField(Field):
    min: int
    max: int
    step: int

    def __init__(self, mongo_name, human_name, min=0, max=100, default=0, step=1, required=True):
        super().__init__(mongo_name, human_name, html_type="number", default=default, required=required)

        self.min = min
        self.max = max
        self.step = step

    def get_value(self, form: MultiDict):
        return form.get(self.mongo_name, default=self.default, type=int)


class ObjectIdField(Field):
    def __init__(self, mongo_name, human_name, readonly=False):
        super().__init__(mongo_name, human_name, readonly=readonly)

    def get_value(self, form: MultiDict):
        print(form)
        return ObjectId(form.get(self.mongo_name, ""))


class ArrayField(Field):
    field: Field

    def __init__(self, field: Field):
        super().__init__(field.mongo_name, field.human_name, html_type="array")

        self.field = field

    def get_value(self, form: MultiDict):
        return form.getlist(self.mongo_name)


class FieldGroup(Field):
    fields: [Field]

    def __init__(self, group_name, human_name, fields: [Field]):
        super().__init__(group_name, human_name, html_type="group")

        self.fields = fields

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

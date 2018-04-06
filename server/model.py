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


class CheckboxField(Field):
    def __init__(self, mongo_name, human_name, default=False):
        super().__init__(mongo_name, human_name, html_type="checkbox", default=default)

    def get_value(self, form: MultiDict):
        return self.mongo_name in form


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


class ArrayField(Field):
    field: Field

    def __init__(self, field: Field):
        super().__init__(field.mongo_name, field.human_name, html_type="array")

        self.field = field

    def get_value(self, form: MultiDict):
        return form.getlist(self.mongo_name)


class Model:
    fields: [Field]

    def __init__(self, fields: [Field]):
        self.fields = fields

    def from_form(self, form: MultiDict):
        out = {}
        for field in self.fields:
            out[field.mongo_name] = field.get_value(form)
        return out

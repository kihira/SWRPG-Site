class Field:
    human_name: str = ""
    mongo_name: str = ""
    required: bool = True


class Model:
    fields: [Field] = []

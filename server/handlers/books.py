from server.endpoint import Endpoint
from server.model import Model, Field, TextareaField, SelectField

book_endpoint = Endpoint("books", "Books", Model([
    Field("name", "Name", table=False),
    SelectField("system", "System", [
        "Edge of the Empire",
        "Age of Rebellion",
        "Force and Destiny",
        "Star Wars Roleplaying"
    ]),
    Field("key", "SKU"),
    Field("_id", "Initials"),  # todo should allow specifying custom order for table display
    Field("isbn", "ISBN", table=False),
    Field("ffg_url", "Product Page", html_type="url", table=False),
    Field("release_date", "Release Date", html_type="date", table=False),
    TextareaField("description", "Description", table=False)
], index=False), objectid=False)
